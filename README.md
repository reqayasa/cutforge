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
```bash
pyside6-deploy -c pysidedeploy.spec
```