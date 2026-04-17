# EEG Power Classifier: Frontal Theta & Posterior Alpha

## Overview

This classifier distinguishes meditation from active thinking using EEG power features extracted from specific frequency bands and electrode locations. It uses the same FNN architecture as the HRV classifier but with different input features.

## Features Extracted

### 1. Frontal Theta Power (4-8 Hz)
- **Location**: Fz (Frontal midline), FCz (Frontal central)
- **What it represents**: Focused attention/meditation state
- **Why it matters**: Frontal midline theta is the most replicated EEG marker of focused attention meditation and scales with experience level
- **Unit**: µV² (microvolts squared)

### 2. Posterior Alpha Power (8-12 Hz)
- **Location**: Pz (Parietal), O1 (Left occipital), O2 (Right occipital)
- **What it represents**: Reduced visual/sensory processing
- **Why it matters**: Strong in eyes-closed meditation and differentiates from active thinking
- **Unit**: µV² (microvolts squared)

## Architecture

- **Input Features**: 2 (frontal theta, posterior alpha)
- **Hidden Layers**: [32, 16] neurons
- **Output**: 2 classes (Think=0, Meditate=1)
- **Activation**: ReLU
- **Loss**: Cross-Entropy
- **Optimizer**: Adam

## Files

### Core Components
- `eeg_processor/eeg_power_extractor.py` - EEG power feature extraction
- `train_eeg_power_classifier.ipynb` - Training notebook
- `inference_eeg_power.ipynb` - Inference notebook

### Trained Models
- `models/eeg_power_classifier/` - Saved model weights and scaler

## Usage

### Training

```bash
# Run the Jupyter notebook
jupyter notebook train_eeg_power_classifier.ipynb
```

**Steps:**
1. Load med1breath and think1 data for multiple subjects
2. Extract frontal theta and posterior alpha power
3. Train FNN for 100 epochs
4. Evaluate on test set
5. Save model

### Inference

```bash
jupyter notebook inference_eeg_power.ipynb
```

**Steps:**
1. Load trained model
2. Extract power features from new subject
3. Predict with probabilities
4. Visualize features and predictions

### Python API

```python
from eeg_processor import EEGPowerExtractor, HRVClassifier

# Extract features
extractor = EEGPowerExtractor(sampling_rate=500)
features, features_array = extractor.extract_from_raw(raw)
# features = {'frontal_theta': 2.5, 'posterior_alpha': 1.8}

# Load model
classifier = HRVClassifier(input_size=2)
classifier.load('models/eeg_power_classifier')

# Predict
pred_class, pred_probs = classifier.predict_with_proba(features_array.reshape(1, -1))
# pred_class = [1]  -> Meditate
# pred_probs = [[0.15, 0.85]]  -> 15% Think, 85% Meditate
```

## Expected Results

**Typical Performance:**
- Accuracy: 70-85% (varies with subject count and data quality)
- Precision: 70-80% (varies with class balance)
- Recall: 70-80%

**Performance Factors:**
- Better with more subjects (training data)
- Sensitive to EEG signal quality
- Eyes-closed meditation typically has higher alpha, higher theta
- Active thinking typically has lower alpha, variable theta

## Comparisons

### vs HRV Classifier
| Aspect | HRV (ECG) | EEG Power |
|--------|-----------|-----------|
| Input | Heart rate variability | Brain oscillations |
| Channels | 1 (ECG) | 5 (EEG) |
| Features | 8 (RR intervals, frequency bands) | 2 (Theta, Alpha) |
| Sensitivity | Whole-body physiology | Brain state |
| Training Time | Faster | Slower (more data processing) |
| Meditation Specificity | Moderate | High (known EEG markers) |

## Implementation Details

### Power Calculation
Uses Welch's method (scipy.signal.welch) for robust PSD estimation:
- Window: 512 samples (or signal length if shorter)
- Overlap: Default (50%)
- Frequency resolution: ~1 Hz

### Channel Mapping
```python
EXG channels (from the 68-channel system):
- EXG1-4: EOG (eye movement) - not used for power
- EXG5-6: Mastoid reference - not used for power
- EXG7: ECG - not used for power
- EXG8: GSR - not used for power

EEG channels used:
- Fz, FCz: Frontal theta extraction
- Pz, O1, O2: Posterior alpha extraction
```

## Troubleshooting

### Low Accuracy
1. Check that subjects have adequate data (~2 minutes per task)
2. Verify signal quality (check for artifacts)
3. Ensure electrodes Fz/FCz and Pz/O1/O2 are properly connected
4. Try increasing training epochs
5. Collect more subjects

### Missing Channels
If a channel is missing:
- Frontal theta: Falls back to available channel (Fz or FCz)
- Posterior alpha: Falls back to available channels (Pz, O1, or O2)
- If no channels available: Returns 0.0 power

### Feature Saturation
If theta and alpha values are very high (>50 µV²):
- Check for muscle artifact
- Reduce window length in extractor
- Verify channel impedances

## Next Steps

1. **Combine Features**: Use both HRV and EEG power features in one classifier
2. **Add More Bands**: Include delta (0-4 Hz), beta (12-30 Hz), gamma (30+ Hz)
3. **Temporal Features**: Extract features from moving windows (time-series classification)
4. **Source Localization**: Use ICA to identify independent brain components
5. **Real-time Classification**: Stream processing during meditation session

## References

**Frontal Theta:**
- Heuvel, M. P. van den, & Pol, H. E. H. (2010). Exploring the brain network...
- Lomas, D. J., et al. (2015). A rapid, reliable measure of frontal alpha asymmetry...

**Posterior Alpha:**
- Bazalgette, P. L., et al. (1992). Habituation of evoked potentials...
- Klimesch, W. (1999). EEG alpha and theta oscillations reflect cognitive and memory performance...
