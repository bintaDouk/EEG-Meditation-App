"""
Inference script for the meditation vs thinking classifier.

This script demonstrates how to:
1. Load a trained model
2. Extract HRV features from new EEG data
3. Make predictions with class labels and probabilities
"""

import numpy as np
import os
from pathlib import Path
from dotenv import load_dotenv

from eeg_processor import Config, DataLoader, HRVFeatureExtractor, HRVClassifier

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


def make_predictions_for_subject(subject_id: str, classifier: HRVClassifier, config: Config):
    """
    Load a subject's data and make predictions for meditation vs thinking.

    Parameters
    ----------
    subject_id : str
        Subject ID to load
    classifier : HRVClassifier
        Trained classifier
    config : Config
        Configuration object
    """
    print(f"\n{'=' * 70}")
    print(f"PREDICTIONS FOR SUBJECT {subject_id}")
    print(f"{'=' * 70}\n")

    # Load data
    loader = DataLoader(config)
    raw = loader.load_eeg_data(subject_id, session=None, task=None)

    if raw is None:
        print(f"[ERROR] Could not load data for subject {subject_id}")
        return

    # Set up channels
    loader.setup_montage(montage_name='biosemi64', on_missing='ignore')
    channel_type_mapping = {
        'EXG1': 'eog', 'EXG2': 'eog', 'EXG3': 'eog', 'EXG4': 'eog',
        'EXG5': 'misc', 'EXG6': 'misc', 'EXG7': 'ecg'
    }
    loader.set_channel_types(channel_type_mapping)

    # Extract HRV features
    try:
        ecg_idx = raw.ch_names.index('EXG7')
        ecg_signal = raw.get_data(picks=ecg_idx)[0]

        extractor = HRVFeatureExtractor(sampling_rate=int(raw.info['sfreq']))
        features, _ = extractor.extract_with_interval(ecg_signal)

        # Convert to array format for prediction
        X = np.array([list(features.values())])

        # Make prediction with probabilities
        pred_class, pred_probs = classifier.predict_with_proba(X)

        class_name = "Think" if pred_class[0] == 0 else "Meditate"
        think_prob = pred_probs[0][0]
        meditate_prob = pred_probs[0][1]
        confidence = max(pred_probs[0])

        print(f"Subject: {subject_id}")
        print(f"Predicted class:      {class_name} ({pred_class[0]})")
        print(f"Probabilities:")
        print(f"  - Think:    {think_prob:.4f}")
        print(f"  - Meditate: {meditate_prob:.4f}")
        print(f"Confidence:           {confidence:.4f}")
        print()

        return {
            'subject_id': subject_id,
            'predicted_class': class_name,
            'class_idx': pred_class[0],
            'think_probability': think_prob,
            'meditate_probability': meditate_prob,
            'confidence': confidence
        }

    except Exception as e:
        print(f"[ERROR] Could not extract features: {e}")
        return None


def main():
    """Main inference pipeline."""

    print("\n" + "=" * 70)
    print("MEDITATION CLASSIFIER - INFERENCE")
    print("=" * 70)

    # Initialize config
    config = Config(
        bids_root=os.getenv('BIDS_ROOT'),
        random_seed=42
    )

    # Load trained model
    model_dir = Path(__file__).parent / 'models' / 'meditation_classifier'

    if not model_dir.exists():
        print(f"\n[ERROR] Model not found at {model_dir}")
        print("Please train the model first using train_classifier.py")
        return

    classifier = HRVClassifier(input_size=8)
    classifier.load(str(model_dir))
    print(f"[OK] Model loaded from {model_dir}\n")

    # Make predictions for multiple subjects
    loader = DataLoader(config)
    loader.explore_bids_structure()

    results = []
    for subject_id in loader.subjects[:3]:  # Predict for first 3 subjects
        result = make_predictions_for_subject(subject_id, classifier, config)
        if result:
            results.append(result)

    # Summary
    if results:
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70 + "\n")

        for result in results:
            print(f"Subject {result['subject_id']}: "
                  f"{result['predicted_class']} "
                  f"(Confidence: {result['confidence']:.4f})")

        print()


if __name__ == "__main__":
    main()
