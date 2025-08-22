# Rename by HIMU

====================================================
       ██╗  ██╗██╗███╗   ███╗██╗   ██╗
       ██║  ██║██║████╗ ████║██║   ██║
       ███████║██║██╔████╔██║██║   ██║
       ██╔══██║██║██║╚██╔╝██║██║   ██║
       ██║  ██║██║██║ ╚═╝ ██║╚██████╔╝
       ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ╚═════╝ 
====================================================


---

## 📦 Prerequisites

Make sure you have the following installed **before running the script**:

1. **Python 3.x**  
   - Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
   - During installation, tick **"Add Python to PATH"**.  
   - Verify:  
     ```bash
     python --version
     ```

2. **Pip (Python package manager)**  
   - Installed automatically with Python (if not, reinstall Python).  
   - Verify:  
     ```bash
     pip --version
     ```

3. **MKVToolNix (for `mkvpropedit`)**  
   - Download: [https://mkvtoolnix.download/](https://mkvtoolnix.download/)  
   - Install and make sure the installation path (e.g., `C:\Program Files\MKVToolNix`) is added to your **System PATH**.  
   - Verify:  
     ```bash
     mkvpropedit --version
     ```

4. **Python libraries** (auto-installed if missing via `requirements.bat`)  
   - `pymediainfo`  
   - `questionary`  
   - `rich`  

---

# 🚀 Usage

1. **Place your `.mkv` files in the **`input_folder/`**.**  
   (They will be renamed **in-place** unless changed to `output_folder/` in config).

2. **Run the batch file:**
   ```bash
   run_renamer.bat

3. **Interactive Menu will appear:**
   - Choose between Movie or Series mode.
   - Enter details like show name, season, OTT platform.
   - The script will extract metadata (resolution, audio language, codec, etc.), generate a new filename, and rename the file.

4. **Example:**
Old: 6.mkv
New: Pammi.Aunty.S01E06.720p.HS.WEB-DL.EN.AAC2.0.H264-TMBxHIMU.mkv

5. **At the end, a summary is shown with how many files were renamed.**

**✅ Notes :**
 - Always keep a backup of your files.
 - Overwriting is enabled by default.
 - Languages will be capitalized (en → EN, und → UND).
 - mkvpropedit is mandatory for updating track metadata.

---

# 🔧 Troubleshooting :

1. **Python not detected**
   - Error : [ERROR] Python is not installed or not in PATH.
   - Fix : Reinstall Python 3.x and check "Add Python to PATH" during installation.
   - Test with : python --version

2. **pip not detected**
   - Error: [ERROR] pip is not installed or not in PATH.
   - Fix: Reinstall Python (pip comes bundled).

   - install manually: python -m ensurepip --upgrade

3. **mkvpropedit not found**
   - Error: [WARNING] mkvpropedit not found!
   - Fix: Install MKVToolNix from https://mkvtoolnix.download/

    - Add its install folder (e.g., C:\Program Files\MKVToolNix) to System PATH.

   - Verify: mkvpropedit --version


 Created with ❤️ by HIMU
