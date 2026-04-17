"""
Data inspection module for analyzing EEG data properties.
"""

from typing import Dict, List
import mne


class DataInspector:
    """Provides methods to inspect and analyze EEG data properties."""
    
    def __init__(self, raw: mne.io.BaseRaw):
        """
        Initialize DataInspector with raw EEG data.
        
        Parameters
        ----------
        raw : mne.io.BaseRaw
            The raw EEG data to inspect
        """
        self.raw = raw
    
    def print_summary(self) -> Dict:
        """
        Print and return comprehensive EEG data properties summary.
        
        Returns
        -------
        dict
            Dictionary containing data properties
        """
        if self.raw is None:
            print("[ERROR] No raw data loaded")
            return {}
        
        info = self.raw.info
        data_shape = self.raw.get_data().shape
        
        properties = {
            'sampling_frequency': info['sfreq'],
            'num_channels': len(info['ch_names']),
            'channel_names': info['ch_names'],
            'duration_seconds': self.raw.times[-1],
            'duration_minutes': self.raw.times[-1] / 60,
            'num_samples': data_shape[1],
            'data_shape': data_shape,
            'channel_types': self.get_channel_types()
        }
        
        print("=" * 70)
        print("EEG DATA SUMMARY")
        print("=" * 70)
        print(f"Sampling frequency: {properties['sampling_frequency']} Hz")
        print(f"Number of channels: {properties['num_channels']}")
        print(f"Channel names: {properties['channel_names']}")
        print(f"Recording duration: {properties['duration_seconds']:.2f} s ({properties['duration_minutes']:.2f} min)")
        print(f"Total samples: {properties['num_samples']}")
        print(f"Data shape (channels × samples): {properties['data_shape']}")
        
        print("\n" + "=" * 70)
        print("CHANNEL INFORMATION")
        print("=" * 70)
        for ch_type, count in properties['channel_types'].items():
            print(f"{ch_type.upper()}: {count} channel(s)")
        
        return properties
    
    def get_channel_types(self) -> Dict[str, int]:
        """
        Get count of channels by type.
        
        Returns
        -------
        dict
            Dictionary mapping channel types to counts
        """
        ch_types_dict = {}
        for ch_type in self.raw.get_channel_types():
            if ch_type not in ch_types_dict:
                ch_types_dict[ch_type] = 0
            ch_types_dict[ch_type] += 1
        
        return ch_types_dict
    
    def get_channel_names_by_type(self, ch_type: str) -> List[str]:
        """
        Get all channel names of a specific type.
        
        Parameters
        ----------
        ch_type : str
            Channel type (e.g., 'eeg', 'eog', 'ecg')
        
        Returns
        -------
        list
            Channel names of the specified type
        """
        picks = mne.pick_types(self.raw.info, **{ch_type: True})
        return [self.raw.info['ch_names'][i] for i in picks]
    
    def get_data_statistics(self) -> Dict:
        """
        Calculate basic statistics of the EEG data.
        
        Returns
        -------
        dict
            Dictionary containing min, max, mean, std for each channel type
        """
        import numpy as np
        
        stats = {}
        for ch_type in self.raw.get_channel_types():
            picks = mne.pick_types(self.raw.info, **{ch_type: True})
            if len(picks) > 0:
                data = self.raw.get_data(picks=picks)
                stats[ch_type] = {
                    'min': np.min(data),
                    'max': np.max(data),
                    'mean': np.mean(data),
                    'std': np.std(data)
                }
        
        return stats
    
    def print_channel_info(self):
        """Print detailed information about all channels."""
        print("\n" + "=" * 70)
        print("DETAILED CHANNEL INFORMATION")
        print("=" * 70)
        
        for i, ch_name in enumerate(self.raw.info['ch_names']):
            ch_info = self.raw.info['chs'][i]
            ch_type = ch_info.get('kind', 'unknown')
            print(f"{i+1:2d}. {ch_name:20s} | Type: {ch_type}")
