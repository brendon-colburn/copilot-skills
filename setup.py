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
    
    if version.major >= 3 and version.minor >= 7:
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
            return True
    
    # Read the example config
    try:
        with open(example_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print_error(f"Failed to read config.example.json: {e}")
        return False
    
    # Get OneDrive path from user
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
        
        # Expand user home directory if needed
        expanded_path = os.path.expanduser(engagements_path)
        
        # Ask user to confirm if path doesn't exist
        if not os.path.exists(expanded_path):
            print_info(f"Path does not exist yet: {expanded_path}")
            response = input("Do you want to create it later and continue? (y/n): ").strip().lower()
            if response != 'y':
                continue
        
        # Convert to proper format for JSON (use forward slashes or double backslashes)
        if platform.system() == "Windows":
            # Use double backslashes for Windows
            json_path = engagements_path.replace('/', '\\')
        else:
            json_path = expanded_path
        
        config["engagements_base_path"] = json_path
        break
    
    # Write the config file
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print_success(f"Created config.json at: {config_path}")
        return True
    except Exception as e:
        print_error(f"Failed to write config.json: {e}")
        return False


def install_dependencies():
    """Install Python dependencies."""
    print_step(3, "Installing Python Dependencies")
    
    repo_root = Path(__file__).parent
    requirements_path = repo_root / ".github" / "skills" / "agenda-builder" / "requirements.txt"
    
    if not requirements_path.exists():
        print_info("No requirements.txt found, skipping dependency installation.")
        return True
    
    print(f"Installing dependencies from: {requirements_path}")
    print("This may take a minute...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
        ])
        print_success("Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        print_info("You can manually install them later with:")
        print(f"  pip install -r {requirements_path}")
        return False


def show_vscode_instructions():
    """Show instructions for VS Code setup."""
    print_step(4, "VS Code Configuration")
    
    print("To complete setup, you need to configure VS Code:\n")
    
    print("A. Enable Agent Skills:")
    print("   1. Open VS Code Settings (Ctrl+, or Cmd+,)")
    print("   2. Search for 'chat.useAgentSkills'")
    print("   3. Enable 'Chat: Use Agent Skills'\n")
    
    print("B. Add Workspace Folders:")
    print("   1. Open this repository folder in VS Code")
    print("   2. Go to 'File > Add Folder to Workspace'")
    print("   3. Add your OneDrive Engagements folder")
    print("      (This allows Copilot to directly access your engagement files)\n")
    
    print_info("These steps must be done manually in VS Code.")


def show_completion():
    """Show completion message."""
    print_header("Setup Complete!")
    
    print("You're ready to use Copilot Skills for Customer Engagements!\n")
    print("Try these commands in VS Code Copilot Chat:\n")
    print('  "initiate an engagement for Contoso on 2026-03-15"')
    print('  "generate tasks for Project Phoenix on 2026-04-20"')
    print('  "build agenda from planning_transcript.txt"\n')
    print("For more information, see README.md")
    print("\nHappy engaging! 🚀\n")


def main():
    """Main setup flow."""
    print_header("Copilot Skills for Customer Engagements - Setup")
    print("This script will guide you through the configuration process.\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create config file
    if not create_config_file():
        print_error("Configuration failed. Please fix the errors and try again.")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()  # Continue even if this fails
    
    # Show VS Code instructions
    show_vscode_instructions()
    
    # Show completion
    show_completion()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
