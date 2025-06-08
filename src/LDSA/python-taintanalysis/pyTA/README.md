#  Python Static Taint and Dependency Analysis Toolkit
---

## Directory Structure

```
src/LDSA/python-taintanalysis/pyTA/depanalyzer/
│
├── varanalys.py      # Variable dependency analysis
├── controlflow.py    # Control flow analysis
├── crosschecker.py   # Cross-checking variable and control flow dependencies
├── main.py           # Example pipeline for batch analysis
└── __init__.py
```

---

## 1. Variable Dependency Analysis

**Script:** `varanalys.py`

Extracts variable dependencies within a Python project, supporting scope-aware tracing.

**Usage Example:**
```python
from varanalys import DependencyAnalyzer

# Initialize analyzer with your project directory and output CSV path
analyzer = DependencyAnalyzer("apps/glance/", "taresult/test.csv")

# Analyze dependencies for a specific variable
analyzer.run_var_traces("your_variable_name")

# Or, find variable locations from a CSV list
analyzer.find_var_locations_from_csv("input_varnames.csv", "output_locations.csv")
```

---

## 2. Control Flow Analysis

**Script:** `controlflow.py`

Extracts control flow structures (if, for, while, try, with, etc.) from Python files.

**Usage Example:**
```python
from controlflow import ControlFlowAnalyzer

# Analyze all Python files in a project directory
analyzer = ControlFlowAnalyzer("apps/glance/", "result/controlflow/glance_controlflow.csv")
analyzer.analyze_project()

# Or, analyze a single Python file
ControlFlowAnalyzer.analyze_single_file("path/to/your/file.py")
```

---


---

## 3. Batch Pipeline Example

**Script:** `main.py`

You can run the full pipeline for multiple software projects by editing the `softwarelist` in `main.py` and running:

```bash
python main.py
```

---

## 5. Output

- Variable dependency results: e.g., `result/taresult/{software}.csv`
- Control flow results: e.g., `result/controlflow/{software}controlflow_result.csv`
- Cross-check results: e.g., `result/depresult/{software}.csv`

---

## 6. Requirements

- Python 3.7+

---

## Example Directory Structure

```
project_root/
├── apps/
│   └── glance/
│       └── ... (Python source files)
├── configfile/
│   └── glance-defaultConfig.csv
├── result/
│   ├── taresult/
│   ├── controlflow/
│   └── depresult/
└── src/
    └── LDSA/
        └── python-taintanalysis/
            └── pyTA/
                └── depanalyzer/
                    ├── varanalys.py
                    ├── controlflow.py
                    ├── crosschecker.py
                    ├── main.py
                    └── __init__.py
```

---

```