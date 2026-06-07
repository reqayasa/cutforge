# CUTFORGE | Cutting List Solver (Python)
![Screen Shot](app_screenshot.png?raw=true "Cutting List Solver")

Personal project for solving cutting stock problems using a PySide6 desktop app.

## Roadmap

### Already Working (1D Solver)

- FFD solver implemented  
- Import stock & demand from CSV  
- Support multiple stock sizes + quantities  
- Preview imported data  
- Result summary: Total parts, Total used, Total waste, eficiencty
- Logging system  
- Export result to CSV  

### Next Improvements (High Priority)

- [ ] Edit data directly in preview → sync back to CSV  
- [ ] Improve result summary (especially multiple stock usage breakdown)  
- [ ] Add kerf support  
- [ ] Set default input/output folder  
- [ ] Run multiple CSV files in one go (batch process)  

### Algorithm Improvements

- [ ] Add BFD (Best Fit Decreasing)  
- [ ] Explore column generation (advanced, maybe slow)  
- [ ] Allow user to select algorithm  

### Visualization / UX

- [ ] Graphical cutting pattern preview  
- [ ] Alternative output formats (selectable in settings)
- [ ] Add icon

### Bigger Expansion

- [ ] 2D cutting version (basically duplicate + redesign logic)


## Clone Repository

```bash
git clone https://github.com/reqayasa/cutforge.git
cd cutforge
```

## Start Development
1. Create Virtual Environment
```bash
python -m venv .venv
```

2. Activate it:
```bash
# Windows
.venv/Scripts/Activate

# Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the App
```bash
python main.py
```

5. Updating -> Push to repo
```bash
pip freeze > requirements.txt
git add .
git commit -m "message"
git push -u origin main
```

## Build Application (PySide6 Deploy)

### Requirements
- **Python 3.9+** (tested with 3.12)
- Virtual environment activated (with requirements.txt installed)
- **Windows/Linux** - builds work cross-platform
- ~2 GB disk space for build output

Required packages (in `requirements.txt`):
- `PySide6==6.10.2`
- `PySide6_Essentials==6.10.2`
- `shiboken6==6.10.2`
- `Nuitka==2.7.11` (installed automatically by pyside6-deploy)

### Build Instructions

The build configuration is in `pysidedeploy.spec`. You can build in two modes:

#### Option 1: Standalone (Recommended - Default)
Creates a self-contained folder with all dependencies. Larger but more portable.

```bash
pyside6-deploy -c pysidedeploy.spec
```

Output location: `./dist/cutforge/`
- Platform: Windows → `cutforge.exe`
- Platform: Linux → `cutforge` (executable)

#### Option 2: One-File Executable
Creates a single `.exe` (Windows) or binary (Linux). Slower startup, smaller on disk.

First, update `pysidedeploy.spec`:
```ini
[nuitka]
mode = onefile
```

Then build:
```bash
pyside6-deploy -c pysidedeploy.spec
```

Output location: `./dist/cutforge` (single executable file)

### Build Notes
- First build takes longer (~5-10 min depending on system)
- Subsequent builds are faster due to caching
- Build produces optimized, compressed binary using Nuitka
- Qt translations are excluded for minimal size (~150 MB standalone)
- The `./data/input` folder is automatically included in the build