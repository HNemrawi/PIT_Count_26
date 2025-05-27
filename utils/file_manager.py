"""
File management for temporary storage of uploaded files.
Prevents memory issues while maintaining sheet re-selection functionality.
"""

import tempfile
import os
from pathlib import Path
import pickle
from datetime import datetime, timedelta
from io import BytesIO
import streamlit as st
import uuid

class FileManager:
    """Manages temporary file storage for uploaded files"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "pit_count_uploads"
        self.temp_dir.mkdir(exist_ok=True)
        self._cleanup_old_files()
    
    def _cleanup_old_files(self, hours=24):
        """Remove files older than specified hours"""
        try:
            cutoff = datetime.now() - timedelta(hours=hours)
            for file in self.temp_dir.glob("*.pkl"):
                if datetime.fromtimestamp(file.stat().st_mtime) < cutoff:
                    file.unlink()
        except Exception as e:
            # Don't fail if cleanup has issues
            pass
    
    def save_file(self, file_content: bytes, source_name: str, session_id: str) -> str:
        """Save file content to temp storage"""
        file_path = self.temp_dir / f"{session_id}_{source_name}.pkl"
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(file_content, f)
            return str(file_path)
        except Exception as e:
            raise Exception(f"Failed to save file: {str(e)}")
    
    def load_file(self, file_path: str) -> BytesIO:
        """Load file buffer from temp storage"""
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            return BytesIO(data)
        except Exception as e:
            raise Exception(f"Failed to load file: {str(e)}")
    
    def delete_file(self, file_path: str):
        """Delete temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except:
            pass  # Don't fail if deletion has issues
    
    def delete_session_files(self, session_id: str):
        """Delete all files for a session"""
        try:
            for file in self.temp_dir.glob(f"{session_id}_*.pkl"):
                file.unlink()
        except:
            pass