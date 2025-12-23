import sys
import os
import subprocess
import config  # Import the "Hit List" for Dimitri
from staff import serge, zero, gustave, dimitri, agatha

def run_in_background():
    """Detaches the current command into a silent background process"""
    # Remove --bg so the new process doesn't loop infinitely
    args = [arg for arg in sys.argv if arg != "--bg"]
    
    # sys.executable ensures we use the venv python
    subprocess.Popen(
        [sys.executable] + args, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    print(f"🥷 GBH Background Service Started.")
    print(f"   (Running '{args[1]} {args[2]}' in the shadows)")

def main():
    # --- 1. HANDLE BACKGROUND REQUESTS ---
    if "--bg" in sys.argv:
        run_in_background()
        return

    # --- 2. DEFAULT BEHAVIOR (No Args) ---
    if len(sys.argv) < 2:
        g = gustave.Gustave()
        g.report()
        return

    command = sys.argv[1].lower()

    # --- GUSTAVE (System Status) ---
    if command == "status":
        g = gustave.Gustave()
        if "--notify" in sys.argv:
            g.notify()  # The startup notification
        else:
            g.report()  # The text dashboard

    # --- SERGE (File Sorter) ---
    elif command == "sort":
        serge.start_watch()

    # --- ZERO (Cleanup) ---
    elif command == "clean":
        boy = zero.Zero()
        
        # Check for duplicate flag
        if "--dupes" in sys.argv:
            target_dir = os.path.expanduser("~/Downloads")
            
            # Logic to handle custom paths: gbh clean --dupes ~/Pictures
            args = sys.argv
            for i, arg in enumerate(args):
                if arg == "--dupes":
                    if i + 1 < len(args):
                        target_dir = os.path.expanduser(args[i+1])
            
            boy.find_duplicates(target_dir)
        else:
            # Default: Sweep screenshots
            boy.clean_screenshots(days_old=1)

    # --- DIMITRI (Monitoring) ---
    elif command == "wait":
        # Usage: gbh wait 8000 [--bg]
        if len(sys.argv) < 3:
            print("Usage: gbh wait <port> [--bg]")
            return
        
        guard = dimitri.Dimitri()
        if sys.argv[2].isdigit():
            guard.wait_for_port(int(sys.argv[2]))
        else:
            print("❌ Port must be a number.")

    elif command == "watch":
        # Usage: gbh watch error.log [--bg]
        if len(sys.argv) < 3:
            print("Usage: gbh watch <file> [--bg]")
            return
        guard = dimitri.Dimitri()
        guard.watch_log(sys.argv[2])

    elif command == "patrol":
        # Startup routine (reads config.py)
        guard = dimitri.Dimitri()
        guard.start_patrol(config.PERMANENT_PORTS, config.PERMANENT_LOGS)

    elif command == "stop":
        # Kill switch for background watchers
        print("🔫 Stopping all GBH background tasks...")
        os.system("pkill -f 'gbh wait'")
        os.system("pkill -f 'gbh watch'")
        os.system("pkill -f 'gbh patrol'")
        print("   All watchers terminated.")

    # --- AGATHA (Archiving) ---
    elif command == "pack":
        # Usage: gbh pack [path]
        target = os.getcwd()
        if len(sys.argv) > 2:
            target = sys.argv[2]
        
        baker = agatha.Agatha()
        baker.pack_project(target)

    elif command == "backup":
        baker = agatha.Agatha()
        baker.backup_config()

    # --- HELP MENU ---
    else:
        print("🏨 GBH Suite Commands:")
        print("  gbh status           -> System Health Dashboard")
        print("  gbh sort             -> Start File Sorter (Serge)")
        print("  gbh clean            -> Sweep Screenshots")
        print("  gbh clean --dupes    -> Find Duplicates")
        print("  gbh wait <port>      -> Notify when Port is Ready")
        print("  gbh watch <file>     -> Notify on Log Errors")
        print("  gbh pack .           -> Archive Project (Smart Zip)")
        print("  gbh backup           -> Backup Dotfiles")

if __name__ == "__main__":
    main()