"""
Backup Manager Module - Automated backup system for Clever AI project files.

Why: Provides reliable data protection through automated backup creation and
     retention management, ensuring project continuity and recovery capability
     while maintaining efficient storage usage through cleanup policies.

Where: Used by scheduled backup processes, deployment systems, and manual
       backup operations to protect Clever AI data and configuration.

How: Implements ZIP-based backup creation with timestamp naming, automatic
     cleanup of old backups, and configurable retention policies.
"""
import os
from pathlib import Path
import shutil
import time
import zipfile

import config


class BackupManager:
    """
    Automated backup system with ZIP compression and retention management.
    
    Why: Provides systematic data protection for Clever AI with efficient
         storage usage and automated cleanup to prevent disk space issues.
    
    Where: Used by backup schedulers, deployment scripts, and maintenance
           tools to ensure consistent data protection policies.
    
    How: Creates ZIP archives with timestamp naming, manages retention through
         configurable keep_latest parameter, and excludes backup directory
         from recursive backups to prevent storage waste.
    """
    
    def __init__(self, project_path: str | Path | None = None, keep_latest: int = 1):
        """
        Initialize backup manager with project path and retention policy.
        
        Why: Sets up backup system with configurable location and retention
             to support different deployment scenarios and storage constraints.
        
        Where: Called during backup system initialization or by scheduled
               backup processes that need specific retention policies.
        
        How: Resolves project path using config defaults if not specified,
             creates backup directory structure, and stores retention settings.
        """
        if project_path is None:
            project_path = config.ROOT_DIR
        self.project_path = Path(project_path).expanduser()
        self.backup_dir = self.project_path / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.keep_latest = keep_latest

    def create_backup(self) -> Path:
        """
        Create compressed backup of entire project with timestamp naming.
        
        Why: Provides point-in-time project snapshot for recovery, deployment
             rollback, or data migration with efficient compression.
        
        Where: Called by scheduled backup jobs, deployment processes, and
               manual backup operations when data protection is needed.
        
        How: Creates ZIP archive with timestamp naming, walks project directory
             recursively while excluding backup folder, and triggers cleanup.
        
        Returns:
            Path: Location of created backup file
        """
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = self.backup_dir / backup_name

        # Create ZIP archive of project folder
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.project_path):
                # Skip backups folder to prevent recursive inclusion
                if str(self.backup_dir) in root:
                    continue
                for file in files:
                    file_path = Path(root) / file
                    zipf.write(file_path, arcname=file_path.relative_to(self.project_path))

        print(f"Backup created: {backup_path}")
        
        # Maintain retention policy
        self.cleanup_old_backups()
        return backup_path

    def cleanup_old_backups(self) -> None:
        """
        Remove old backup files beyond retention policy limit.
        
        Why: Prevents unlimited backup accumulation that would consume disk
             space while maintaining recent backups for recovery needs.
        
        Where: Called automatically after backup creation and by maintenance
               scripts to enforce storage policies and prevent disk issues.
        
        How: Lists backup files sorted by modification time, identifies excess
             backups beyond keep_latest limit, and removes older files safely.
        """
        backups = sorted(self.backup_dir.glob("backup_*.zip"), key=os.path.getmtime, reverse=True)
        if len(backups) > self.keep_latest:
            for old_backup in backups[self.keep_latest:]:
                old_backup.unlink()
                print(f"Deleted old backup: {old_backup}")


if __name__ == "__main__":
    # Default backup configuration using centralized settings
    bm = BackupManager(keep_latest=3)
    bm.create_backup()
