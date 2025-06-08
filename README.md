# Bimodal-LLM-Symbolic-Configuration-Dependency-Mining

This is repository of paper
>Bimodal-LLM-Symbolic-Configuration-Dependency-Mining

## Introduction

>While most software systems are highly configurable, correctly configuring them is complex due to the presence of diverse dependencies between the configuration options---the setting of one configuration option depends on the value of the others. A root cause thereof is that the guideline for complying with dependency is often missing or poorly instructed. Existing automated tools for configuration dependency analysis are limited to certain dependency forms and granularity without fully exploiting the valuable artefacts from the systems that can be readily leveraged.

>In this paper, we overcome the above limitation in analyzing and mining configuration dependencies via LDSA, a bimodal LLM-symbolic automated tool. The key of LDSA is that we construct formal expressions of information from two modalities, user manual and code, which are combined with dedicated LLMs, for reasoning and mining the dependencies in a system. This would produce a fine-grained and formal dependency expression, alongside addressing relevant tasks for configuration dependency analysis, that can assist other tools for configuration management. Experiment results on seven systems and against four existing tools show that LDSA significantly outperforms them on all dependency analysis tasks with up to 1218% improvement on F1-score while being able to boost other tasks such as configuration tuning and is practical for real-world application.


## Systems
| Name           | Category              | Language | Version  |
|----------------|-----------------------|----------|----------|
| HDFS           | File System           | Java     | 3.3.5    |
| HBase          | NoSQL Database        | Java     | 2.1.1    |
| Yarn           | Resource Management   | Java     | 3.3.5    |
| MapReduce      | Distributed Computing | Java     | 3.3.5    |
| Core           | Resource Management   | Java     | 3.3.5    |
| Cinder         | Storage Service       | Python   | 26.1.0   |
| Glance         | Image Service         | Python   | 30.1.0   |

###  Dependency related analysis tools:
- **[GPTuner](https://github.com/SolidLao/GPTuner)**  
  Leverages LLMs to parse user manuals for extracting dependencies between configuration options, enabling automated performance tuning.

- **[CDep](https://github.com/xlab-uiuc/cdep-fse-ae)**  
  Use code coloring and pattern matching for classifying dependencies, empowered with inter procedure analysis to extract the variable assignments of option values. 
  
- [COT]
  Please check \src\TailoredTools\COT for more detail.

- [LLM-RAG]
  Please check \src\TailoredTools\LLM-RAG for more detail.

## Repository structure:

> |——RQ_Supplementary: Contains the specific supplementary files for tables in our paper.  
|——Dataset: All result of each method with multi runs and groundtruth result.  
|——src: The source code of methods mentioned in paper.  


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
  - `FullResponse`: Full LLM response for reference
---
