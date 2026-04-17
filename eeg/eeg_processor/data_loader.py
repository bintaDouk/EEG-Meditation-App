"""
Data loading module for BIDS EEG data.
"""

from typing import Optional, List, Tuple
import mne
from mne_bids import BIDSPath, read_raw_bids, get_entity_vals
from .config import Config


class DataLoader:
    """Handles loading and basic setup of BIDS EEG data."""
    
    def __init__(self, config: Config):
        """
        Initialize DataLoader with configuration.
        
        Parameters
        ----------
        config : Config
            Configuration object containing BIDS root path and parameters.
        """
        self.config = config
        self.raw = None
        self.subjects = None
        self.sessions = None
        self.tasks = None
    
    def explore_bids_structure(self) -> dict:
        """
        Explore and list available entities in the BIDS dataset.
        
        Returns
        -------
        dict
            Dictionary containing subjects, sessions, and tasks.
        """
        try:
            self.subjects = get_entity_vals(self.config.bids_root, entity_key='subject')
            self.sessions = get_entity_vals(self.config.bids_root, entity_key='session') or []
            self.tasks = get_entity_vals(self.config.bids_root, entity_key='task') or []
            
            print(f"[OK] BIDS structure explored successfully")
            print(f"  - Subjects: {len(self.subjects)} ({self.subjects})")
            print(f"  - Sessions: {len(self.sessions)} ({self.sessions if self.sessions else 'None'})")
            print(f"  - Tasks: {len(self.tasks)} ({self.tasks})")
            
            return {
                'subjects': self.subjects,
                'sessions': self.sessions,
                'tasks': self.tasks
            }
        except Exception as e:
            print(f"[ERROR] Error exploring BIDS structure: {e}")
            return {}
    
    def load_eeg_data(
        self,
        subject: str,
        session: Optional[str] = None,
        task: Optional[str] = None,
        verbose: bool = False
    ) -> Optional[mne.io.BaseRaw]:
        """
        Load EEG data from a specific subject/session/task.
        
        Parameters
        ----------
        subject : str
            Subject identifier (e.g., '001')
        session : str, optional
            Session identifier
        task : str, optional
            Task identifier
        verbose : bool, default=False
            Verbosity level for MNE operations
        
        Returns
        -------
        mne.io.BaseRaw or None
            Loaded raw EEG data, or None if loading failed.
        """
        try:
            bids_path = BIDSPath(
                subject=subject,
                session=session,
                task=task,
                datatype='eeg',
                root=self.config.bids_root
            )
            
            print(f"Loading BIDS file: {bids_path}")
            self.raw = read_raw_bids(bids_path=bids_path, verbose=verbose)
            
            print(f"[OK] Successfully loaded EEG data")
            print(f"  - Shape: {self.raw.get_data().shape}")
            
            return self.raw
        
        except Exception as e:
            print(f"[ERROR] Error reading EEG data: {e}")
            return None
    
    def setup_montage(self, montage_name: str = 'biosemi64', on_missing: str = 'ignore'):
        """
        Set up electrode montage for the loaded data.
        
        Parameters
        ----------
        montage_name : str, default='biosemi64'
            Name of standard montage to use
        on_missing : str, default='ignore'
            How to handle missing channels ('raise', 'warn', 'ignore')
        """
        if self.raw is None:
            print("[ERROR] No raw data loaded. Load data first using load_eeg_data()")
            return
        
        try:
            montage = mne.channels.make_standard_montage(montage_name)
            self.raw.set_montage(montage, on_missing=on_missing)
            print(f"[OK] Montage '{montage_name}' set successfully")
        except Exception as e:
            print(f"[ERROR] Error setting montage: {e}")
    
    def set_channel_types(self, channel_type_mapping: dict):
        """
        Set custom channel types for auxiliary channels.
        
        Parameters
        ----------
        channel_type_mapping : dict
            Dictionary mapping channel names to types (e.g., {'EXG1': 'eog'})
        """
        if self.raw is None:
            print("[ERROR] No raw data loaded.")
            return
        
        try:
            self.raw.set_channel_types(channel_type_mapping)
            print(f"[OK] Channel types updated: {len(channel_type_mapping)} channels")
        except Exception as e:
            print(f"[ERROR] Error setting channel types: {e}")
    
    def load_first_available(self) -> Optional[mne.io.BaseRaw]:
        """
        Load the first available subject/task combination.
        
        Returns
        -------
        mne.io.BaseRaw or None
            Loaded raw EEG data for the first available subject.
        """
        if not self.subjects:
            self.explore_bids_structure()
        
        if not self.subjects:
            print("[ERROR] No subjects found in BIDS dataset")
            return None
        
        subject = self.subjects[0]
        session = self.sessions[0] if self.sessions else None
        task = self.tasks[0] if self.tasks else None
        
        return self.load_eeg_data(subject, session, task)
