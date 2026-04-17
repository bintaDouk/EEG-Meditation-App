"""
EEG Meditation Feature Extraction & Score Pipeline
====================================================
Fixes applied vs original:
  - hjorth_parameters now returns (activity, mobility, complexity) arrays,
    separate from the DataFrame builder (hjorth_to_df)
  - hjorth_per_band uses epochs.get_data() and calls the corrected helper
  - compute_entropy_features: removed dangling statement, fixed 'General Entropy' key
  - compute_connectivity_features: freq_bands variable name unified
  - feature_extraction: passes epochs.get_data() to hjorth, assembles final DataFrame
  - bandpower dict converted to DataFrame
  - MeditationScorer class maps features -> user-friendly scores
"""
 
import numpy as np
import pandas as pd
from scipy import stats
import mne
from mne_connectivity import spectral_connectivity_epochs
 
 
# ---------------------------------------------------------------------------
# Frequency bands
# ---------------------------------------------------------------------------
 
FREQ_BANDS = {
    "delta": (1,  4),
    "theta": (4,  8),
    "alpha": (8,  12),
    "beta":  (12, 30),
    "gamma": (30, 45),
}
 
 
# ---------------------------------------------------------------------------
# Hjorth parameters
# ---------------------------------------------------------------------------
 
def hjorth_parameters(data):
    """
    Compute raw Hjorth arrays for EEG epochs.
 
    Parameters
    ----------
    data : np.ndarray, shape (n_epochs, n_channels, n_times)
 
    Returns
    -------
    activity   : (n_epochs, n_channels)
    mobility   : (n_epochs, n_channels)
    complexity : (n_epochs, n_channels)
    """
    d1 = np.diff(data, n=1, axis=-1)
    d2 = np.diff(data, n=2, axis=-1)
 
    var_x  = data.var(axis=-1)
    var_d1 = d1.var(axis=-1)
    var_d2 = d2.var(axis=-1)
 
    activity   = var_x
    mobility   = np.sqrt(var_d1 / (var_x + 1e-12))
    complexity = np.sqrt(var_d2 / (var_d1 + 1e-12)) / (mobility + 1e-12)
 
    return activity, mobility, complexity
 
 
def hjorth_to_df(data, ch_names):
    """Build a tidy DataFrame from Hjorth arrays (drops activity — redundant with band power)."""
    activity, mobility, complexity = hjorth_parameters(data)
 
    mob_cols  = [f"hjorth_mobility_{ch}"   for ch in ch_names]
    comp_cols = [f"hjorth_complexity_{ch}" for ch in ch_names]
 
    return pd.DataFrame(
        np.concatenate([mobility, complexity], axis=1),
        columns=mob_cols + comp_cols,
    )
 
 
def hjorth_per_band(epochs, freq_bands=FREQ_BANDS):
    """Hjorth mobility & complexity computed inside each frequency band."""
    ch_names = epochs.ch_names
    rows = []
 
    for band, (fmin, fmax) in freq_bands.items():
        ep   = epochs.copy().filter(fmin, fmax, method="iir", verbose=False)
        data = ep.get_data()                          # (n_epochs, n_ch, n_times)
        _, mob, comp = hjorth_parameters(data)
 
        cols  = (
            [f"hjorth_mobility_{band}_{ch}"   for ch in ch_names] +
            [f"hjorth_complexity_{band}_{ch}" for ch in ch_names]
        )
        block = np.concatenate([mob, comp], axis=1)
        rows.append(pd.DataFrame(block, columns=cols))
 
    return pd.concat(rows, axis=1)
 
 
# ---------------------------------------------------------------------------
# Connectivity
# ---------------------------------------------------------------------------
 
