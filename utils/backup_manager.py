import os
from pathlib import Path
import shutil
import time
import zipfile
import config

class BackupManager:
    """
    Automated backup system for Clever AI project files and databases.
    
    Why: Provides data protection and recovery capabilities for Clever AI's
         local databases, configuration, and project files to prevent data loss.
    Where: Used by backup automation processes and manual backup operations
           to maintain safe copies of the entire project state.
    How: Creates timestamped ZIP archives of the project directory, excludes
         backup folder from recursion, maintains configurable retention policy.
    """
    
    def __init__(self, project_path, keep_latest=1):
        """
        Initialize backup manager with project path and retention policy.
        
        Why: Sets up backup configuration and ensures backup directory exists
             for storing compressed project archives.
        Where: Called when backup operations are initiated, typically from
               scheduled processes or manual backup triggers.
        How: Creates backup directory structure, expands user paths,
             configures retention count for automatic cleanup.
        
        Args:
            project_path: Path to the project root directory to backup
            keep_latest: Number of most recent backups to retain (default: 1)
        """
        self.project_path = Path(project_path).expanduser()
        self.backup_dir = self.project_path / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.keep_latest = keep_latest

    def create_backup(self):
        """
        Create a timestamped ZIP backup of the entire project directory.
        
        Why: Preserves complete project state including databases, configuration,
             and source code to enable recovery from data corruption or loss.
        Where: Called by backup automation or manual backup processes to
               create point-in-time snapshots of Clever AI state.
        How: Generates timestamp-based filename, creates ZIP archive with
             compression, recursively includes all files except backup directory.
        """
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = self.backup_dir / backup_name

        # Zip project folder
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.project_path):
                # Skip backups folder itself
                if str(self.backup_dir) in root:
                    continue
                for file in files:
                    file_path = Path(root) / file
                    zipf.write(file_path, arcname=file_path.relative_to(self.project_path))

        print(f"Backup created: {backup_path}")

        # Clean old backups
        self.cleanup_old_backups()

    def cleanup_old_backups(self):
        """
        Remove old backup files based on retention policy configuration.
        
        Why: Manages disk space usage by automatically removing outdated
             backups while preserving the most recent ones for recovery.
        Where: Called after successful backup creation to maintain clean
               backup directory with configurable retention limits.
        How: Lists backup files by modification time, keeps most recent
             files up to retention limit, deletes older archives.
        """
        backups = sorted(self.backup_dir.glob("backup_*.zip"), key=os.path.getmtime, reverse=True)
        if len(backups) > self.keep_latest:
            for old_backup in backups[self.keep_latest:]:
                old_backup.unlink()
                print(f"Deleted old backup: {old_backup}")

if __name__ == "__main__":
    bm = BackupManager(project_path=config.ROOT_DIR, keep_latest=1)
    bm.create_backup()
