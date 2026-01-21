#!/usr/bin/env python3
"""
Interactive setup script for Copilot Skills for Customer Engagements.
Guides users through all configuration steps.
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
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return True, config.get("engagements_base_path")
            except:
                return True, None
    
    # Read the example config
    try:
        with open(example_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
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
                title="Select OneDrive Engagements Folder",
                mustexist=False
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
        with open(config_path, 'w') as f:
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
        settings_dir = Path(os.environ.get('APPDATA', '')) / "Code" / "User"
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
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        else:
            settings = {}
        
        # Enable Agent Skills
        settings["chat.useAgentSkills"] = True
        
        # Write updated settings
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print_success("VS Code Agent Skills enabled!")
        return True
    except Exception as e:
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
        
        with open(workspace_path, 'w') as f:
            json.dump(workspace_config, f, indent=2)
        
        print_success(f"Workspace file created: {workspace_path}")
        print_info(f"Open this workspace in VS Code with: code {workspace_path}")
        return True
    except Exception as e:
        print_error(f"Failed to create workspace file: {e}")
        return False


def show_completion(workspace_created):
    """Show completion message."""
    print_header("Setup Complete!")
    
    print("You're ready to use Copilot Skills for Customer Engagements!\n")
    
    if workspace_created:
        print("Next step: Open the workspace file in VS Code")
        print("  Run: code copilot-skills.code-workspace")
        print("  Or: Open it from VS Code File menu\n")
    else:
        print("Next step: Open this repository in VS Code\n")
    
    print("Try these commands in VS Code Copilot Chat:\n")
    print('  "initiate an engagement for Contoso on 2026-03-15"')
    print('  "generate tasks for Project Phoenix on 2026-04-20"')
    print('  "build agenda from planning_transcript.txt"')
    print("\nFor more information, see README.md")
    print("\nHappy engaging! 🚀\n")


def main():
    """Main setup flow."""
    print_header("Copilot Skills for Customer Engagements - Setup")
    print("This script will guide you through the configuration process.\n")
    
    repo_root = Path(__file__).parent
    
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
    
    # Show completion
    show_completion(workspace_created)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