def compute_connectivity_features(epochs, freq_bands=FREQ_BANDS):
    """
    Pairwise coherence (upper triangle) for each band.
 
    Returns DataFrame with columns  coh_{band}_ch1-ch2.
    """
    ch_names = epochs.ch_names
    n_ch     = len(ch_names)
    triu_idx = np.triu_indices(n_ch, k=1)
 
    pair_labels = [
        f"{ch_names[i]}-{ch_names[j]}"
        for i, j in zip(*triu_idx)
    ]
 
    rows = []
    for band, (fmin, fmax) in freq_bands.items():
        con = spectral_connectivity_epochs(
            epochs,
            method="coh",
            mode="fourier",
            sfreq=epochs.info["sfreq"],
            fmin=fmin,
            fmax=fmax,
            faverage=True,
            verbose=False,
        )
        # con.get_data() -> (n_connections, n_freqs_or_1)
        # With faverage=True the last dim is 1; squeeze it
        con_matrix = con.get_data(output="dense")  # (n_ch, n_ch, 1)
        con_matrix = con_matrix[:, :, 0]           # (n_ch, n_ch)
 
        # con.get_data(output="dense") averages over epochs already,
        # but we want per-epoch values — use the flat form instead:
        con_flat = con.get_data()                  # (n_connections,)
 
        cols = [f"coh_{band}_{lbl}" for lbl in pair_labels]
        # broadcast to n_epochs rows (connectivity is averaged over epochs in
        # spectral_connectivity_epochs; repeat for shape consistency)
        n_epochs = len(epochs)
        rows.append(
            pd.DataFrame(
                np.tile(con_flat, (n_epochs, 1)),
                columns=cols,
            )
        )
 
    return pd.concat(rows, axis=1)

def compute_connectivity_features(epochs, freq_bands):
    con_features = []

    for band, (fmin, fmax) in freq_bands.items():
        con = spectral_connectivity_epochs(
            epochs,
            method="coh",          # coherence
            mode="fourier",
            sfreq=epochs.info["sfreq"],
            fmin=fmin,
            fmax=fmax,
            faverage=True,         # average within band
            verbose=False
        )
    
        # get connectivity matrix
        con_data = con.get_data()  # shape: (n_epochs, n_nodes, n_nodes)
    
        con_features.append(con_data)
    # stack bands
    con_features = np.stack(con_features, axis=1)

    # Flatten 
    n_epochs, n_bands, n_ch, _ = con_features.shape
    
    triu_idx = np.triu_indices(n_ch, k=1)
    
    features = []
    
    for i in range(n_epochs):
        feat = []
        for b in range(n_bands):
            mat = con_features[i, b]
            feat.extend(mat[triu_idx])  # upper triangle
        features.append(feat)
    
    X_conn = np.array(features)
    df_conn = pd.DataFrame(X_conn)
    return df_conn
 
 
# ---------------------------------------------------------------------------
# Entropy
# ---------------------------------------------------------------------------
 
def compute_entropy_features(psd_data, freqs, freq_bands=FREQ_BANDS):
    """
    Parameters
    ----------
    psd_data : (n_epochs, n_channels, n_freqs)
    freqs    : (n_freqs,)
 
    Returns
    -------
    DataFrame with one spectral-entropy column per band + overall entropy.
    """
    eps = 1e-12
 
    # ── Overall spectral entropy ────────────────────────────────────────────
    psd_norm         = psd_data / (psd_data.sum(axis=-1, keepdims=True) + eps)
    overall_entropy  = -(psd_norm * np.log(psd_norm + eps)).sum(axis=-1)
    # Shape (n_epochs, n_channels) -> one scalar per epoch (mean over channels)
    entropy_dict = {"spectral_entropy_overall": overall_entropy.mean(axis=-1)}
 
    # ── Per-band spectral entropy ───────────────────────────────────────────
    for band, (fmin, fmax) in freq_bands.items():
        idx = (freqs >= fmin) & (freqs <= fmax)
        if not idx.any():
            continue
        band_psd      = psd_data[:, :, idx]
        band_psd_norm = band_psd / (band_psd.sum(axis=-1, keepdims=True) + eps)
        entropy       = -(band_psd_norm * np.log(band_psd_norm + eps)).sum(axis=-1)
        entropy_dict[f"spectral_entropy_{band}"] = entropy.mean(axis=-1)
 
    return pd.DataFrame(entropy_dict)
 
 
