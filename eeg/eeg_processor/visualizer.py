"""
Visualization module for plotting EEG data.
"""

import matplotlib.pyplot as plt
import mne


class Visualizer:
    """Methods for visualizing EEG data in various formats."""
    
    def __init__(self, raw: mne.io.BaseRaw, plot_style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize Visualizer with raw EEG data.
        
        Parameters
        ----------
        raw : mne.io.BaseRaw
            The raw EEG data to visualize
        plot_style : str, default='seaborn-v0_8-darkgrid'
            Matplotlib style to use
        """
        self.raw = raw
        self.plot_style = plot_style
        plt.style.use(self.plot_style)
    
    def plot_raw_signals(self, duration: float = 10, n_channels: int = 64):
        """
        Plot raw EEG signals.
        
        Parameters
        ----------
        duration : float, default=10
            Duration in seconds to plot
        n_channels : int, default=64
            Number of channels to display
        """
        if self.raw is None:
            print("[ERROR] No raw data loaded")
            return
        
        eeg_signal = self.raw.copy().pick(mne.pick_types(self.raw.info, eeg=True, exclude='bads'))
        
        fig = eeg_signal.plot(duration=duration, n_channels=n_channels, scalings='auto')
        plt.suptitle('EEG Signals - Raw Data', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_power_spectral_density(self, fmin: float = 0.5, fmax: float = 50):
        """
        Plot power spectral density (PSD) of EEG signals.
        
        Parameters
        ----------
        fmin : float, default=0.5
            Minimum frequency in Hz
        fmax : float, default=50
            Maximum frequency in Hz
        """
        if self.raw is None:
            print("[ERROR] No raw data loaded")
            return
        
        eeg_signal = self.raw.copy().pick(mne.pick_types(self.raw.info, eeg=True, exclude='bads'))
        
        fig = eeg_signal.compute_psd(fmin=fmin, fmax=fmax, n_jobs=1).plot()
        plt.suptitle('Power Spectral Density (PSD) - EEG Signals', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_channel_locations(self):
        """Plot 2D projection of electrode locations."""
        if self.raw is None:
            print("[ERROR] No raw data loaded")
            return
        
        eeg_signal = self.raw.copy().pick(mne.pick_types(self.raw.info, eeg=True, exclude='bads'))
        
        try:
            fig = eeg_signal.plot_sensors()
            plt.suptitle('EEG Channel Locations', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"[ERROR] Could not plot channel locations: {e}")
    
    def plot_ica_components(self, ica: mne.preprocessing.ICA):
        """
        Plot ICA component topomaps.
        
        Parameters
        ----------
        ica : mne.preprocessing.ICA
            Fitted ICA object
        """
        try:
            ica.plot_components()
            plt.suptitle('ICA Components - Topomaps', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"[ERROR] Error plotting ICA components: {e}")
    
    def plot_ica_sources(self, ica: mne.preprocessing.ICA, duration: float = 10):
        """
        Plot ICA source time series.
        
        Parameters
        ----------
        ica : mne.preprocessing.ICA
            Fitted ICA object
        duration : float, default=10
            Duration in seconds to plot
        """
        try:
            ica.plot_sources(self.raw, duration=duration)
            plt.suptitle('ICA Sources - Time Series', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"[ERROR] Error plotting ICA sources: {e}")
    
    def plot_ica_properties(self, ica: mne.preprocessing.ICA, picks: list = None):
        """
        Plot detailed ICA component properties.
        
        Parameters
        ----------
        ica : mne.preprocessing.ICA
            Fitted ICA object
        picks : list, optional
            Component indices to plot (default: [0, 1])
        """
        if picks is None:
            picks = [0, 1]
        
        try:
            ica.plot_properties(self.raw, picks=picks)
            plt.suptitle('ICA Component Properties', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"[ERROR] Error plotting ICA properties: {e}")
    
    def plot_artifact_channels(self, artifact_channel_names: list):
        """
        Plot auxiliary/artifact channels (EOG, ECG, etc.).
        
        Parameters
        ----------
        artifact_channel_names : list
            Names of artifact channels to plot
        """
        try:
            artifact_signal = self.raw.copy().pick(artifact_channel_names)
            artifact_signal.plot()
            plt.suptitle('Artifact Channels (EOG, ECG, etc.)', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"[ERROR] Error plotting artifact channels: {e}")
