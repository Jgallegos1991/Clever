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

class BackupManager:
    def __init__(self, project_path, keep_latest=1):
import config

import config


class BackupManager:
    """
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
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
 main
        self.project_path = Path(project_path).expanduser()
        self.backup_dir = self.project_path / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.keep_latest = keep_latest

    def create_backup(self):
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
    def create_backup(self):
        """
        Create a timestamped ZIP backup of the entire project directory.
        
        Why: Preserves complete project state including databases, configuration,
             and source code to enable recovery from data corruption or loss.
        Where: Called by backup automation or manual backup processes to
               create point-in-time snapshots of Clever AI state.
        How: Generates timestamp-based filename, creates ZIP archive with
             compression, recursively includes all files except backup directory.

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
 main
        """
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = self.backup_dir / backup_name

        # Zip project folder
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.project_path):
                # Skip backups folder itself
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

        # Clean old backups
        self.cleanup_old_backups()

    def cleanup_old_backups(self):
        
        # Maintain retention policy
        self.cleanup_old_backups()
        return backup_path

 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
    def cleanup_old_backups(self):
        """
        Remove old backup files based on retention policy configuration.
        
        Why: Manages disk space usage by automatically removing outdated
             backups while preserving the most recent ones for recovery.
        Where: Called after successful backup creation to maintain clean
               backup directory with configurable retention limits.
        How: Lists backup files by modification time, keeps most recent
             files up to retention limit, deletes older archives.

    def cleanup_old_backups(self) -> None:
        """
        Remove old backup files beyond retention policy limit.
        
        Why: Prevents unlimited backup accumulation that would consume disk
             space while maintaining recent backups for recovery needs.
        
        Where: Called automatically after backup creation and by maintenance
               scripts to enforce storage policies and prevent disk issues.
        
        How: Lists backup files sorted by modification time, identifies excess
             backups beyond keep_latest limit, and removes older files safely.
 main
        """
        backups = sorted(self.backup_dir.glob("backup_*.zip"), key=os.path.getmtime, reverse=True)
        if len(backups) > self.keep_latest:
            for old_backup in backups[self.keep_latest:]:
                old_backup.unlink()
                print(f"Deleted old backup: {old_backup}")

if __name__ == "__main__":
    bm = BackupManager(project_path="~/Projects/Jordans_AI_Base", keep_latest=1)

if __name__ == "__main__":
 copilot/fix-cc2a9f5a-a710-4e20-9fec-adba0964457f
    bm = BackupManager(project_path=config.ROOT_DIR, keep_latest=1)

    # Default backup configuration using centralized settings
    bm = BackupManager(keep_latest=3)
 main
    bm.create_backup()
