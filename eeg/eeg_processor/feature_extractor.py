"""HRV feature extraction from ECG signals using neurokit2."""

from typing import Dict, Tuple
import numpy as np
import neurokit2 as nk


class HRVFeatureExtractor:
    """Extract Heart Rate Variability features from ECG signals."""

    def __init__(self, sampling_rate: int = 500):
        """
        Initialize HRV extractor.
        
        Parameters
        ----------
        sampling_rate : int, default=500
            Sampling rate of the ECG signal in Hz
        """
        self.sampling_rate = sampling_rate

    def extract(self, ecg_signal: np.ndarray) -> Dict[str, float]:
        """
        Extract HRV features from ECG signal.
        
        Parameters
        ----------
        ecg_signal : np.ndarray
            Raw ECG signal
        
        Returns
        -------
        dict
            Dictionary containing HRV metrics:
            - hr_mean: Mean heart rate (bpm)
            - rr_mean: Mean RR interval (ms)
            - sdnn: Standard deviation of NN intervals (ms)
            - rmssd: Root mean square of successive differences
            - pnn50: % of successive differences > 50ms
            - lf: Low frequency power (ms²)
            - hf: High frequency power (ms²)
            - lf_hf: LF/HF ratio
            - vlf: Very low frequency power (ms²)
        """
        # Clean and find peaks
        ecg_clean = nk.ecg_clean(ecg_signal, sampling_rate=self.sampling_rate)
        _, rpeaks = nk.ecg_peaks(ecg_clean, sampling_rate=self.sampling_rate)
        
        # Calculate HRV metrics
        hrv = nk.hrv_time(rpeaks, sampling_rate=self.sampling_rate)
        try:
            hrv_freq = nk.hrv_frequency(rpeaks, sampling_rate=self.sampling_rate, method='fft')
        except Exception:
            # Fallback: use time-domain features only
            hrv_freq = None
        
        # Combine metrics
        features = {
            'hr_mean': hrv['HR_Mean'].values[0],
            'rr_mean': hrv['RR_Mean'].values[0],
            'sdnn': hrv['SDNN'].values[0],
            'rmssd': hrv['RMSSD'].values[0],
            'pnn50': hrv['pNN50'].values[0],
        }
        
        if hrv_freq is not None:
            features.update({
                'lf': hrv_freq['HRV_LF'].values[0],
                'hf': hrv_freq['HRV_HF'].values[0],
                'lf_hf': hrv_freq['HRV_LFHF'].values[0],
                'vlf': hrv_freq['HRV_VLF'].values[0],
            })
        
        return features

    def extract_with_interval(
        self, ecg_signal: np.ndarray, duration: int = 60
    ) -> Tuple[Dict[str, float], np.ndarray]:
        """
        Extract HRV features from ECG signal with R-peak times.
        
        Parameters
        ----------
        ecg_signal : np.ndarray
            Raw ECG signal
        duration : int, default=60
            Duration in seconds (for reference)
        
        Returns
        -------
        tuple
            (features dict, rr_intervals array in ms)
        """
        ecg_clean = nk.ecg_clean(ecg_signal, sampling_rate=self.sampling_rate)
        _, rpeaks = nk.ecg_peaks(ecg_clean, sampling_rate=self.sampling_rate)
        
        # Get RR intervals
        rr_intervals = np.diff(rpeaks['ECG_R_Peaks']) / self.sampling_rate * 1000  # Convert to ms
        
        # Extract features
        hrv = nk.hrv_time(rpeaks, sampling_rate=self.sampling_rate)
        hrv_freq = nk.hrv_frequency(rpeaks, sampling_rate=self.sampling_rate, psd_method='welch')
        
        features = {
            'rr_mean': hrv['HRV_MeanNN'].values[0],
            'sdnn': hrv['HRV_SDNN'].values[0],
            'rmssd': hrv['HRV_SDRMSSD'].values[0],
            'pnn50': hrv['HRV_pNN50'].values[0],
            'lf': hrv_freq['HRV_LF'].values[0],
            'hf': hrv_freq['HRV_HF'].values[0],
            'lf_hf': hrv_freq['HRV_LFHF'].values[0],
            'vlf': hrv_freq['HRV_VLF'].values[0],
        }
        
        return features, rr_intervals
