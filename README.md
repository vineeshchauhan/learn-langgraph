# Project environment creation guide

## Install Python version
```bash
python --version
# Expected: Python 3.8+ (we recommend Python 3.11 or 3.12 for best compatibility)
```

---

## Understanding Virtual Environments

A virtual environment is an isolated Python environment that allows you to manage dependencies for each project separately. It prevents conflicts between projects and avoids affecting the system-wide Python installation. Tools like `venv` (built-in) or `virtualenv` are commonly used to create them.

### Benefits:
1. **Avoid Dependency Conflicts** - Different projects can use different versions of the same package
2. **Isolate Project Environments** - Each project has its own clean environment
3. **Simplifies Project Management** - Clear separation between projects
4. **Prevents System Interference** - No changes to system-wide Python installation
5. **Enables Reproducibility** - Exact dependencies can be recorded and shared

---

## Terminal-Specific Commands

The commands differ based on your shell. Choose the appropriate one for your terminal:

### Option A: Using `venv` (Recommended - Built into Python 3.3+)

#### CMD (Windows Command Prompt)
```cmd
# Create virtual environment
python -m venv my_env

# Activate (Notice: no `Scripts\` prefix needed)
my_env\Scripts\activate

# Deactivate
deactivate
```

#### PowerShell (Windows PowerShell / Windows Terminal)
```powershell
# Create virtual environment
python -m venv my_env

# Activate
my_env\Scripts\Activate.ps1

# Deactivate
deactivate
```

**PowerShell Note:** If you get an execution policy error, run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy RemoteSigned
```

#### Git Bash (Mingw64 / WSL)
```bash
# Create virtual environment
python -m venv my_env

# Activate
source my_env/Scripts/activate

# Deactivate
deactivate
```

---

### Option B: Using `virtualenv` (Alternative)

#### CMD
```cmd
# Install virtualenv (one-time)
pip install virtualenv

# Create virtual environment
virtualenv my_env

# Activate
cd my_env
Scripts\activate

# Deactivate
cd my_env
deactivate
```

#### PowerShell
```powershell
# Install virtualenv (one-time)
pip install virtualenv

# Create virtual environment
virtualenv my_env

# Activate
cd my_env
Scripts\Activate.ps1

# Deactivate
deactivate
```

#### Git Bash
```bash
# Install virtualenv (one-time)
pip install virtualenv

# Create virtual environment
virtualenv my_env

# Activate
source my_env/bin/activate

# Deactivate
deactivate
```

---

## Quick Start (All Terminals)

After creating and activating your virtual environment:

```bash
# Install all project dependencies
pip install -r requirements.txt

# Verify installation
python -c "import langchain; import langgraph; print('All packages installed successfully!')"
```

---

## Troubleshooting: Environment Disappearing

If your `my_env` folder disappears after a few days, here are the common causes and solutions:

### Cause 1: Antivirus Software
Many antivirus programs automatically delete virtual environments because they contain many small files (a common virus pattern).

**Solution:** Add an exclusion for your project folder:
- Windows Security → Virus & threat protection → Manage settings → Add or remove exclusions
- Add: `C:\dev\learn-langgraph\my_env`

### Cause 2: Disk Cleanup / Temp Files
Windows Disk Cleanup or temporary file cleaners may remove the `my_env` folder.

**Solution:** Check your Disk Cleanup settings and exclude `my_env` folder.

### Cause 3: Git Push/Pull Issues
If you're using Git, ensure `my_env` is in your `.gitignore` (which it should be). Some developers accidentally delete it when cleaning their workspace.

**Solution:** Check `.gitignore` - it should include `my_env/`:
```bash
echo "my_env/" >> .gitignore
```

### Cause 4: Cloud Sync (Dropbox, OneDrive, Google Drive)
Syncing the `my_env` folder can cause issues. These folders often get corrupted or deleted during sync.

**Solution:** Never store `my_env` in a synced folder. Use local storage only.

### Recommended: Create a Reinstallation Script

Create a file named `setup_env.bat` in your project root:
```batch
@echo off
echo Creating virtual environment...
python -m venv my_env
echo Activating and installing dependencies...
call my_env\Scripts\activate.bat
pip install -r requirements.txt
echo Setup complete! Run "call my_env\Scripts\activate.bat" to activate the environment.
pause
```

---

## Verification Checklist

After setup, verify everything works:

1. **Virtual environment created:** `dir my_env` should show folders like `Scripts`, `Lib`, `pyvenv.cfg`
2. **Activation works:** Prompt should show `(my_env)` prefix
3. **Dependencies installed:** `pip list` should show all packages from `requirements.txt`
4. **Python works:** `python --version` should show your Python version
5. **Imports work:** `python -c "import langchain; import langgraph"` should not error

---



---

## Importing from Parent Directory (Module Import Issue)

### Problem
When you have a file in a subdirectory (e.g., 	ools/tool_basics.py) that needs to import constants from the parent directory (e.g., constants.py), you might try:

`ash
python tools/tool_basics.py
`

This causes: ModuleNotFoundError: No module named 'constants'

### Why It Fails
Python looks for modules in the current working directory, not in the script's directory. When running python tools/tool_basics.py, Python's module search path includes 	ools/ but not the parent directory.

### Simple Solution: Use Relative Imports

**Step 1:** Create an empty __init__.py file in the subdirectory to make it a package:
`ash
# In tools folder, create __init__.py (can be empty)
`

**Step 2:** Use relative imports in 	ool_basics.py:
`python
from ..constants import openai_key
from ..constants import openai_base_url
`

**Step 3:** Run as a module, not as a script:
`ash
# Correct way
python -m tools.tool_basics

# Wrong way (causes ModuleNotFoundError)
python tools/tool_basics.py
`

### Key Rule
- **Relative imports (rom ..module import X) only work when running as a module**
- Use python -m package.module instead of python path/to/file.py
- The -m flag tells Python to treat the file as part of a package

### Alternative: Run from the Subdirectory
You can also change to the subdirectory first:
`ash
cd tools
python tool_basics.py
`
But this changes the working directory, which may affect other path-dependent code.

---
## Pro Tips

1. **Always activate before working:** Make it a habit to run `my_env\Scripts\activate` first thing
2. **Keep requirements.txt updated:** After installing new packages, run `pip freeze > requirements.txt`
3. **Use `.env` for secrets:** Never commit API keys to Git
4. **Consider pyenv:** For managing multiple Python versions on Windows
5. **Consider pipx:** For installing Python CLI tools globally without affecting project environments
