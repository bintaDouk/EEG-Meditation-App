"""
EEG Data Processor Package

A modular framework for loading, inspecting, and preprocessing BIDS-formatted EEG data.
"""

__version__ = "0.1.0"
__author__ = "EEG Lab"

from .config import Config
from .data_loader import DataLoader
from .inspector import DataInspector
from .visualizer import Visualizer
from .preprocessor import Preprocessor
from .feature_extractor import HRVFeatureExtractor

__all__ = [
    "Config",
    "DataLoader",
    "DataInspector",
    "Visualizer",
    "Preprocessor",
    "HRVFeatureExtractor",
]
