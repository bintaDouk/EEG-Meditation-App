"""
Preprocessing module for EEG data artifacts and ICA.
"""

from typing import List, Tuple, Optional
import mne
from mne_icalabel import label_components
import numpy as np


class Preprocessor:
    """Handles preprocessing of EEG data including filtering, ICA, and artifact removal."""
    
    def __init__(self, raw: mne.io.BaseRaw):
        """
        Initialize Preprocessor with raw EEG data.
        
        Parameters
        ----------
        raw : mne.io.BaseRaw
            The raw EEG data to preprocess
        """
        self.raw = raw
        self.ica = None
        self.filt_raw = None
    
    def detect_eog_artifacts(self, ch_name: str = 'EXG1', threshold: float = 2.0) -> mne.Epochs:
        """
        Detect and create epochs around EOG (eye movement) artifacts.
        
        Parameters
        ----------
        ch_name : str, default='EXG1'
            Name of the EOG channel
        threshold : float, default=2.0
            Threshold for EOG artifact detection
        
        Returns
        -------
        mne.Epochs
            Epochs containing EOG-triggered events
        """
        try:
            eog_epochs = mne.preprocessing.create_eog_epochs(self.raw, ch_name=ch_name, threshold=threshold)
            eog_evoked = eog_epochs.average()
            eog_evoked.apply_baseline(baseline=(None, -0.2))
            
            print(f"[OK] EOG artifacts detected and epoched")
            print(f"  - Number of EOG events: {len(eog_epochs)}")
            
            return eog_epochs
        except Exception as e:
            print(f"[ERROR] Error detecting EOG artifacts: {e}")
            return None
    
    def detect_ecg_artifacts(self, ch_name: str = 'EXG7', threshold: float = 0.5) -> mne.Epochs:
        """
        Detect and create epochs around ECG (heart beat) artifacts.
        
        Parameters
        ----------
        ch_name : str, default='EXG7'
            Name of the ECG channel
        threshold : float, default=0.5
            Threshold for ECG artifact detection
        
        Returns
        -------
        mne.Epochs
            Epochs containing ECG-triggered events
        """
        try:
            ecg_epochs = mne.preprocessing.create_ecg_epochs(self.raw, ch_name=ch_name, threshold=threshold)
            ecg_evoked = ecg_epochs.average()
            ecg_evoked.apply_baseline(baseline=(None, -0.2))
            
            print(f"[OK] ECG artifacts detected and epoched")
            print(f"  - Number of ECG events: {len(ecg_epochs)}")
            
            return ecg_epochs
        except Exception as e:
            print(f"[ERROR] Error detecting ECG artifacts: {e}")
            return None
    
    def filter_data(
        self,
        l_freq: float = 1.0,
        h_freq: float = 40.0,
        method: str = 'iir'
    ) -> mne.io.BaseRaw:
        """
        Apply highpass and lowpass filters to raw data.
        
        Parameters
        ----------
        l_freq : float, default=1.0
            Lowpass frequency cutoff in Hz
        h_freq : float, default=40.0
            Highpass frequency cutoff in Hz
        method : str, default='iir'
            Filter method ('iir' or 'fir')
        
        Returns
        -------
        mne.io.BaseRaw
            Filtered copy of raw data
        """
        try:
            self.raw.load_data()
            self.filt_raw = self.raw.copy().filter(l_freq, h_freq, method=method)
            
            print(f"[OK] Data filtered successfully")
            print(f"  - Filter type: bandpass ({l_freq}-{h_freq} Hz)")
            print(f"  - Method: {method}")
            
            return self.filt_raw
        except Exception as e:
            print(f"[ERROR] Error filtering data: {e}")
            return None
    
    def fit_ica(
        self,
        n_components: int = 20,
        method: str = 'fastica',
        random_state: int = 42,
        use_filtered: bool = True
    ) -> Optional[mne.preprocessing.ICA]:
        """
        Fit ICA model to decompose data into independent components.
        
        Parameters
        ----------
        n_components : int, default=20
            Number of ICA components to extract
        method : str, default='fastica'
            ICA method ('fastica', 'infomax', or 'picard')
        random_state : int, default=42
            Random seed for reproducibility
        use_filtered : bool, default=True
            Use filtered data (requires filter_data() called first)
        
        Returns
        -------
        mne.preprocessing.ICA or None
            Fitted ICA object
        """
        try:
            data_to_fit = self.filt_raw if use_filtered and self.filt_raw else self.raw
            
            self.ica = mne.preprocessing.ICA(
                n_components=n_components,
                method=method,
                random_state=random_state
            )
            self.ica.fit(data_to_fit)
            
            print(f"[OK] ICA fitted successfully")
            print(f"  - Components: {n_components}")
            print(f"  - Method: {method}")
            #print(f"  - Explained variance: {self.ica.get_explained_variance_ratio(self.filt_raw).sum():.2%}")
            
            return self.ica
        except Exception as e:
            print(f"[ERROR] Error fitting ICA: {e}")
            return None
    
    def auto_label_ica_components(self) -> Tuple[List[str], np.ndarray]:
        """
        Automatically label ICA components as brain or artifact using ICLabel.
        
        Returns
        -------
        tuple
            (labels, probabilities) - Labels of components and their probabilities
        """
        if self.ica is None:
            print("[ERROR] No ICA model fitted.")
            return None, None
        
        try:
            ic_labels = label_components(self.raw, self.ica, method="iclabel")
            labels = ic_labels["labels"]
            probabilities = ic_labels["y_pred_proba"]
            
            print(f"[OK] ICA components labeled using ICLabel")
            for i, label in enumerate(labels):
                print(f"  - Component {i}: {label}")
            
            return labels, probabilities
        except Exception as e:
            print(f"[ERROR] Error labeling ICA components: {e}")
            return None, None
    
    def exclude_non_brain_components(self, exclude_list: List[int] = None):
        """
        Exclude non-brain components and apply ICA to raw data.
        
        Parameters
        ----------
        exclude_list : list, optional
            Indices of components to exclude. If None, auto-excludes non-brain components
            after labeling.
        """
        if self.ica is None:
            print("[ERROR] No ICA model fitted.")
            return
        
        try:
            if exclude_list is None:
                # Auto-exclude non-brain components
                labels, _ = self.auto_label_ica_components()
                if labels:
                    exclude_list = [i for i, label in enumerate(labels) if label not in ("brain", "other")]
            
            self.ica.exclude = exclude_list
            self.ica.apply(self.raw)
            
            print(f"[OK] ICA applied and artifacts removed")
            print(f"  - Excluded components: {exclude_list}")
        except Exception as e:
            print(f"[ERROR] Error excluding components: {e}")
    
    def manually_exclude_components(self, exclude_list: List[int]):
        """
        Manually specify ICA components to exclude and apply.
        
        Parameters
        ----------
        exclude_list : list
            Indices of components to exclude (e.g., [0, 1])
        """
        if self.ica is None:
            print("[ERROR] No ICA model fitted.")
            return
        
        try:
            self.ica.exclude = exclude_list
            self.ica.apply(self.raw)
            
            print(f"[OK] ICA applied with manual exclusion")
            print(f"  - Excluded components: {exclude_list}")
        except Exception as e:
            print(f"[ERROR] Error applying ICA: {e}")
    
    def get_ica_sources(self) -> np.ndarray:
        """
        Get ICA source time series.
        
        Returns
        -------
        np.ndarray
            ICA source data [n_components × n_samples]
        """
        if self.ica is None:
            print("[ERROR] No ICA model fitted.")
            return None
        
        return self.ica.get_sources(self.raw).get_data()
    
    def remove_bad_channels(self, bad_channels: List[str]):
        """
        Mark channels as bad and exclude them from analysis.
        
        Parameters
        ----------
        bad_channels : list
            List of channel names to mark as bad
        """
        try:
            self.raw.info['bads'].extend(bad_channels)
            self.raw.interpolate_bads()
            
            print(f"[OK] Bad channels handled")
            print(f"  - Bad channels: {bad_channels}")
        except Exception as e:
            print(f"[ERROR] Error removing bad channels: {e}")
