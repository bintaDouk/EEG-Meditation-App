# EEG Processor - Modular Python Package

A well-structured, modular Python package for processing BIDS-formatted EEG data. The code from the Jupyter notebook has been refactored into reusable, production-ready modules.

## Overview

This package provides a clean separation of concerns with the following core modules:

### Core Modules

1. **`config.py`** - Configuration management
   - `Config` class for centralized settings
   - BIDS directory validation
   - Processing parameters

2. **`data_loader.py`** - BIDS data loading and setup
   - `DataLoader` class for reading EEG files
   - BIDS structure exploration
   - Channel montage and type configuration
   - Handles subjects, sessions, and tasks

3. **`inspector.py`** - Data inspection and analysis
   - `DataInspector` class for analyzing data properties
   - Summary statistics
   - Channel type analysis
   - Data statistics (min, max, mean, std)

4. **`visualizer.py`** - Visualization and plotting
   - `Visualizer` class for EEG data visualization
   - Raw signal plots
   - Power spectral density (PSD)
   - Channel location plots
   - ICA component visualization
   - Artifact channel plots

5. **`preprocessor.py`** - Preprocessing and artifact removal
   - `Preprocessor` class for data preprocessing
   - Artifact detection (EOG, ECG)
   - Filtering and ICA fitting
   - Automatic component labeling with ICLabel
   - Bad channel handling

## Installation

1. Ensure your `requirements.txt` includes:
```
mne>=1.0
mne-bids>=0.10
mne-icalabel>=0.5
numpy
pandas
matplotlib
```

2. Install the package:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

```python
from eeg_processor import Config, DataLoader, DataInspector, Visualizer, Preprocessor

# 1. Configure
config = Config(bids_root=r"path/to/bids/dataset")

# 2. Load data
loader = DataLoader(config)
loader.explore_bids_structure()
raw = loader.load_first_available()
loader.setup_montage()
loader.set_channel_types({'EXG1': 'eog', 'EXG7': 'ecg'})

# 3. Inspect
inspector = DataInspector(raw)
inspector.print_summary()

# 4. Visualize
visualizer = Visualizer(raw)
visualizer.plot_raw_signals()
visualizer.plot_power_spectral_density()

# 5. Preprocess
preprocessor = Preprocessor(raw)
preprocessor.filter_data(l_freq=1.0, h_freq=40.0)
preprocessor.fit_ica(n_components=20)
preprocessor.exclude_non_brain_components()
visualizer.plot_raw_signals()  # View cleaned data
```

### Detailed Examples

#### Loading Specific Subject Data

```python
from eeg_processor import DataLoader, Config

config = Config(bids_root=r"path/to/dataset")
loader = DataLoader(config)

# Load specific subject/task
raw = loader.load_eeg_data(
    subject='001',
    session='01',
    task='med1breath'
)
loader.setup_montage()
```

#### Full Preprocessing Pipeline

```python
from eeg_processor import Preprocessor

preprocessor = Preprocessor(raw)

# Step 1: Filter
preprocessor.filter_data(l_freq=1.0, h_freq=40.0)

# Step 2: Fit ICA
ica = preprocessor.fit_ica(n_components=20, method='fastica')

# Step 3: Auto-label and remove artifacts
labels, probs = preprocessor.auto_label_ica_components()
preprocessor.exclude_non_brain_components()

# Or manually exclude specific components
preprocessor.manually_exclude_components([0, 1])
```

#### Advanced Visualization

```python
from eeg_processor import Visualizer

visualizer = Visualizer(raw)

# Plot raw signals
visualizer.plot_raw_signals(duration=10, n_channels=64)

# Plot frequency content
visualizer.plot_power_spectral_density(fmin=0.5, fmax=50)

# Plot channel locations
visualizer.plot_channel_locations()

# ICA visualization
visualizer.plot_ica_components(ica)
visualizer.plot_ica_sources(ica)
visualizer.plot_ica_properties(ica, picks=[0, 1])

# Artifact channels
visualizer.plot_artifact_channels(['EXG1', 'EXG2', 'EXG7'])
```

#### Data Inspection

