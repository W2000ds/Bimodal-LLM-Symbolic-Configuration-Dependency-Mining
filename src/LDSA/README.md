## LLM-Symbolic Code Analyzer Usage Guide

`RunCode.py` is the main entry point for running the configuration dependency mining pipeline, including code extraction, dependency identification, and dependency classification.

### 1. Preparation

- Ensure the following files and directories are ready:
  - Source code directory of your target software (set `project_root_dir`).
  - Taint analysis result CSV (set `TA_resultcsv`).
  - Prompt files for the identification and formalization (`prompt1.txt`, `prompt2.txt`,corresponding to Fig. 6 and Fig. 7 in paper).
  - Output directories for results.

- Update the following variables in `RunCode.py` as needed:
  - `software`: Name of the target software (e.g., `'hdfs'`).
  - `modellist`: List of models to use (e.g., `['dpseek']`).
  - `project_root_dir`: Path to your software's source code directory.
  - `TA_resultcsv`: Path to the taint analysis result CSV.
  - `Identifyerprompt_file` and `Classifyerprompt_file`: Paths to your prompt files.
  - `Identifyerresultfile` and `Classifyerresultfile`: Output paths for results.

### 2. Running the Pipeline

Run the script with:

```bash
python RunCode.py
```

The script will perform the following steps for each model in `modellist`:
1. **Code Extraction:** Extracts relevant code snippets based on the taint analysis results.
2. **Dependency Identification:** Uses LLM-based prompts to identify configuration dependencies.
3. **Dependency Classification:** Further classifies the identified dependencies.

### 3. Output

- `CodeDepBase.csv`: Extracted code base for analysis.
- `Finderresult.csv`: Results of the dependency identification step.
- `Formalizationresult.csv`: Results of the dependency formalization step.

### 4. Notes

- Make sure all required dependencies (such as `pandas`) are installed.
- Adjust file paths and parameters as needed for your environment.
- The script prints progress information to the console.

---
**Example directory structure:**
```
project_root/
├── src/
│   └── LDSA/
│       ├── RunCode.py
│       ├── DepClassifyer.py
│       ├── DepIdentifyer.py
│       ├── CodeExtractor.py
│       └── ...
├── TAresult/
│   └── hdfs.csv
├── prompt1.txt
├── prompt2.txt
└── ...
```

## LLM-Symbolic Manual Analyzer Usage Guide

`RunManual.py` is used for LLM-based dependency mining from software manual/documentation. It processes pairs of configuration parameters and their descriptions, and uses an LLM to extract formal dependency expressions (BNF) and dependency types.

---

### 1. Preparation

- **Dependencies:**  
  - Install required Python packages:
    ```bash
    pip install openai pandas
    ```
  - Ensure your LLM chat API wrappers (e.g., `dpseek_qwen_chat`, `doubao_chat`, etc.) are implemented and available in LLMChat.py.
  - Prepare the following files:
    - Manual dependency CSVs for each software (e.g., `./ManualParser/dependency/cinderDependency.csv`)
    - Prompt file (`prompt3.txt`), which contains the instruction for the LLM, corresponding to Fig. 7 in paper.

- **Edit the script as needed:**
  - Update the `model` list to include the LLMs you want to use (e.g., `["dpseek"]`).
  - Update the `software` list to include your target software names (e.g., `["cinder", "glance", "hdfs"]`).
  - Adjust file paths if your directory structure is different.

---

### 2. Running the Script

Run the script with:

```bash
python RunManual.py
```

For each model and software, the script will:
1. Read the manual dependency CSV file.
2. For each parameter pair, construct a prompt and query the LLM.
3. Extract the BNF formula and dependency type from the LLM response.
4. Write the results to a CSV file in `./ldsa-result/manual/`.

---

### 3. Output

- Output files are named as:  
  `./ldsa-result/manual/{model}-{software}.csv`
- Each output CSV contains:
  - `ID`: Row identifier
  - `Parameter1`: First configuration parameter
  - `Parameter2`: Second configuration parameter
  - `BNF`: Extracted BNF formula
  - `Type`: Dependency type
  - `FullResponse`: Full LLM response for reference

---

### 4. Notes

- The script will skip already processed IDs if you rerun it (incremental processing).
- Make sure your prompt file and manual dependency CSVs are correctly formatted.
- The script prints progress and errors to the console.
- If you use a different LLM or API, update the model selection and chat function calls accordingly.

---

**Example directory structure:**
```
project_root/
├── src/
│   └── LDSA/
│       ├── RunManual.py
│       └── ...
├── ManualParser/
│   └── dependency/
│       ├── cinderDependency.csv
│       ├── glanceDependency.csv
│       └── hdfsDependency.csv
├── prompt3.txt
└── ldsa-result/
    └── manual/
```
```
