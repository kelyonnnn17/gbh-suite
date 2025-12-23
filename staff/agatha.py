import os
import shutil
import datetime
import zipfile

# --- CONFIGURATION ---
ARCHIVE_DIR = os.path.expanduser("~/Documents/Archives")
BACKUP_DIR = os.path.expanduser("~/Documents/Backups/Dotfiles")

# Folders to IGNORE when packing a project
BLACKLIST = [
    "node_modules", 
    "venv", 
    ".venv", 
    "env", 
    "__pycache__", 
    ".git", 
    ".DS_Store", 
    "dist", 
    "build"
]

class Agatha:
    def __init__(self):
        # Ensure destination folders exist
        if not os.path.exists(ARCHIVE_DIR):
            os.makedirs(ARCHIVE_DIR)
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

    def log(self, msg):
        print(f"🧁 {msg}")

    # --- JOB 1: SMART PROJECT ARCHIVING ---
    def pack_project(self, source_path):
        source_path = os.path.abspath(source_path)
        project_name = os.path.basename(source_path)
        
        # Timestamp: project_2023-10-27.zip
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        zip_name = f"{project_name}_{timestamp}.zip"
        zip_path = os.path.join(ARCHIVE_DIR, zip_name)
        
        self.log(f"Baking a Mendl's Box for: {project_name}")
        self.log(f"Excluding junk: {', '.join(BLACKLIST)}")

        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_path):
                    # Modify dirs in-place to skip blacklisted folders
                    dirs[:] = [d for d in dirs if d not in BLACKLIST]
                    
                    for file in files:
                        if file in BLACKLIST: continue
                        
                        file_path = os.path.join(root, file)
                        # Calculate path relative to the source folder
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)
            
            # Check size
            size_mb = os.path.getsize(zip_path) / (1024 * 1024)
            self.log(f"Done! Archive saved to: {zip_path}")
            self.log(f"Final Size: {size_mb:.2f} MB")
            
        except Exception as e:
            print(f"❌ Error packing project: {e}")

    # --- JOB 2: DOTFILE BACKUP ---
    def backup_config(self):
        """Backs up .zshrc, .ssh/config, etc."""
        files_to_save = [
            "~/.zshrc",
            "~/.gitconfig",
            "~/.ssh/config",
            "~/.vimrc",
            # Add other config files here
        ]
        
        self.log("Backing up critical configuration files...")
        
        for path in files_to_save:
            full_path = os.path.expanduser(path)
            if os.path.exists(full_path):
                dest = os.path.join(BACKUP_DIR, os.path.basename(path))
                shutil.copy2(full_path, dest)
                print(f"   ✅ Saved: {os.path.basename(path)}")
            else:
                print(f"   ⚠️  Skipped (Not found): {path}")
        
        self.log(f"Configs secured in {BACKUP_DIR}")