"""
Training pipeline for meditation vs thinking task classifier using HRV features.

This script:
1. Loads multiple subjects' data for specific tasks (meditate1 and think1)
2. Extracts HRV features from ECG signals
3. Trains a simple FNN classifier
4. Evaluates on test set with probabilities
"""

import numpy as np
import os
from pathlib import Path
from dotenv import load_dotenv

from eeg_processor import (
    Config, DataLoader, Preprocessor, HRVFeatureExtractor, HRVClassifier
)

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Task mapping
TASK_NAMES = ['meditate1', 'meditate2', 'think1', 'think2']
MEDITATE_TASK = 'meditate1'  # Task index 0
THINK_TASK = 'think1'        # Task index 2


def extract_hrv_features_for_task(
    raw,
    task_name: str,
    ecg_channel: str = 'EXG7',
    sampling_rate: int = 500
) -> dict:
    """
    Extract HRV features for a specific task.

    Parameters
    ----------
    raw : mne.io.BaseRaw
        Loaded raw EEG data
    task_name : str
        Name of the task for logging
    ecg_channel : str
        Name of ECG channel
    sampling_rate : int
        Sampling rate in Hz

    Returns
    -------
    dict
        Dictionary with HRV features
    """
    try:
        ecg_idx = raw.ch_names.index(ecg_channel)
        ecg_signal = raw.get_data(picks=ecg_idx)[0]

        extractor = HRVFeatureExtractor(sampling_rate=sampling_rate)
        features, _ = extractor.extract_with_interval(ecg_signal)

        return features
    except Exception as e:
        print(f"  [WARNING] Could not extract HRV for {task_name}: {e}")
        return None


