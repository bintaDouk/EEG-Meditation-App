"""Neural network classifier for EEG meditation task classification."""

from typing import Dict, Tuple, List, Optional
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader as TorchDataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json
from pathlib import Path


class HRVDataset(Dataset):
    """PyTorch dataset for HRV features."""

    def __init__(self, features: np.ndarray, labels: np.ndarray):
        """
        Initialize HRV dataset.

        Parameters
        ----------
        features : np.ndarray
            Feature matrix (n_samples, n_features)
        labels : np.ndarray
            Label vector (n_samples,)
        """
        self.features = torch.FloatTensor(features)
        self.labels = torch.LongTensor(labels)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.features[idx], self.labels[idx]


class SimpleFFN(nn.Module):
    """Simple Fully Connected Neural Network for binary classification."""

    def __init__(self, input_size: int, hidden_sizes: List[int] = None, dropout: float = 0.3):
        """
        Initialize FFN.

        Parameters
        ----------
        input_size : int
            Number of input features
        hidden_sizes : list of int, optional
            Hidden layer sizes. Default: [64, 32]
        dropout : float, default=0.3
            Dropout rate
        """
        super().__init__()

        if hidden_sizes is None:
            hidden_sizes = [64, 32]

        layers = []
        prev_size = input_size

        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_size = hidden_size

        layers.append(nn.Linear(prev_size, 2))

        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


class HRVClassifier:
    """Classifier for meditation vs thinking tasks using HRV features."""

    def __init__(
        self,
        input_size: int = 8,
        hidden_sizes: List[int] = None,
        learning_rate: float = 0.001,
        device: str = None
    ):
        """
        Initialize classifier.

        Parameters
        ----------
        input_size : int, default=8
            Number of input features
        hidden_sizes : list of int, optional
            Hidden layer sizes
        learning_rate : float, default=0.001
            Learning rate for optimizer
        device : str, optional
            Device to use ('cpu' or 'cuda'). Auto-detected if None.
        """
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.device = device
        self.model = SimpleFFN(input_size, hidden_sizes).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.CrossEntropyLoss()
        self.scaler = StandardScaler()
        self.feature_names = None

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        epochs: int = 50,
        batch_size: int = 16,
        feature_names: Optional[List[str]] = None
    ) -> Dict[str, List[float]]:
        """
        Train the classifier.

        Parameters
        ----------
        X_train : np.ndarray
            Training features (n_samples, n_features)
        y_train : np.ndarray
            Training labels (n_samples,)
        X_val : np.ndarray, optional
            Validation features
        y_val : np.ndarray, optional
            Validation labels
        epochs : int, default=50
            Number of training epochs
        batch_size : int, default=16
            Batch size
        feature_names : list of str, optional
            Names of features for logging

        Returns
        -------
        dict
            Training history with 'train_loss', 'val_loss', 'train_acc', 'val_acc'
        """
        self.feature_names = feature_names

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val) if X_val is not None else None

        train_dataset = HRVDataset(X_train_scaled, y_train)
        train_loader = TorchDataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        history = {
            'train_loss': [],
            'val_loss': [],
            'train_acc': [],
            'val_acc': []
        }

        self.model.train()
        for epoch in range(epochs):
            # Training
            train_loss = 0.0
            train_correct = 0
            train_total = 0

            for features, labels in train_loader:
                features = features.to(self.device)
                labels = labels.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(features)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                train_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                train_total += labels.size(0)
                train_correct += (predicted == labels).sum().item()

            train_loss /= len(train_loader)
            train_acc = train_correct / train_total

            history['train_loss'].append(train_loss)
            history['train_acc'].append(train_acc)

            # Validation
            if X_val_scaled is not None:
                val_loss, val_acc = self._evaluate(X_val_scaled, y_val)
                history['val_loss'].append(val_loss)
                history['val_acc'].append(val_acc)

                if (epoch + 1) % 10 == 0:
                    print(f"Epoch {epoch+1}/{epochs} - "
                          f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
                          f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            else:
                if (epoch + 1) % 10 == 0:
                    print(f"Epoch {epoch+1}/{epochs} - "
                          f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")

        return history

    def _evaluate(self, X: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """Evaluate model on validation set."""
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            y_tensor = torch.LongTensor(y).to(self.device)

            outputs = self.model(X_tensor)
            loss = self.criterion(outputs, y_tensor).item()

            _, predicted = torch.max(outputs.data, 1)
            acc = (predicted == y_tensor).sum().item() / len(y)

        self.model.train()
        return loss, acc

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels.

        Parameters
        ----------
        X : np.ndarray
            Features (n_samples, n_features)

        Returns
        -------
        np.ndarray
            Predicted class labels (n_samples,)
        """
        self.model.eval()
        with torch.no_grad():
            X_scaled = self.scaler.transform(X)
            X_tensor = torch.FloatTensor(X_scaled).to(self.device)
            outputs = self.model(X_tensor)
            _, predicted = torch.max(outputs.data, 1)

        return predicted.cpu().numpy()

    def predict_with_proba(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict class labels with probabilities.

        Parameters
        ----------
        X : np.ndarray
            Features (n_samples, n_features)

        Returns
        -------
        tuple
            (predicted_labels, probabilities)
            - predicted_labels: Class labels (0 or 1)
            - probabilities: Probability of each class (n_samples, 2)
        """
        self.model.eval()
        with torch.no_grad():
            X_scaled = self.scaler.transform(X)
            X_tensor = torch.FloatTensor(X_scaled).to(self.device)
            outputs = self.model(X_tensor)
            probs = torch.softmax(outputs, dim=1)
            _, predicted = torch.max(probs, 1)

        return predicted.cpu().numpy(), probs.cpu().numpy()

    def save(self, path: str):
        """Save model and scaler."""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        torch.save(self.model.state_dict(), path / 'model.pt')
        np.save(path / 'scaler_mean.npy', self.scaler.mean_)
        np.save(path / 'scaler_scale.npy', self.scaler.scale_)

        metadata = {
            'input_size': self.model.network[0].in_features,
            'feature_names': self.feature_names
        }
        with open(path / 'metadata.json', 'w') as f:
            json.dump(metadata, f)

    def load(self, path: str):
        """Load model and scaler."""
        path = Path(path)

        self.model.load_state_dict(torch.load(path / 'model.pt', map_location=self.device))
        self.scaler.mean_ = np.load(path / 'scaler_mean.npy')
        self.scaler.scale_ = np.load(path / 'scaler_scale.npy')

        with open(path / 'metadata.json', 'r') as f:
            metadata = json.load(f)
            self.feature_names = metadata.get('feature_names')
