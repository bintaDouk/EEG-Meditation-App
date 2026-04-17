"""EEG power feature extraction (theta and alpha bands)."""

from typing import Dict, Tuple
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq


class EEGPowerExtractor:
    """Extract EEG power features from specific frequency bands and locations."""

    def __init__(self, sampling_rate: int = 500):
        """
        Initialize EEG power extractor.

        Parameters
        ----------
        sampling_rate : int, default=500
            Sampling rate of the EEG signal in Hz
        """
        self.sampling_rate = sampling_rate

    def extract_power_spectrum(
        self, signal_data: np.ndarray, fmin: float, fmax: float
    ) -> float:
        """
        Extract average power in a frequency band using Welch's method.

        Parameters
        ----------
        signal_data : np.ndarray
            Raw signal data
        fmin : float
            Minimum frequency (Hz)
        fmax : float
            Maximum frequency (Hz)

        Returns
        -------
        float
            Average power in the specified frequency band (µV²)
        """
        try:
            # Use Welch's method for PSD estimation
            freqs, psd = signal.welch(
                signal_data,
                fs=self.sampling_rate,
                nperseg=min(512, len(signal_data))
            )

            # Find indices in frequency range
            mask = (freqs >= fmin) & (freqs <= fmax)
            power = np.mean(psd[mask])

            return power
        except Exception as e:
            print(f"Error computing power spectrum: {e}")
            return 0.0

    def extract(self, raw_data: dict) -> Dict[str, float]:
        """
        Extract frontal theta and posterior alpha power.

        Parameters
        ----------
        raw_data : dict
            Dictionary with channel names as keys and signal arrays as values
            Expected channels: Fz, FCz (for theta), Pz, O1, O2 (for alpha)

        Returns
        -------
        dict
            Dictionary with features:
            - frontal_theta: Average power at Fz/FCz in 4-8 Hz band (µV²)
            - posterior_alpha: Average power at Pz/O1/O2 in 8-12 Hz band (µV²)
        """

        # Frontal theta: 4-8 Hz at Fz/FCz
        frontal_channels = ['Fz', 'FCz']
        theta_powers = []

        for ch in frontal_channels:
            if ch in raw_data:
                power = self.extract_power_spectrum(raw_data[ch], fmin=4, fmax=8)
                theta_powers.append(power)

        frontal_theta = np.mean(theta_powers) if theta_powers else 0.0

        # Posterior alpha: 8-12 Hz at Pz/O1/O2
        posterior_channels = ['Pz', 'O1', 'O2']
        alpha_powers = []

        for ch in posterior_channels:
            if ch in raw_data:
                power = self.extract_power_spectrum(raw_data[ch], fmin=8, fmax=12)
                alpha_powers.append(power)

        posterior_alpha = np.mean(alpha_powers) if alpha_powers else 0.0

        return {
            'frontal_theta': frontal_theta,
            'posterior_alpha': posterior_alpha
        }

    def extract_from_raw(self, raw) -> Tuple[Dict[str, float], np.ndarray]:
        """
        Extract power features from MNE Raw object.

        Parameters
        ----------
        raw : mne.io.BaseRaw
            MNE Raw object with EEG data

        Returns
        -------
        tuple
            (features dict, sample data for verification)
        """
        # Define channel groups
        frontal_channels = ['Fz', 'FCz']
        posterior_channels = ['Pz', 'O1', 'O2']
        all_channels = frontal_channels + posterior_channels

        # Prepare data dictionary
        raw_data = {}
        sfreq = int(raw.info['sfreq'])

        for ch in all_channels:
            if ch in raw.ch_names:
                ch_idx = raw.ch_names.index(ch)
                raw_data[ch] = raw.get_data(picks=ch_idx)[0]

        # Extract features
        features = self.extract(raw_data)

        return features, np.array([features['frontal_theta'], features['posterior_alpha']])

    def extract_batch(self, raw_list: list) -> Tuple[np.ndarray, list]:
        """
        Extract features from multiple Raw objects.

        Parameters
        ----------
        raw_list : list
            List of MNE Raw objects

        Returns
        -------
        tuple
            (Feature matrix, list of feature names)
        """
        features_list = []
        feature_names = ['frontal_theta', 'posterior_alpha']

        for raw in raw_list:
            features, _ = self.extract_from_raw(raw)
            features_list.append([features['frontal_theta'], features['posterior_alpha']])

        return np.array(features_list), feature_names
