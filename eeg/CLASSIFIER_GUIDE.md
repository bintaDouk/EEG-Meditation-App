# Meditation vs Thinking Task Classifier

## Overview

This guide demonstrates how to train and use a neural network classifier to distinguish between meditation and thinking tasks based on Heart Rate Variability (HRV) features extracted from ECG signals.

## Architecture

The classification pipeline consists of:

1. **Data Loading**: Multi-subject EEG data loading from BIDS format
2. **Feature Extraction**: HRV feature extraction from ECG (EXG7) channel
3. **Preprocessing**: Standardization of features using scikit-learn
4. **Model Training**: Simple Fully Connected Neural Network (FNN) in PyTorch
5. **Inference**: Predictions with class labels and probability estimates

## Components

### 1. HRVClassifier (`eeg_processor/classifier.py`)

Main classifier class with the following methods:

- `train()` - Train the model with training/validation data
- `predict()` - Get class predictions
- `predict_with_proba()` - Get class predictions with probabilities
- `save()` / `load()` - Model persistence

### 2. SimpleFFN (`eeg_processor/classifier.py`)

PyTorch neural network with configurable architecture:
- Input layer: 8 features (HRV metrics)
- Hidden layers: [64, 32] neurons (default, configurable)
- Dropout: 0.3 (default, reduces overfitting)
- Output layer: 2 classes (Think=0, Meditate=1)
- Activation: ReLU
- Loss: Cross-Entropy
- Optimizer: Adam

### 3. HRVDataset (`eeg_processor/classifier.py`)

PyTorch Dataset wrapper for HRV features and labels.

## HRV Features

Extracted from ECG signal using neurokit2:

1. **rr_mean** - Mean RR interval (ms)
2. **sdnn** - Standard deviation of NN intervals (ms)
3. **rmssd** - Root mean square of successive differences
4. **pnn50** - Percentage of successive differences > 50ms
5. **lf** - Low frequency power (ms²)
6. **hf** - High frequency power (ms²)
7. **lf_hf** - LF/HF ratio
8. **vlf** - Very low frequency power (ms²)

## Usage

### 1. Training

```bash
cd eeg
python train_classifier.py
```

**What it does:**
- Loads up to 10 subjects (configurable via `max_subjects`)
- Extracts HRV features for:
  - **think1** task (Class 0 - Think)
  - **meditate1** task (Class 1 - Meditate)
- Splits data: 80% train, 10% val, 10% test
- Trains FNN for 100 epochs
- Evaluates on test set
- Saves model to `models/meditation_classifier/`

**Output:**
- Training/validation loss and accuracy
- Test metrics: Accuracy, Precision, Recall, F1-Score
- Example predictions with probabilities
- Saved model files:
  - `model.pt` - Trained weights
  - `scaler_mean.npy` / `scaler_scale.npy` - Feature standardization
  - `metadata.json` - Feature names and metadata

### 2. Inference

```bash
cd eeg
python inference.py
```

**What it does:**
- Loads trained model from `models/meditation_classifier/`
- Makes predictions for first 3 subjects
- Returns class label and probabilities

**Output format:**
```
Subject 01:
Predicted class:      Meditate (1)
Probabilities:
  - Think:    0.1766
  - Meditate: 0.8234
Confidence:           0.8234
```

## Example: Custom Inference

```python
from eeg_processor import Config, DataLoader, HRVFeatureExtractor, HRVClassifier
import numpy as np
from pathlib import Path

# Load trained model
classifier = HRVClassifier(input_size=8)
classifier.load('models/meditation_classifier')

# Load subject data
loader = DataLoader(config)
raw = loader.load_eeg_data('01', session=None, task=None)

# Extract HRV features
extractor = HRVFeatureExtractor(sampling_rate=int(raw.info['sfreq']))
ecg_idx = raw.ch_names.index('EXG7')
ecg_signal = raw.get_data(picks=ecg_idx)[0]
features, _ = extractor.extract_with_interval(ecg_signal)

# Make prediction
X = np.array([list(features.values())])
pred_class, pred_probs = classifier.predict_with_proba(X)

print(f"Class: {'Think' if pred_class[0] == 0 else 'Meditate'}")
print(f"Think probability:    {pred_probs[0][0]:.4f}")
print(f"Meditate probability: {pred_probs[0][1]:.4f}")
```

## Customization

### Modify Training Parameters

Edit `train_classifier.py`:

```python
# Number of subjects to load
max_subjects = 10

# Train/val/test split
train_size, val_size, test_size = 0.7, 0.15, 0.15

# Model architecture
hidden_sizes = [128, 64, 32]

# Training
epochs = 200
batch_size = 8
learning_rate = 0.001
```

### Different Task Combinations

To classify different tasks, modify in `train_classifier.py`:

```python
MEDITATE_TASK = 'meditate1'  # or 'meditate2'
THINK_TASK = 'think1'         # or 'think2'
```

### Model Architecture

Modify in `train_classifier.py`:

```python
classifier = HRVClassifier(
    input_size=8,
    hidden_sizes=[256, 128, 64],  # Custom layers
    learning_rate=0.0005,
    device='cuda'  # Use GPU if available
)
```

## Files

- `eeg_processor/classifier.py` - Core classifier implementation
- `train_classifier.py` - Training pipeline
- `inference.py` - Inference script
- `models/meditation_classifier/` - Saved trained model

## Notes

- The classifier currently uses a binary classification (Meditate vs Think)
- HRV features work best with good quality ECG signals
- Training with more subjects generally improves performance
- Model is saved with feature standardizer for consistent inference
- GPU support available (automatically detected)

## Next Steps

1. Train the model: `python train_classifier.py`
2. Run inference: `python inference.py`
3. Experiment with different task combinations
4. Add more features (e.g., EEG power bands) for better performance
5. Try multi-class classification (all 4 tasks)
