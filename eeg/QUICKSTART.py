"""
Quick reference guide for using the EEG processor package.
"""

# ────────────────────────────────────────────────────────────────
# QUICK START - 5 MINUTES TO YOUR FIRST ANALYSIS
# ────────────────────────────────────────────────────────────────

# 1. IMPORT
from eeg_processor import Config, DataLoader, DataInspector, Visualizer, Preprocessor

# 2. CONFIGURE
config = Config(bids_root=r"path/to/ds003969")

# 3. LOAD
loader = DataLoader(config)
raw = loader.load_first_available()
loader.setup_montage()
loader.set_channel_types({
    'EXG1': 'eog', 'EXG2': 'eog', 'EXG3': 'eog', 'EXG4': 'eog',
    'EXG5': 'misc', 'EXG6': 'misc', 'EXG7': 'ecg'
})

# 4. INSPECT
inspector = DataInspector(raw)
inspector.print_summary()

# 5. VISUALIZE
visualizer = Visualizer(raw)
visualizer.plot_raw_signals(duration=10)
visualizer.plot_power_spectral_density()

# 6. PREPROCESS
preprocessor = Preprocessor(raw)
preprocessor.filter_data(l_freq=1.0, h_freq=40.0)
preprocessor.fit_ica(n_components=20)
preprocessor.exclude_non_brain_components()

# 7. VIEW RESULTS
visualizer.plot_raw_signals()  # Clean data


# ────────────────────────────────────────────────────────────────
# COMMON TASKS
# ────────────────────────────────────────────────────────────────

# Task 1: Load specific subject/task
raw = loader.load_eeg_data(subject='001', session='01', task='med1breath')

# Task 2: See what's available
bids_info = loader.explore_bids_structure()
print(bids_info)

# Task 3: Manually exclude specific ICA components
preprocessor.manually_exclude_components([0, 1, 2])

# Task 4: Get ICA source signals
sources = preprocessor.get_ica_sources()

# Task 5: Remove bad channels
preprocessor.remove_bad_channels(['Cz', 'Pz'])

# Task 6: Get detailed channel info
eeg_channels = inspector.get_channel_names_by_type('eeg')
stats = inspector.get_data_statistics()

# Task 7: Plot artifact channels
visualizer.plot_artifact_channels(['EXG1', 'EXG2', 'EXG7'])

# Task 8: Detect artifacts without ICA
eog_epochs = preprocessor.detect_eog_artifacts(ch_name='EXG1')
ecg_epochs = preprocessor.detect_ecg_artifacts(ch_name='EXG7')

# Task 9: Filter without ICA
preprocessor.filter_data(l_freq=0.5, h_freq=50)

# Task 10: Get raw MNE data structure
mne_raw = loader.raw  # For direct MNE-Python operations


# ────────────────────────────────────────────────────────────────
# WORKFLOW TEMPLATES
# ────────────────────────────────────────────────────────────────

# WORKFLOW A: Minimal preprocessing
# Suitable for: Quick inspection and visualization
def minimal_workflow(bids_root):
    config = Config(bids_root=bids_root)
    loader = DataLoader(config)
    raw = loader.load_first_available()
    loader.setup_montage()
    
    inspector = DataInspector(raw)
    inspector.print_summary()
    
    visualizer = Visualizer(raw)
    visualizer.plot_raw_signals()
    visualizer.plot_power_spectral_density()
    
    return raw


# WORKFLOW B: ICA-based cleaning
# Suitable for: Artifact removal with automatic detection
def ica_workflow(bids_root):
    config = Config(bids_root=bids_root)
    loader = DataLoader(config)
    raw = loader.load_first_available()
    loader.setup_montage()
    loader.set_channel_types({
        'EXG1': 'eog', 'EXG7': 'ecg'
    })
    
    preprocessor = Preprocessor(raw)
    preprocessor.filter_data()
    preprocessor.fit_ica()
    preprocessor.exclude_non_brain_components()
    
    visualizer = Visualizer(raw)
    visualizer.plot_raw_signals()
    
    return raw, preprocessor.ica


