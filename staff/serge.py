import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
SOURCE_DIR = os.path.expanduser("~/Downloads")
PROJECTS_DIR = os.path.expanduser("~/Documents/Projects")

DESTINATIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".heic", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".csv", ".xlsx", ".epub"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
    "Installers": [".dmg", ".pkg", ".app"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".sql", ".sh", ".json", ".ipynb"]
}

EMOJI_MAP = {
    "Images": "🖼️", "Documents": "📝", "Audio": "🎵", "Video": "🎥",
    "Archives": "📦", "Installers": "💿", "Code": "💻", "Others": "📂"
}

# --- LOGIC ---
def send_notification(title, message):
    try:
        safe_msg = message.replace('"', '\\"')
        safe_title = title.replace('"', '\\"')
        os.system(f"""osascript -e 'display notification "{safe_msg}" with title "{safe_title}"'""")
    except Exception:
        pass

def make_unique(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f"{filename}({counter}){extension}"
        counter += 1
    return path

class SmartSorter(FileSystemEventHandler):
    def on_created(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event, is_move=True)

    def process(self, event, is_move=False):
        file_path = event.dest_path if is_move else event.src_path
        
        if not os.path.exists(file_path):
            return

        if os.path.isdir(file_path): return
        if os.path.isdir(file_path): return

        filename = os.path.basename(file_path)
        if filename == ".DS_Store" or filename.startswith("."): return
        if filename.endswith((".tmp", ".crdownload", ".part")): return

        # Identify Category
        category = "Others"
        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        for cat, exts in DESTINATIONS.items():
            if extension in exts:
                category = cat
                break
        
        # Code goes to Projects, everything else stays in Downloads/Category
        if category == "Code":
            dest_dir = PROJECTS_DIR
        else:
            dest_dir = os.path.join(SOURCE_DIR, category)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        if os.path.dirname(file_path) == dest_dir: return

        try:
            time.sleep(0.5)
            dest_path = os.path.join(dest_dir, filename)
            final_dest = make_unique(dest_path)
            shutil.move(file_path, final_dest)
            
            icon = EMOJI_MAP.get(category, "📂")
            send_notification(f"Moved to {category} {icon}", filename)
            print(f"✅ Moved {filename} -> {category}")
        except Exception as e:
            print(f"❌ Error moving {filename}: {e}")

# --- THIS IS THE MISSING FUNCTION ---
def start_watch():
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)

    observer = Observer()
    handler = SmartSorter()
    observer.schedule(handler, SOURCE_DIR, recursive=False)
    observer.start()
    
    send_notification("Serge Active 🎩", "I am watching the door.")
    print(f"🎩 Serge is watching {SOURCE_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()