```python
from eeg_processor import DataInspector

inspector = DataInspector(raw)

# Print comprehensive summary
properties = inspector.print_summary()

# Channel information
inspector.print_channel_info()

# Get specific channel types
eeg_channels = inspector.get_channel_names_by_type('eeg')
eog_channels = inspector.get_channel_names_by_type('eog')

# Channel statistics
stats = inspector.get_data_statistics()
```

## Example Script

See `example_main.py` for a complete example workflow demonstrating all modules in sequence.

Run it with:
```bash
python example_main.py
```

## Key Features

✅ **Modular Design** - Clean separation of concerns  
✅ **Reusable Components** - Use modules independently  
✅ **Production-Ready** - Error handling and validation  
✅ **Well-Documented** - Comprehensive docstrings  
✅ **BIDS-Compliant** - Works with standard BIDS datasets  
✅ **Flexible Configuration** - Easily adjustable parameters  
✅ **Artifact Removal** - Automatic and manual ICA options  
✅ **Rich Visualization** - Multiple plotting options  

## Class Reference

### Config
Central configuration management.

**Attributes:**
- `bids_root` (str): Path to BIDS dataset root
- `ica_n_components` (int): Number of ICA components
- `filter_low_hz` (float): Highpass filter cutoff
- `filter_high_hz` (float): Lowpass filter cutoff

**Methods:**
- `get_bids_contents()`: List BIDS directory contents

### DataLoader
Loads and configures BIDS EEG data.

**Methods:**
- `explore_bids_structure()`: List subjects, sessions, tasks
- `load_eeg_data(subject, session, task)`: Load specific file
- `load_first_available()`: Load first subject's data
- `setup_montage(montage_name)`: Configure electrode positions
- `set_channel_types(mapping)`: Configure channel types

### DataInspector
Analyze EEG data properties.

**Methods:**
- `print_summary()`: Print comprehensive summary
- `print_channel_info()`: Print all channel details
- `get_channel_types()`: Get channel type counts
- `get_channel_names_by_type(type)`: Get channels of specific type
- `get_data_statistics()`: Calculate basic statistics

### Visualizer
Create various plots.

**Methods:**
- `plot_raw_signals()`: Plot raw EEG time series
- `plot_power_spectral_density()`: Plot frequency content
- `plot_channel_locations()`: Plot 2D sensor layout
- `plot_ica_components()`: Plot component topomaps
- `plot_ica_sources()`: Plot component time series
- `plot_ica_properties()`: Plot detailed component info
- `plot_artifact_channels()`: Plot EOG/ECG channels

### Preprocessor
Preprocess data and remove artifacts.

**Methods:**
- `filter_data(l_freq, h_freq)`: Apply bandpass filter
- `detect_eog_artifacts()`: Find eye movement artifacts
- `detect_ecg_artifacts()`: Find heartbeat artifacts
- `fit_ica()`: Decompose into independent components
- `auto_label_ica_components()`: Auto-label with ICLabel
- `exclude_non_brain_components()`: Remove non-brain ICA
- `manually_exclude_components(list)`: Manual component rejection
- `get_ica_sources()`: Get ICA source time series
- `remove_bad_channels()`: Interpolate bad channels

## Advantages Over Notebook

1. **Reusability** - Use components in other projects
2. **Testing** - Easier to unit test modular code
3. **Version Control** - Better git integration
4. **Maintainability** - Cleaner, more organized code
5. **Scalability** - Process multiple subjects easily
6. **Documentation** - Comprehensive docstrings
7. **Error Handling** - Robust exception management
8. **Configuration** - Centralized, easy to modify

## Extending the Package

Add new modules as needed:

```python
# Create new_processor.py
from eeg_processor import DataInspector

class PeakDetector(DataInspector):
    def find_peaks(self, threshold=2.0):
        # Implementation
        pass

# Use it
from new_processor import PeakDetector
detector = PeakDetector(raw)
peaks = detector.find_peaks()
```

## Notes

- All modules require MNE-Python and BIDS data in standard format
- Montage defaults to 'biosemi64' for this dataset
- ICA typically uses 20 components; adjust based on your needs
- Filtered data is stored separately; original raw data is preserved
- Error handling provides helpful feedback for troubleshooting

## Support

For issues or questions, refer to:
- MNE Documentation: https://mne.tools/
- BIDS Specification: https://bids-standard.github.io/
