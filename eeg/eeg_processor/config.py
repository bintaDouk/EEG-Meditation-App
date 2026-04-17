"""
Configuration module for EEG processing setup.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class for EEG data processing settings."""
    
    bids_root: str
    random_seed: int = 42
    plot_style: str = 'seaborn-v0_8-darkgrid'
    
    # Preprocessing parameters
    ica_n_components: int = 20
    ica_method: str = 'fastica'
    filter_low_hz: float = 1.0
    filter_high_hz: float = 40.0
    
    # Visualization parameters
    plot_duration: float = 10  # seconds
    num_channels_plot: int = 64
    psd_fmin: float = 0.5
    psd_fmax: float = 50.0
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not os.path.isdir(self.bids_root):
            raise ValueError(f"BIDS root directory not found: {self.bids_root}")
        print(f"[OK] Configuration initialized with BIDS root: {self.bids_root}")
    
    def get_bids_contents(self) -> list:
        """Get list of contents in BIDS root directory."""
        return os.listdir(self.bids_root)