# ---------------------------------------------------------------------------
# Band power
# ---------------------------------------------------------------------------
 
def bandpower_from_psd(psd_data, freqs, band):
    fmin, fmax = band
    idx = (freqs >= fmin) & (freqs <= fmax)

    if not np.any(idx):
        return np.zeros((psd_data.shape[0], psd_data.shape[1]))
        
    return psd_data[..., idx].mean(axis=-1)   # (n_epochs, n_channels)
 
 
def bandpower_to_df(psd_data, freqs, ch_names, freq_bands=FREQ_BANDS):
    rows = {}
    for band, frange in freq_bands.items():
        bp = bandpower_from_psd(psd_data, freqs, frange)  # (n_epochs, n_ch)
        print(psd_data.shape, bp.shape, len(ch_names))
        for ci, ch in enumerate(ch_names):
            rows[f"bp_{band}_{ch}"] = bp[:, ci]
    return pd.DataFrame(rows)
 
 
# ---------------------------------------------------------------------------
# Time-domain features
# ---------------------------------------------------------------------------
 
def time_features(data, ch_names):
    """
    Parameters
    ----------
    data : (n_epochs, n_channels, n_times)
    """
    def zcr(x):
        signs     = np.sign(x)
        crossings = np.diff(signs, axis=-1)
        return (crossings != 0).sum(axis=-1) / x.shape[-1]
 
    stat_features = {
        "mean": data.mean(axis=-1),
        "var":  data.var(axis=-1),
        "std":  data.std(axis=-1),
        "ptp":  np.ptp(data, axis=-1),
        "skew": stats.skew(data, axis=-1),
        "kurt": stats.kurtosis(data, axis=-1),
        "rms":  np.sqrt((data ** 2).mean(axis=-1)),
        "zcr":  zcr(data),
    }
 
    blocks = np.concatenate(list(stat_features.values()), axis=1)
    cols   = [
        f"{stat}_{ch}"
        for stat in stat_features
        for ch in ch_names
    ]
    return pd.DataFrame(blocks, columns=cols)


def feature_extraction(raw_clean, freq_bands=FREQ_BANDS, epoch_duration=2.0):
    """
    Run the full feature pipeline on a preprocessed Raw object.
 
    Returns
    -------
    df_features : DataFrame, one row per epoch
    epochs      : mne.Epochs  (kept for downstream use)
    psd_data    : (n_epochs, n_ch, n_freqs)
    freqs       : (n_freqs,)
    """
    # ── Epoch ───────────────────────────────────────────────────────────────
    events = mne.make_fixed_length_events(raw_clean, duration=epoch_duration)
    epochs = mne.Epochs(
        raw_clean, events,
        tmin=0, tmax=epoch_duration,
        baseline=None, preload=True,
    )
    ch_names = epochs.ch_names
    data     = epochs.get_data()                          # (n_epochs, n_ch, n_times)
 
    # ── PSD ─────────────────────────────────────────────────────────────────
    psd_obj           = epochs.compute_psd(
        method="welch", fmin=1, fmax=45, n_fft=256, n_overlap=128,
    )
    psd_data, freqs   = psd_obj.get_data(return_freqs=True)   # (n_epochs, n_ch, n_freqs)
    ch_names_psd = psd_obj.ch_names
    print(len(psd_obj.ch_names))
    # ── Feature blocks ──────────────────────────────────────────────────────
    df_bp       = bandpower_to_df(psd_data, freqs, ch_names_psd, freq_bands)
    df_time     = time_features(data, ch_names)
    df_hjorth   = hjorth_to_df(data, ch_names)
    df_hjorth_b = hjorth_per_band(epochs, freq_bands)
    #df_conn     = compute_connectivity_features(epochs, freq_bands)
    df_entropy  = compute_entropy_features(psd_data, freqs, freq_bands)
 
    df_features = pd.concat(
        [df_bp, df_time, df_hjorth, df_hjorth_b,  df_entropy],
        axis=1,
    )
    #df_conn,
 
    return df_features, epochs, psd_data, freqs



