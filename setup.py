#!/usr/bin/env python3
"""
Interactive setup script for Copilot Skills for Customer Engagements.
Guides users through all configuration steps.
"""

import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(step_num, text):
    """Print a formatted step."""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 70)


def print_success(text):
    """Print a success message."""
    print(f"✓ {text}")


def print_error(text):
    """Print an error message."""
    print(f"✗ ERROR: {text}")


def print_info(text):
    """Print an info message."""
    print(f"ℹ {text}")


def check_python_version():
    """Check if Python version meets requirements."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major > 3 or (version.major == 3 and version.minor >= 7):
        print_success("Python version meets requirements (3.7+)")
        return True
    else:
        print_error("Python 3.7 or later is required")
        return False


def create_config_file():
    """Create config.json from config.example.json."""
    print_step(2, "Creating Configuration File")
    
    repo_root = Path(__file__).parent
    config_path = repo_root / "config.json"
    example_path = repo_root / "config.example.json"
    
    if config_path.exists():
        print_info(f"config.json already exists at: {config_path}")
        response = input("Do you want to reconfigure it? (y/n): ").strip().lower()
        if response != 'y':
            print("Skipping configuration file creation.")
            # Return the existing path
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return True, config.get("engagements_base_path")
            except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
                print_error(f"Failed to read existing config: {e}")
                return True, None
    
    # Read the example config
    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        print_error(f"Failed to read config.example.json: {e}")
        return False, None
    
    # Get OneDrive path from user
    print("\nHow would you like to specify your OneDrive Engagements folder?")
    print("  1. Browse for folder (graphical file picker)")
    print("  2. Enter path manually")
    
    choice = input("\nEnter choice (1 or 2) [default: 1]: ").strip() or "1"
    
    normalized_path = None
    
    if choice == "1":
        # Try to use file picker
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            print("\nOpening folder picker...")
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            root.attributes('-topmost', True)  # Bring dialog to front
            
            folder_path = filedialog.askdirectory(
                title="Select OneDrive Engagements Folder"
            )
            
            root.destroy()
            
            if folder_path:
                normalized_path = os.path.normpath(folder_path)
                print(f"Selected: {normalized_path}")
            else:
                print_info("No folder selected. Falling back to manual entry.")
                choice = "2"  # Fall back to manual entry
        except ImportError:
            print_error("tkinter not available. Falling back to manual entry.")
            print_info("Install tkinter with: sudo apt-get install python3-tk (Linux)")
            choice = "2"
        except Exception as e:
            print_error(f"Failed to open file picker: {e}")
            choice = "2"
    
    if choice == "2" or normalized_path is None:
        # Manual entry
        print("\nPlease enter your OneDrive Engagements folder path.")
        print("Examples:")
        if platform.system() == "Windows":
            print("  Windows: C:\\Users\\username\\OneDrive - Microsoft\\Engagements")
        else:
            print("  Mac/Linux: /Users/username/OneDrive - Microsoft/Engagements")
        
        while True:
            engagements_path = input("\nOneDrive Engagements path: ").strip()
            
            if not engagements_path:
                print_error("Path cannot be empty")
                continue
            
            # Expand user home directory and normalize the path
            expanded_path = os.path.expanduser(engagements_path)
            normalized_path = os.path.normpath(expanded_path)
            break
    
    # Ask user to confirm if path doesn't exist
    if not os.path.exists(normalized_path):
        print_info(f"Path does not exist yet: {normalized_path}")
        response = input("Do you want to create it later and continue? (y/n): ").strip().lower()
        if response != 'y':
            return False, None
    
    # json.dump() will automatically escape backslashes for JSON
    config["engagements_base_path"] = normalized_path
    
    # Write the config file
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print_success(f"Created config.json at: {config_path}")
        return True, normalized_path
    except Exception as e:
        print_error(f"Failed to write config.json: {e}")
        return False, None


def install_dependencies():
    """Install Python dependencies."""
    print_step(3, "Installing Python Dependencies")
    
    repo_root = Path(__file__).parent
    skills_dir = repo_root / ".github" / "skills"
    
    # Find all requirements.txt files in skills directories
    requirements_files = []
    if skills_dir.exists():
        requirements_files = list(skills_dir.glob("*/requirements.txt"))
    
    if not requirements_files:
        print_info("No requirements.txt found, skipping dependency installation.")
        return True
    
    # Install dependencies from all requirements files
    success = True
    for requirements_path in requirements_files:
        print(f"Installing dependencies from: {requirements_path}")
        print("This may take a minute...\n")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
            ])
            print_success(f"Dependencies installed from {requirements_path.parent.name}")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install dependencies from {requirements_path.parent.name}: {e}")
            success = False
    
    if success:
        print_success("All Python dependencies installed successfully")
    return success


def get_vscode_settings_path():
    """Get the path to VS Code user settings.json."""
    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get('APPDATA')
        if appdata:
            settings_dir = Path(appdata) / "Code" / "User"
        else:
            # Fallback for Windows if APPDATA is not set
            settings_dir = Path.home() / "AppData" / "Roaming" / "Code" / "User"
    elif system == "Darwin":  # macOS
        settings_dir = Path.home() / "Library" / "Application Support" / "Code" / "User"
    else:  # Linux
        settings_dir = Path.home() / ".config" / "Code" / "User"
    
    return settings_dir / "settings.json"


def configure_vscode_settings():
    """Configure VS Code user settings to enable Agent Skills."""
    print_step(4, "Configuring VS Code Settings")
    
    settings_path = get_vscode_settings_path()
    
    print(f"VS Code settings location: {settings_path}")
    
    # Ask user if they want to automatically configure
    response = input("\nDo you want to automatically enable Agent Skills in VS Code? (y/n): ").strip().lower()
    
    if response != 'y':
        print_info("Skipping automatic VS Code configuration.")
        print("\nTo manually enable Agent Skills:")
        print("  1. Open VS Code Settings (Ctrl+, or Cmd+,)")
        print("  2. Search for 'chat.useAgentSkills'")
        print("  3. Enable 'Chat: Use Agent Skills'")
        return False
    
    try:
        # Create settings directory if it doesn't exist
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read existing settings or create empty dict
        if settings_path.exists():
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        else:
            settings = {}
        
        # Enable Agent Skills
        settings["chat.useAgentSkills"] = True
        
        # Write updated settings
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
        
        print_success("VS Code Agent Skills enabled!")
        return True
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, OSError) as e:
        print_error(f"Failed to update VS Code settings: {e}")
        print_info("You can manually enable it in VS Code Settings.")
        return False


def configure_vscode_workspace(repo_path, engagements_path):
    """Configure VS Code workspace to include both folders."""
    print_step(5, "Configuring VS Code Workspace")
    
    if not engagements_path:
        print_info("No engagements path configured, skipping workspace setup.")
        return False
    
    workspace_path = repo_path / "copilot-skills.code-workspace"
    
    print(f"\nThis will create a workspace file: {workspace_path}")
    print("The workspace will include:")
    print(f"  1. This repository: {repo_path}")
    print(f"  2. Engagements folder: {engagements_path}")
    
    response = input("\nDo you want to create/update the workspace file? (y/n): ").strip().lower()
    
    if response != 'y':
        print_info("Skipping workspace configuration.")
        print("\nTo manually add workspace folders:")
        print("  1. Open this repository folder in VS Code")
        print("  2. Go to 'File > Add Folder to Workspace'")
        print("  3. Add your OneDrive Engagements folder")
        return False
    
    try:
        workspace_config = {
            "folders": [
                {
                    "name": "Copilot Skills",
                    "path": "."
                },
                {
                    "name": "Engagements",
                    "path": str(engagements_path)
                }
            ],
            "settings": {
                "chat.useAgentSkills": True
            }
        }
        
        with open(workspace_path, 'w', encoding='utf-8') as f:
            json.dump(workspace_config, f, indent=2)
        
        print_success(f"Workspace file created: {workspace_path}")
        return True
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, OSError) as e:
        print_error(f"Failed to create workspace file: {e}")
        return False


def configure_pattern_updater_scheduler(repo_root):
    """Configure optional automated pattern updates."""
    print_step(6, "Pattern Updater Automation (Optional)")
    
    print("\nThe pattern-updater skill can run automatically on a schedule.")
    print("This will extract patterns from your engagements and update the knowledge base.\n")
    
    response = input("Do you want to set up automated pattern updates? (y/n): ").strip().lower()
    
    if response != 'y':
        print_info("Skipping automated pattern updates.")
        print("You can still update patterns manually via Copilot chat or by running:")
        print(f"  python {repo_root}/.github/skills/pattern-updater/scripts/run_update.py")
        return False
    
    # Ask for schedule frequency
    print("\nHow often should patterns be updated?")
    print("  1. Monthly (recommended)")
    print("  2. Weekly")
    print("  3. Custom")
    
    schedule_choice = input("\nEnter choice (1, 2, or 3) [default: 1]: ").strip() or "1"
    
    system = platform.system()
    script_path = repo_root / ".github" / "skills" / "pattern-updater" / "scripts" / "run_update.py"
    
    print(f"\nConfiguring scheduler for {system}...")
    
    try:
        if system == "Windows":
            # Windows Task Scheduler
            if schedule_choice == "1":
                # Monthly on the 1st at 9 AM
                schedule = "/sc monthly /d 1 /st 09:00"
            elif schedule_choice == "2":
                # Weekly on Monday at 9 AM
                schedule = "/sc weekly /d MON /st 09:00"
            else:
                schedule = input("Enter custom schedule (e.g., '/sc weekly /d MON /st 09:00'): ").strip()
            
            task_cmd = f'schtasks /create /tn "Copilot Pattern Updater" /tr "\"{sys.executable}\" \"{script_path}\"" {schedule} /f'
            print_info(f"Creating task: {task_cmd}")
            print_info("Note: This requires administrator privileges.")
            
            confirm = input("\nProceed with task creation? (y/n): ").strip().lower()
            if confirm == 'y':
                result = subprocess.run(task_cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print_success("Windows Task Scheduler task created successfully!")
                    return True
                else:
                    print_error(f"Failed to create task: {result.stderr}")
                    print_info("You can manually create a scheduled task to run:")
                    print(f"  python {script_path}")
                    return False
            else:
                print_info("Task creation skipped.")
                return False
        
        elif system == "Darwin":
            # macOS launchd
            print_info("Creating launchd plist for macOS...")
            
            if schedule_choice == "1":
                # Monthly on the 1st at 9 AM
                interval_dict = '        <key>Day</key>\n        <integer>1</integer>\n        <key>Hour</key>\n        <integer>9</integer>\n        <key>Minute</key>\n        <integer>0</integer>'
            elif schedule_choice == "2":
                # Weekly (every 7 days) at 9 AM
                interval_dict = '        <key>Weekday</key>\n        <integer>1</integer>\n        <key>Hour</key>\n        <integer>9</integer>\n        <key>Minute</key>\n        <integer>0</integer>'
            else:
                print_info("Custom scheduling for launchd requires manual plist editing.")
                interval_dict = '        <key>Day</key>\n        <integer>1</integer>\n        <key>Hour</key>\n        <integer>9</integer>\n        <key>Minute</key>\n        <integer>0</integer>'
            
            plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.copilot.patternupdater</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{script_path}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
{interval_dict}
    </dict>
    <key>StandardOutPath</key>
    <string>{Path.home()}/Library/Logs/pattern-updater.log</string>
    <key>StandardErrorPath</key>
    <string>{Path.home()}/Library/Logs/pattern-updater.error.log</string>
</dict>
</plist>'''
            
            plist_path = Path.home() / "Library" / "LaunchAgents" / "com.copilot.patternupdater.plist"
            plist_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            # Load the launch agent
            subprocess.run(["launchctl", "load", str(plist_path)], check=False)
            
            print_success(f"LaunchAgent created at: {plist_path}")
            print_info("Logs will be written to ~/Library/Logs/pattern-updater.log")
            return True
        
        else:
            # Linux cron
            print_info("Creating cron job for Linux...")
            
            if schedule_choice == "1":
                # Monthly on the 1st at 9 AM
                cron_schedule = "0 9 1 * *"
            elif schedule_choice == "2":
                # Weekly on Monday at 9 AM
                cron_schedule = "0 9 * * 1"
            else:
                cron_schedule = input("Enter custom cron schedule (e.g., '0 9 * * 1' for weekly Monday 9am): ").strip()
            
            cron_line = f'{cron_schedule} cd "{repo_root}" && "{sys.executable}" "{script_path}" >> "{Path.home()}/pattern-updater.log" 2>&1\n'
            
            print_info(f"Add this line to your crontab:")
            print(f"  {cron_line}")
            
            confirm = input("\nAdd to crontab now? (y/n): ").strip().lower()
            if confirm == 'y':
                # Get current crontab
                result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                current_crontab = result.stdout if result.returncode == 0 else ""
                
                # Check if already exists
                if "pattern-updater" in current_crontab or str(script_path) in current_crontab:
                    print_info("Pattern updater cron job already exists.")
                    return True
                
                # Add new line
                new_crontab = current_crontab + cron_line
                
                # Write back
                process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
                process.communicate(input=new_crontab)
                
                if process.returncode == 0:
                    print_success("Cron job added successfully!")
                    print_info(f"Logs will be written to {Path.home()}/pattern-updater.log")
                    return True
                else:
                    print_error("Failed to add cron job")
                    return False
            else:
                print_info("Manual crontab setup skipped.")
                print("Run 'crontab -e' and add the line above to enable automated updates.")
                return False
    
    except Exception as e:
        print_error(f"Failed to configure scheduler: {e}")
        print_info("You can still run pattern updates manually via Copilot or command line.")
        return False


def show_completion(workspace_created, scheduler_configured):
    """Show completion message."""
    print_header("Setup Complete!")
    
    print("You're ready to use Copilot Skills for Customer Engagements!\n")
    
    if workspace_created:
        print("A workspace file has been created with both folders configured.\n")
        print("To get started:")
        print("  1. Run: code .")
        print("  2. When VS Code opens, click 'Yes' on the workspace notification")
        print("     (lower-right corner) to load both folders.\n")
    else:
        print("Next step: Launch VS Code in this directory")
        print("  Run: code .\n")
    
    if scheduler_configured:
        print("✓ Automated pattern updates are configured!\n")
        print("Patterns will be automatically extracted from your engagements")
        print("and the knowledge base will be kept up to date.\n")
    
    print("Try these commands in VS Code Copilot Chat:\n")
    print('  "initiate an engagement for Contoso on March 15"')
    print('  "generate tasks for Project Phoenix starting in 30 days"')
    print('  "build agenda from planning_transcript.txt"')
    print('  "update patterns from my engagements"')
    print("\nFor more information, see README.md")
    print("\nHappy engaging! 🚀\n")


def main():
    """Main setup flow."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Setup script for Copilot Skills for Customer Engagements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup.py                    # Run full setup
  python setup.py --scheduler-only   # Configure scheduler only
  python setup.py --help             # Show this help message
        """
    )
    parser.add_argument(
        '--scheduler-only',
        action='store_true',
        help='Configure only the pattern updater scheduler (skip other setup steps)'
    )
    
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent
    
    # Scheduler-only mode
    if args.scheduler_only:
        print_header("Pattern Updater Scheduler Configuration")
        print("Configuring automated pattern updates only.\n")
        
        # Check if config.json exists
        config_path = repo_root / "config.json"
        if not config_path.exists():
            print_error("config.json not found!")
            print_info("Please run 'python setup.py' (without --scheduler-only) first to complete initial setup.")
            sys.exit(1)
        
        # Configure scheduler
        scheduler_configured = configure_pattern_updater_scheduler(repo_root)
        
        # Show completion
        print("\n" + "=" * 70)
        if scheduler_configured:
            print("✓ Scheduler configuration complete!")
            print("\nAutomated pattern updates are now enabled.")
        else:
            print("Scheduler configuration skipped.")
            print("\nRun 'python setup.py --scheduler-only' again to configure scheduling.")
        print("=" * 70 + "\n")
        return
    
    # Full setup mode
    print_header("Copilot Skills for Customer Engagements - Setup")
    print("This script will guide you through the configuration process.\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create config file
    success, engagements_path = create_config_file()
    if not success:
        print_error("Configuration failed. Please fix the errors and try again.")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()  # Continue even if this fails
    
    # Configure VS Code settings
    configure_vscode_settings()
    
    # Configure VS Code workspace
    workspace_created = configure_vscode_workspace(repo_root, engagements_path)
    
    # Configure pattern updater scheduler (optional)
    scheduler_configured = configure_pattern_updater_scheduler(repo_root)
    
    # Show completion
    show_completion(workspace_created, scheduler_configured)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except SystemExit:
        raise  # Allow sys.exit() to work properly
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
