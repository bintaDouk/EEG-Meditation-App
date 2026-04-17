"""
Main example script demonstrating the usage of the EEG processing pipeline.

This script shows how to use the modular EEG processing components to:
1. Load BIDS EEG data
2. Inspect data properties
3. Visualize raw signals
4. Preprocess data (filtering, ICA)
5. Remove artifacts
"""

import numpy as np
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Verify the environment variable is loaded
if not os.getenv('BIDS_ROOT'):
    print(f"WARNING: BIDS_ROOT not found in .env file at {env_path}")
    print(f"Checked file exists: {env_path.exists()}")

# Import EEG processing modules
from eeg_processor import Config, DataLoader, DataInspector, Visualizer, Preprocessor, HRVFeatureExtractor


def main():
    """
    Main execution function demonstrating the complete EEG processing pipeline.
    """
    
    print("\n" + "=" * 70)
    print("EEG DATA PROCESSING PIPELINE")
    print("=" * 70 + "\n")
    
    # ─────────────────────────────────────────────────────────────
    # 1. CONFIGURATION
    # ─────────────────────────────────────────────────────────────
    print("1. INITIALIZING CONFIGURATION")
    print("-" * 70)
    
    config = Config(
        bids_root=os.getenv('BIDS_ROOT'),
        random_seed=42,
        ica_n_components=20,
        ica_method='fastica',
        filter_low_hz=1.0,
        filter_high_hz=40.0,
        psd_fmin=0.5,
        psd_fmax=50.0
    )
    
    bids_contents = config.get_bids_contents()
    print(f"BIDS directory contents: {bids_contents}\n")
    
    # ─────────────────────────────────────────────────────────────
    # 2. DATA EXPLORATION
    # ─────────────────────────────────────────────────────────────
    print("2. EXPLORING BIDS DATASET STRUCTURE")
    print("-" * 70)
    
    loader = DataLoader(config)
    bids_info = loader.explore_bids_structure()
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 3. DATA LOADING
    # ─────────────────────────────────────────────────────────────
    print("3. LOADING EEG DATA")
    print("-" * 70)
    
    raw = loader.load_first_available()
    if raw is None:
        print("\nERROR: Could not load data. Exiting.")
        return
    
    # Set up electrode montage and channel types
    loader.setup_montage(montage_name='biosemi64', on_missing='ignore')
    
    # Configure auxiliary channels (EOG, ECG)
    channel_type_mapping = {
        'EXG1': 'eog',  # left eye corner
        'EXG2': 'eog',  # right eye corner
        'EXG3': 'eog',  # left eye eyebrow (above)
        'EXG4': 'eog',  # left eye below
        'EXG5': 'misc', # left mastoid
        'EXG6': 'misc', # right mastoid
        'EXG7': 'ecg'   # middle of collar bone (ECG approximation)
    }
    loader.set_channel_types(channel_type_mapping)
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 4. DATA INSPECTION
    # ─────────────────────────────────────────────────────────────
    print("4. INSPECTING DATA PROPERTIES")
    print("-" * 70)
    
    inspector = DataInspector(raw)
    properties = inspector.print_summary()
    inspector.print_channel_info()
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 5. VISUALIZATION (BEFORE PREPROCESSING)
    # ─────────────────────────────────────────────────────────────
    print("5. VISUALIZING RAW DATA")
    print("-" * 70)
    
    visualizer = Visualizer(raw, plot_style='seaborn-v0_8-darkgrid')
    
    print("Plotting raw EEG signals...")
    visualizer.plot_raw_signals(duration=config.plot_duration, n_channels=config.num_channels_plot)
    
    print("Plotting power spectral density...")
    visualizer.plot_power_spectral_density(fmin=config.psd_fmin, fmax=config.psd_fmax)
    
    print("Plotting channel locations...")
    visualizer.plot_channel_locations()
    
    print("Plotting artifact channels (EOG, ECG)...")
    artifact_channels = ['EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6', 'EXG7']
    visualizer.plot_artifact_channels(artifact_channels)
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 6. PREPROCESSING - ARTIFACT DETECTION
    # ─────────────────────────────────────────────────────────────
    print("6. DETECTING NATURAL ARTIFACTS")
    print("-" * 70)
    
    preprocessor = Preprocessor(raw)
    
    print("Detecting EOG (eye movement) artifacts...")
    eog_epochs = preprocessor.detect_eog_artifacts(ch_name='EXG1')
    
    print("Detecting ECG (heartbeat) artifacts...")
    ecg_epochs = preprocessor.detect_ecg_artifacts(ch_name='EXG7')
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 7. PREPROCESSING - FILTERING
    # ─────────────────────────────────────────────────────────────
    print("7. FILTERING DATA")
    print("-" * 70)
    
    filt_raw = preprocessor.filter_data(
        l_freq=config.filter_low_hz,
        h_freq=config.filter_high_hz,
        method='iir'
    )
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 8. PREPROCESSING - ICA FITTING
    # ─────────────────────────────────────────────────────────────
    print("8. FITTING ICA MODEL")
    print("-" * 70)


    
    ica = preprocessor.fit_ica(
        n_components=config.ica_n_components,
        method=config.ica_method,
        random_state=config.random_seed,
        use_filtered=True
    )
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 9. VISUALIZATION - ICA COMPONENTS
    # ─────────────────────────────────────────────────────────────
    print("9. VISUALIZING ICA COMPONENTS")
    print("-" * 70)
    
    print("Plotting ICA component topomaps...")
    visualizer.plot_ica_components(ica)
    
    print("Plotting ICA source time series...")
    visualizer.plot_ica_sources(ica, duration=10)
    
    print("Plotting ICA component properties (components 0-1)...")
    visualizer.plot_ica_properties(ica, picks=[0, 1])
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 10. PREPROCESSING - AUTO-LABELING & EXCLUSION
    # ─────────────────────────────────────────────────────────────
    print("10. AUTO-LABELING AND EXCLUDING NON-BRAIN COMPONENTS")
    print("-" * 70)
    
    labels, probabilities = preprocessor.auto_label_ica_components()
    preprocessor.exclude_non_brain_components()
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 11. HRV FEATURE EXTRACTION
    # ─────────────────────────────────────────────────────────────
    print("11. EXTRACTING HRV FEATURES")
    print("-" * 70)
    
    try:
        # Extract ECG channel
        ecg_idx = raw.ch_names.index('EXG7')
        ecg_signal = raw.get_data(picks=ecg_idx)[0]
        
        # Extract HRV features
        hrv_extractor = HRVFeatureExtractor(sampling_rate=int(raw.info['sfreq']))
        hrv_features, rr_intervals = hrv_extractor.extract_with_interval(ecg_signal)
        
        print(f"[OK] HRV features extracted")
        print(f"  - RR Interval (mean): {hrv_features['rr_mean']:.2f} ms")
        print(f"  - SDNN: {hrv_features['sdnn']:.2f} ms")
        print(f"  - RMSSD: {hrv_features['rmssd']:.2f} ms")
        print(f"  - pNN50: {hrv_features['pnn50']:.2f}%")
        print(f"  - LF/HF Ratio: {hrv_features['lf_hf']:.2f}")
        print(f"  - HF Power: {hrv_features['hf']:.2f} ms²")
        print(f"  - LF Power: {hrv_features['lf']:.2f} ms²")
        print(f"  - VLF Power: {hrv_features['vlf']:.2f} ms²")
    except Exception as e:
        print(f"[WARNING] Could not extract HRV features: {e}")
    
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 12. VISUALIZATION - CLEANED DATA
    # ─────────────────────────────────────────────────────────────
    print("12. VISUALIZING CLEANED DATA")
    print("-" * 70)
    
    print("Plotting cleaned EEG signals...")
    visualizer.plot_raw_signals(duration=config.plot_duration, n_channels=config.num_channels_plot)
    print()
    
    # ─────────────────────────────────────────────────────────────
    # 12. SUMMARY
    # ─────────────────────────────────────────────────────────────
    print("=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)
    print(f"\nFinal data shape: {raw.get_data().shape}")
    print(f"ICA components excluded: {ica.exclude}")
    print(f"Processing successfully completed!")
    print()


if __name__ == "__main__":
    main()