class MeditationScorer:
    """
    Maps extracted EEG features to interpretable 0-100 meditation scores.
 
    Scores
    ------
    focus_score       : Sustained focused attention (beta-driven, low theta)
    calm_score        : Relaxed, non-aroused state (alpha dominant)
    mindfulness_score : Internally directed, aware state (frontal theta + alpha)
    stability_score   : How consistent/stable the mental state is (low entropy)
    drowsiness_risk   : Risk of drifting to sleep (delta/theta dominance)
 
    All scores are percentile-ranked within the session so that the first
    epoch is not unfairly penalised by an arbitrary absolute scale.
    The scorer can also be fitted on a baseline (eyes-closed rest) to
    produce calibrated scores relative to that individual's baseline.
    """
 
    FRONTAL_CHANNELS = {"F3", "F4", "Fz", "AF3", "AF4", "F7", "F8"}
    CENTRAL_CHANNELS = {"C3", "C4", "Cz"}
    OCCIPITAL_CHANNELS = {"O1", "O2", "Oz"}
 
    def __init__(self, ch_names, freq_bands=FREQ_BANDS):
        self.ch_names   = ch_names
        self.freq_bands = freq_bands
        self._baseline  = None   # set via fit_baseline()
 
    # ── helpers ─────────────────────────────────────────────────────────────
 
    def _ch_idx(self, group: set) -> list[int]:
        """Indices of channels belonging to a spatial group."""
        return [i for i, ch in enumerate(self.ch_names) if ch in group]
 
    def _band_mean(self, psd_data, freqs, band_name, ch_idx=None):
        """Mean power in a band, optionally restricted to channel subset."""
        fmin, fmax = self.freq_bands[band_name]
        idx        = (freqs >= fmin) & (freqs <= fmax)
        data       = psd_data[:, ch_idx, :] if ch_idx else psd_data
        return data[:, :, idx].mean(axis=(1, 2))   # (n_epochs,)
 
    @staticmethod
    def _minmax(x):
        rng = x.max() - x.min()
        return (x - x.min()) / (rng + 1e-12)
 
    @staticmethod
    def _percentile_scale(x):
        """Rank-based 0-1 scaling — robust to outliers."""
        from scipy.stats import rankdata
        return (rankdata(x) - 1) / (len(x) - 1 + 1e-12)
 
    # ── baseline calibration ────────────────────────────────────────────────
 
    def fit_baseline(self, psd_baseline, freqs):
        """
        Fit scorer to a resting-state (eyes-closed) PSD.
 
        Parameters
        ----------
        psd_baseline : (n_epochs, n_channels, n_freqs) from a rest recording
        freqs        : matching frequency axis
        """
        self._baseline = {
            band: self._band_mean(psd_baseline, freqs, band)
            for band in self.freq_bands
        }
 
    # ── individual score components ─────────────────────────────────────────
 
    def focus_score(self, psd_data, freqs):
        """
        β / (α + θ)  at frontal channels.
 
        High beta relative to alpha+theta = engaged, directed attention.
        Rises during focused attention meditation (Samatha, breath focus).
        """
        f_idx = self._ch_idx(self.FRONTAL_CHANNELS) or list(range(len(self.ch_names)))
 
        beta  = self._band_mean(psd_data, freqs, "beta",  f_idx)
        alpha = self._band_mean(psd_data, freqs, "alpha", f_idx)
        theta = self._band_mean(psd_data, freqs, "theta", f_idx)
 
        raw = beta / (alpha + theta + 1e-12)
        return self._percentile_scale(raw) * 100
 
    def calm_score(self, psd_data, freqs):
        """
        Posterior/central alpha power, penalised by beta (arousal).
 
        High alpha + low beta = eyes-closed, cortically idle, calm.
        Classic 'relaxation' metric — highest during open-monitoring states.
        """
        oc_idx = (
            self._ch_idx(self.OCCIPITAL_CHANNELS | self.CENTRAL_CHANNELS)
            or list(range(len(self.ch_names)))
        )
 
        alpha = self._band_mean(psd_data, freqs, "alpha", oc_idx)
        beta  = self._band_mean(psd_data, freqs, "beta",  oc_idx)
 
        raw = alpha / (beta + 1e-12)
        return self._percentile_scale(raw) * 100
 
    def mindfulness_score(self, psd_data, freqs):
        """
        Frontal midline theta + moderate alpha (θ/α ratio).
 
        Elevated frontal theta reflects internal monitoring, meta-awareness.
        Particularly associated with open-monitoring (Vipassana-style) practice.
        """
        f_idx = self._ch_idx(self.FRONTAL_CHANNELS | self.CENTRAL_CHANNELS) or list(range(len(self.ch_names)))
 
        theta = self._band_mean(psd_data, freqs, "theta", f_idx)
        alpha = self._band_mean(psd_data, freqs, "alpha", f_idx)
 
        # θ/α > 1 = theta-dominant = mindfulness signature
        raw = theta / (alpha + 1e-12)
        return self._percentile_scale(raw) * 100
 
    def stability_score(self, df_features):
        """
        Inverse spectral entropy, smoothed over a rolling window.
 
        Low entropy = ordered, regular brain rhythm = sustained state.
        Drops when the user's mind wanders or transitions between states.
        """
        if "spectral_entropy_overall" not in df_features.columns:
            raise ValueError("Run compute_entropy_features first.")
 
        entropy = df_features["spectral_entropy_overall"].values
        # Invert: high entropy -> low stability
        raw = -entropy
        return self._percentile_scale(raw) * 100
 
    def drowsiness_risk(self, psd_data, freqs):
        """
        (δ + θ) / (α + β)  — high slow-wave dominance signals sleep onset.
 
        Use as an alert trigger:  > 65 for 3+ consecutive epochs -> warning.
        Importantly different from focus loss: focus loss = beta drop,
        drowsiness = delta/theta surge.
        """
        delta = self._band_mean(psd_data, freqs, "delta")
        theta = self._band_mean(psd_data, freqs, "theta")
        alpha = self._band_mean(psd_data, freqs, "alpha")
        beta  = self._band_mean(psd_data, freqs, "beta")
 
        raw = (delta + theta) / (alpha + beta + 1e-12)
        return self._percentile_scale(raw) * 100
 
    def frontal_alpha_asymmetry(self, psd_data, freqs):
        """
        FAA = ln(F4 alpha) - ln(F3 alpha).
 
        Positive = left-prefrontal dominant = approach motivation, positive affect.
        Negative = right-prefrontal dominant = withdrawal, stress.
        Reported per epoch (not rescaled — the sign carries meaning).
        """
        try:
            f3_idx = self.ch_names.index("F3")
            f4_idx = self.ch_names.index("F4")
        except ValueError:
            return np.full(psd_data.shape[0], np.nan)
 
        fmin, fmax = self.freq_bands["alpha"]
        fidx       = (freqs >= fmin) & (freqs <= fmax)
 
        f3_alpha = psd_data[:, f3_idx, :][:, fidx].mean(axis=-1)
        f4_alpha = psd_data[:, f4_idx, :][:, fidx].mean(axis=-1)
 
        return np.log(f4_alpha + 1e-12) - np.log(f3_alpha + 1e-12)
 
    # ── focus-loss detector ─────────────────────────────────────────────────
 
    def detect_focus_loss(
        self,
        psd_data,
        freqs,
        threshold: float = 35.0,
        min_consecutive: int = 3,
    ) -> np.ndarray:
        """
        Returns a boolean array (n_epochs,) flagging focus-loss events.
 
        A focus-loss event is declared when focus_score < threshold for
        at least `min_consecutive` epochs in a row.  The debounce prevents
        single-epoch artefacts from triggering false alerts.
 
        Parameters
        ----------
        threshold       : focus score below which an epoch is 'at risk'
        min_consecutive : minimum run length before alert fires
 
        Returns
        -------
        alert_mask : (n_epochs,) bool — True = alert should fire this epoch
        """
        scores     = self.focus_score(psd_data, freqs)
        below      = scores < threshold
        alert_mask = np.zeros(len(scores), dtype=bool)
 
        run = 0
        for i, b in enumerate(below):
            run = run + 1 if b else 0
            if run >= min_consecutive:
                alert_mask[i] = True
 
        return alert_mask
 
    # ── full score summary ──────────────────────────────────────────────────
 
    def compute_all(self, psd_data, freqs, df_features):
        """
        Compute all scores and return a tidy DataFrame aligned with epochs.
 
        Returns
        -------
        df_scores : DataFrame with one row per epoch
        summary   : dict with session-level statistics
        """
        df_scores = pd.DataFrame({
            "focus_score":       self.focus_score(psd_data, freqs),
            "calm_score":        self.calm_score(psd_data, freqs),
            "mindfulness_score": self.mindfulness_score(psd_data, freqs),
            "stability_score":   self.stability_score(df_features),
            "drowsiness_risk":   self.drowsiness_risk(psd_data, freqs),
            "faa":               self.frontal_alpha_asymmetry(psd_data, freqs),
            "focus_loss_alert":  self.detect_focus_loss(psd_data, freqs),
        })
 
        summary = {
            "mean_focus":          df_scores["focus_score"].mean(),
            "mean_calm":           df_scores["calm_score"].mean(),
            "mean_mindfulness":    df_scores["mindfulness_score"].mean(),
            "mean_stability":      df_scores["stability_score"].mean(),
            "peak_focus":          df_scores["focus_score"].max(),
            "time_focused_pct":    (df_scores["focus_score"] > 60).mean() * 100,
            "time_drowsy_pct":     (df_scores["drowsiness_risk"] > 65).mean() * 100,
            "n_focus_loss_events": df_scores["focus_loss_alert"].sum(),
            "session_style":       self._classify_session(df_scores),
        }
 
        return df_scores, summary
 
    def _classify_session(self, df_scores):
        """
        Heuristic classification of meditation style from score profile.
 
        focused_attention : high focus, moderate calm
        open_monitoring   : high mindfulness + calm, lower focus
        drowsy            : high drowsiness, low focus
        restless          : low stability throughout
        """
        f = df_scores["focus_score"].mean()
        c = df_scores["calm_score"].mean()
        m = df_scores["mindfulness_score"].mean()
        d = df_scores["drowsiness_risk"].mean()
        s = df_scores["stability_score"].mean()
 
        if d > 65:
            return "drowsy"
        if s < 30:
            return "restless"
        if f > 60 and f > m:
            return "focused_attention"
        if m > 55 and c > 50:
            return "open_monitoring"
        return "mixed"
        
def run_pipeline(raw_clean):
    """
    One-shot function: raw MNE object -> scores DataFrame + summary dict.
    
    Usage
    -----
        df_features, epochs, psd_data, freqs = feature_extraction(raw_clean)
        scorer    = MeditationScorer(epochs.ch_names)
        df_scores, summary = scorer.compute_all(psd_data, freqs, df_features)
    """
    df_features, epochs, psd_data, freqs = feature_extraction(raw_clean)
    scorer = MeditationScorer(epochs.ch_names)
    df_scores, summary = scorer.compute_all(psd_data, freqs, df_features)
    return df_features, df_scores, summary




