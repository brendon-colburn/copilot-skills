#!/usr/bin/env python3
"""
Configure Pattern Updater Scheduler
Standalone script to enable/disable automated pattern updates.
Can be run independently after initial setup.
"""

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


def print_success(text):
    """Print a success message."""
    print(f"✓ {text}")


def print_error(text):
    """Print an error message."""
    print(f"✗ ERROR: {text}")


def print_info(text):
    """Print an info message."""
    print(f"ℹ {text}")


def configure_pattern_updater_scheduler(repo_root):
    """Configure optional automated pattern updates."""
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


def main():
    """Main scheduler configuration flow."""
    print_header("Pattern Updater Scheduler Configuration")
    print("This script configures automated pattern updates.")
    print("Run this if you want to enable scheduling after initial setup.\n")
    
    repo_root = Path(__file__).parent
    
    # Check if config.json exists
    config_path = repo_root / "config.json"
    if not config_path.exists():
        print_error("config.json not found!")
        print_info("Please run 'python setup.py' first to complete initial setup.")
        sys.exit(1)
    
    # Configure scheduler
    scheduler_configured = configure_pattern_updater_scheduler(repo_root)
    
    # Show completion
    print("\n" + "=" * 70)
    if scheduler_configured:
        print("✓ Scheduler configuration complete!")
        print("\nAutomated pattern updates are now enabled.")
        print("Patterns will be extracted from your engagements on the configured schedule.")
    else:
        print("Scheduler configuration skipped.")
        print("\nYou can still update patterns manually:")
        print("  - Via Copilot: 'update patterns from my engagements'")
        print(f"  - Command line: python {repo_root}/.github/skills/pattern-updater/scripts/run_update.py")
        print("\nRun this script again anytime to enable scheduling.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
