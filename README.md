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

- **[Ciri](https://github.com/xlab-uiuc/ciri/tree/main/icse25_data)**  
  Integrates LLMs to detect dependency-related misconfigurations by analyzing source code and configuration files, identifying potential violations.

- **[CDep](https://github.com/xlab-uiuc/cdep-fse-ae)**  
  uses code coloring and pattern matching for classifying dependencies, empowered with inter procedure analysis to extract the variable assignments of option values. 
  


## Repository structure:

> |——RQ_Supplementary: Contains the specific supplementary files for tables in our paper.

>  |——Dataset: All result of each method with multi runs and groundtruth result.

> |—— LDSA-src: The source code of LDSA.