def main():
    """Main training pipeline."""

    print("\n" + "=" * 70)
    print("MEDITATION VS THINKING CLASSIFIER - TRAINING PIPELINE")
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
    print()

    # ─────────────────────────────────────────────────────────────
    # 2. DATA LOADING
    # ─────────────────────────────────────────────────────────────
    print("2. LOADING DATA FOR MULTIPLE SUBJECTS")
    print("-" * 70)

    loader = DataLoader(config)
    loader.explore_bids_structure()

    # Load first 10 subjects (or adjust as needed)
    max_subjects = 10
    loaded_data, failed = loader.load_multiple_subjects(
        session=None,
        task=None,
        max_subjects=max_subjects
    )

    if not loaded_data:
        print("\n[ERROR] Could not load any subjects. Exiting.")
        return

    print(f"[OK] Loaded {len(loaded_data)} subjects\n")

    # ─────────────────────────────────────────────────────────────
    # 3. FEATURE EXTRACTION FOR SPECIFIC TASKS
    # ─────────────────────────────────────────────────────────────
    print("3. EXTRACTING HRV FEATURES")
    print("-" * 70)

    all_features = []
    all_labels = []
    feature_names = ['rr_mean', 'sdnn', 'rmssd', 'pnn50', 'lf', 'hf', 'lf_hf', 'vlf']

    for subject_id, raw in loaded_data.items():
        print(f"\nSubject {subject_id}:")

        # Set up electrode montage and channel types (from main.py)
        loader.raw = raw  # Temporarily set for setup methods
        loader.setup_montage(montage_name='biosemi64', on_missing='ignore')

        channel_type_mapping = {
            'EXG1': 'eog', 'EXG2': 'eog', 'EXG3': 'eog', 'EXG4': 'eog',
            'EXG5': 'misc', 'EXG6': 'misc', 'EXG7': 'ecg'
        }
        loader.set_channel_types(channel_type_mapping)

        # Extract HRV for meditate1 task
        meditate_features = extract_hrv_features_for_task(raw, MEDITATE_TASK)
        if meditate_features:
            print(f"  ✓ {MEDITATE_TASK}: {list(meditate_features.keys())}")
            all_features.append(list(meditate_features.values()))
            all_labels.append(1)  # Label 1 for meditate

        # Extract HRV for think1 task
        think_features = extract_hrv_features_for_task(raw, THINK_TASK)
        if think_features:
            print(f"  ✓ {THINK_TASK}: {list(think_features.keys())}")
            all_features.append(list(think_features.values()))
            all_labels.append(0)  # Label 0 for think

    X = np.array(all_features)
    y = np.array(all_labels)

    print(f"\n[OK] Extracted features for {len(X)} samples")
    print(f"  - Shape: {X.shape}")
    print(f"  - Classes: {np.bincount(y)}")
    print(f"  - Think (0): {np.sum(y == 0)}, Meditate (1): {np.sum(y == 1)}\n")

    # ─────────────────────────────────────────────────────────────
    # 4. DATA SPLITTING
    # ─────────────────────────────────────────────────────────────
    print("4. SPLITTING DATA")
    print("-" * 70)

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )

    print(f"Train: {X_train.shape[0]} samples")
    print(f"Val:   {X_val.shape[0]} samples")
    print(f"Test:  {X_test.shape[0]} samples\n")

    # ─────────────────────────────────────────────────────────────
    # 5. MODEL TRAINING
    # ─────────────────────────────────────────────────────────────
    print("5. TRAINING CLASSIFIER")
    print("-" * 70)

    classifier = HRVClassifier(
        input_size=X_train.shape[1],
        hidden_sizes=[64, 32],
        learning_rate=0.001
    )

    history = classifier.train(
        X_train, y_train,
        X_val, y_val,
        epochs=100,
        batch_size=16,
        feature_names=feature_names
    )

    print()

    # ─────────────────────────────────────────────────────────────
    # 6. MODEL EVALUATION
    # ─────────────────────────────────────────────────────────────
    print("6. EVALUATING MODEL")
    print("-" * 70)

    test_predictions, test_probs = classifier.predict_with_proba(X_test)

    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    accuracy = accuracy_score(y_test, test_predictions)
    precision = precision_score(y_test, test_predictions)
    recall = recall_score(y_test, test_predictions)
    f1 = f1_score(y_test, test_predictions)

    print(f"Test Accuracy:  {accuracy:.4f}")
    print(f"Test Precision: {precision:.4f}")
    print(f"Test Recall:    {recall:.4f}")
    print(f"Test F1-Score:  {f1:.4f}\n")

    # ─────────────────────────────────────────────────────────────
    # 7. INFERENCE EXAMPLES
    # ─────────────────────────────────────────────────────────────
    print("7. INFERENCE EXAMPLES (WITH PROBABILITIES)")
    print("-" * 70)

    print("\nSample predictions from test set:\n")
    for i in range(min(5, len(X_test))):
        pred_class = test_predictions[i]
        pred_prob = test_probs[i]
        true_class = y_test[i]

        class_name = "Think" if pred_class == 0 else "Meditate"
        true_name = "Think" if true_class == 0 else "Meditate"

        print(f"Sample {i+1}:")
        print(f"  True class:       {true_name} ({true_class})")
        print(f"  Predicted class:  {class_name} ({pred_class})")
        print(f"  Probability:      Think={pred_prob[0]:.4f}, Meditate={pred_prob[1]:.4f}")
        print(f"  Confidence:       {max(pred_prob):.4f}\n")

    # ─────────────────────────────────────────────────────────────
    # 8. SAVE MODEL
    # ─────────────────────────────────────────────────────────────
    print("8. SAVING MODEL")
    print("-" * 70)

    model_dir = Path(__file__).parent / 'models' / 'med_think_hrv_classifier'
    classifier.save(str(model_dir))
    print(f"[OK] Model saved to {model_dir}\n")

    # ─────────────────────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────────────────────
    print("=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print(f"\nModel Performance:")
    print(f"  - Accuracy:  {accuracy:.4f}")
    print(f"  - Precision: {precision:.4f}")
    print(f"  - Recall:    {recall:.4f}")
    print(f"  - F1-Score:  {f1:.4f}")
    print(f"\nModel saved to: {model_dir}")
    print()


if __name__ == "__main__":
    main()
