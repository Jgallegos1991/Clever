import os
from pathlib import Path
import shutil
import time
import zipfile

class BackupManager:
    def __init__(self, project_path, keep_latest=1):
        self.project_path = Path(project_path).expanduser()
        self.backup_dir = self.project_path / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.keep_latest = keep_latest

    def create_backup(self):
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
        backups = sorted(self.backup_dir.glob("backup_*.zip"), key=os.path.getmtime, reverse=True)
        if len(backups) > self.keep_latest:
            for old_backup in backups[self.keep_latest:]:
                old_backup.unlink()
                print(f"Deleted old backup: {old_backup}")

if __name__ == "__main__":
    bm = BackupManager(project_path="~/Projects/Jordans_AI_Base", keep_latest=1)
    bm.create_backup()
