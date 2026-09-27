# Virtual Environment FAQ

## Why does my virtual environment disappear after a few days?

### Most Common Cause: Windows Defender / Antivirus

Windows Defender and many third-party antivirus programs automatically quarantine or delete the `my_env` folder because:
- Virtual environments contain thousands of small files (a common malware pattern)
- The folder is created in your project directory
- Antivirus software uses heuristic analysis that flags many Python virtual environments

**Quick Fix: Add Exclusion**
1. Open **Windows Security** (search in Start menu)
2. Go to **Virus & threat protection** → **Manage settings**
3. Under **Exclusions**, click **Add or remove exclusions**
4. Add: `C:\dev\learn-langgraph\my_env`

### Other Possible Causes

| Cause | Solution |
|-------|----------|
| **Disk Cleanup** | Windows Disk Cleanup may delete large folders. Exclude `my_env` in Disk Cleanup settings |
| **OneDrive/Cloud Sync** | Syncing `my_env` can cause corruption. Ensure it's excluded from sync or not in a synced folder |
| **Manual Cleanup** | You or someone else may have accidentally deleted it while cleaning workspace |
| **Git Operations** | If `.gitignore` is missing or incorrect, some tools may try to "clean" ignored folders |
| **Temporary Location** | If created in a temp folder, Windows may delete it automatically |

## Which Terminal Should I Use?

### For Windows Users:

| Terminal | Best For | Activate Command |
|----------|----------|------------------|
| **Windows Terminal** (newest) | All users | `my_env\Scripts\Activate.ps1` |
| **PowerShell** | PowerShell users | `my_env\Scripts\Activate.ps1` |
| **CMD** | Legacy systems | `my_env\Scripts\activate.bat` |
| **Git Bash** | Unix-like preference | `source my_env/Scripts/activate` |

**Recommendation:** Use **Windows Terminal** with PowerShell for the best experience.

## How to Verify My Environment is Working

Run these commands after activation:

```powershell
# Check if activated (prompt should show (my_env))
(my_env) C:\dev\learn-langgraph>

# Verify Python version
python --version

# Verify packages are installed
pip list | Select-String "langchain|langgraph|pillow"

# Test imports
python -c "import langchain; import langgraph; import pillow; print('Success!')"
```

## Quick Recovery Commands

If your environment disappears, you can quickly recreate it:

```powershell
# Run the setup script (as Administrator if needed)
.\setup_env.bat

# Or do it manually
python -m venv my_env
my_env\Scripts\activate
pip install -r requirements.txt
```

## Best Practices to Prevent Issues

1. **Always activate before working:**
   ```powershell
   # Add to your PowerShell profile for auto-activation
   echo "my_env\Scripts\activate" >> $PROFILE
   ```

2. **Keep requirements.txt updated:**
   ```powershell
   # After installing new packages
   pip freeze > requirements.txt
   ```

3. **Check .gitignore:**
   Ensure `my_env/` is in `.gitignore`:
   ```powershell
   echo "my_env/" >> .gitignore
   ```

4. **Add to antivirus exclusions:**
   - Path: `C:\dev\learn-langgraph\my_env`
   - Or entire folder: `C:\dev\learn-langgraph`

5. **Use setup_env.bat for new setups:**
   This script handles everything and provides helpful error messages

## I Still Have Issues

If the problem persists after trying the above:

1. Check your antivirus logs for quarantined files
2. Verify the folder isn't being synced to cloud storage
3. Run `sfc /scannow` to check for system file corruption
4. Consider using `pipenv` or `poetry` instead of venv for better isolation