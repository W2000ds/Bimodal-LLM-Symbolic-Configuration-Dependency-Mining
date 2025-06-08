# COT LLM Prompting Toolkit

This directory is used to implement Chain-of-Thought reasoning through various LLM APIs (DeepSeek, Doubao, Qwen, etc.), and automatically extract configuration dependencies and other information.

## Main Files

- `LLMChat.py`: Uniformly encapsulates major LLM APIs, providing functions such as `dpseek_chat`, `doubao_chat`, and `qwen_chat`.
- `RunCOT.py`: Reads CSV parameter pairs in batches, invokes LLMs to extract BNF dependencies, and saves the results as CSV.

## Quick Start

1. Install dependencies:
   ```bash
   pip install openai
   ```
2. Configure the API-KEY in `LLMChat.py`.
3. Run batch extraction:
   ```bash
   python RunCOT.py
   ```
   Results are saved in the `./cot-result/` directory.