# WORKFLOW C: Manual inspection and selection
# Suitable for: Careful artifact inspection and manual component selection
def manual_inspection_workflow(bids_root):
    config = Config(bids_root=bids_root)
    loader = DataLoader(config)
    raw = loader.load_first_available()
    loader.setup_montage()
    loader.set_channel_types({
        'EXG1': 'eog', 'EXG7': 'ecg'
    })
    
    visualizer = Visualizer(raw)
    visualizer.plot_raw_signals()
    visualizer.plot_artifact_channels(['EXG1', 'EXG7'])
    
    preprocessor = Preprocessor(raw)
    preprocessor.filter_data()
    preprocessor.fit_ica()
    
    # Inspect ICA components
    visualizer.plot_ica_components(preprocessor.ica)
    visualizer.plot_ica_sources(preprocessor.ica)
    
    # User manually selects components to exclude
    # Modify this based on inspection
    preprocessor.manually_exclude_components([0, 1])
    
    visualizer.plot_raw_signals()
    
    return raw, preprocessor.ica


# WORKFLOW D: Full analysis with all steps
# Suitable for: Complete analysis pipeline
def full_workflow(bids_root, subject=None, session=None, task=None):
    config = Config(bids_root=bids_root)
    loader = DataLoader(config)
    
    # Explore structure
    bids_info = loader.explore_bids_structure()
    
    # Load data
    if subject:
        raw = loader.load_eeg_data(subject, session, task)
    else:
        raw = loader.load_first_available()
    
    # Configure
    loader.setup_montage()
    loader.set_channel_types({
        'EXG1': 'eog', 'EXG2': 'eog', 'EXG3': 'eog', 'EXG4': 'eog',
        'EXG5': 'misc', 'EXG6': 'misc', 'EXG7': 'ecg'
    })
    
    # Inspect
    inspector = DataInspector(raw)
    properties = inspector.print_summary()
    
    # Visualize raw
    visualizer = Visualizer(raw)
    visualizer.plot_raw_signals()
    visualizer.plot_power_spectral_density()
    visualizer.plot_channel_locations()
    
    # Detect artifacts
    preprocessor = Preprocessor(raw)
    eog_epochs = preprocessor.detect_eog_artifacts()
    ecg_epochs = preprocessor.detect_ecg_artifacts()
    
    # Preprocess
    preprocessor.filter_data()
    preprocessor.fit_ica()
    
    # Visualize ICA
    visualizer.plot_ica_components(preprocessor.ica)
    visualizer.plot_ica_sources(preprocessor.ica)
    
    # Clean
    preprocessor.exclude_non_brain_components()
    
    # Visualize cleaned
    visualizer.plot_raw_signals()
    visualizer.plot_power_spectral_density()
    
    return raw, preprocessor.ica, properties


# ────────────────────────────────────────────────────────────────
# TIPS & TRICKS
# ────────────────────────────────────────────────────────────────

# Tip 1: Access MNE objects directly
raw = loader.raw  # mne.io.Raw object
ica = preprocessor.ica  # mne.preprocessing.ICA object
# Use any MNE methods: raw.filter(), ica.apply(), etc.

# Tip 2: Save and reload data
raw.save('cleaned_eeg.fif', overwrite=True)
import mne
raw = mne.io.read_raw_fif('cleaned_eeg.fif')

# Tip 3: Extract epochs around events
events, event_ids = mne.events_from_annotations(raw)
epochs = mne.Epochs(raw, events, event_ids, tmin=-0.5, tmax=2.0)

# Tip 4: Compute ERPs
evoked = epochs['med1breath'].average()
evoked.plot()

# Tip 5: Frequency analysis
spectrum = raw.compute_psd()
spectrum.plot([10, 40])

# Tip 6: Source localization (requires head model)
# See MNE documentation for forward model, inverse, etc.

# Tip 7: Loop through multiple subjects
for subject in ['001', '002', '003']:
    raw = loader.load_eeg_data(subject=subject)
    # Process...

# Tip 8: Save preprocessing parameters
import json
config_dict = {
    'filter_low': config.filter_low_hz,
    'filter_high': config.filter_high_hz,
    'ica_components': config.ica_n_components
}
with open('preprocessing_config.json', 'w') as f:
    json.dump(config_dict, f)
