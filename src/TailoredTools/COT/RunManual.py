# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI
import csv
import requests
import os
import re
import json
from src.TailoredTools.COT.LLMChat import dpseek_chat, siliconflow_chat, qwen_chat,doubao_chat,dpseek_qwen_chat


class ManualClassifyer:
    def __init__(self, csv_file, resultfile, prompt_file,model):
        self.csv_file = csv_file
        self.resultfile = resultfile
        self.prompt_file = prompt_file
        self.model = model 

    def extract_bnf_formula(self, json_response):
        """
        Extracts the BNF formula from a JSON response that may be wrapped in markdown code blocks
        or mixed with non-JSON content.

        :param json_response: A JSON string (potentially in markdown format) or dictionary containing the response.
        :return: The extracted BNF formula as a string, or None if not found.
        """
        # If the input is a string, try to extract JSON from it
        if isinstance(json_response, str):
            try:
                # First, try to extract JSON content from markdown code blocks
                markdown_json_pattern = r'```(?:json)?\s*([\s\S]*?)```'
                match = re.search(markdown_json_pattern, json_response)
                
                if match:
                    # Extract the JSON content from within the code blocks
                    json_content = match.group(1).strip()
                else:
                    # If no markdown code block is found, try to extract JSON directly from the string
                    json_content = json_response.strip()
                
                # Attempt to parse the extracted JSON content
                try:
                    response_dict = json.loads(json_content)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract the first valid JSON object from the string
                    json_object_pattern = r'\{[\s\S]*\}'
                    json_match = re.search(json_object_pattern, json_response)
                    if json_match:
                        json_content = json_match.group(0)
                        response_dict = json.loads(json_content)
                    else:
                        print(f"Failed to parse JSON from response: {json_response[:100]}...")
                        return None
            except Exception as e:
                print(f"Error processing JSON response: {e}")
                return None
        elif isinstance(json_response, dict):
            response_dict = json_response
        else:
            print(f"Unexpected response type: {type(json_response)}")
            return None

        # Extract the BNF formula from the dictionary
        bnf_formula = response_dict.get("BNF formula", None)
        return bnf_formula

    def extract_type(self,text):

        pattern = r'"Type":\s*"([^"]*)"'    
        match = re.search(pattern, text)
        return match.group(1) if match else None

    def load_existing_results(self,resultfile):
        existing_results = {}
        if os.path.exists(resultfile) and os.stat(resultfile).st_size > 0:
            with open(resultfile, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # 跳过表头
                for row in reader:
                    if len(row) >= 2 and row[3] != '':
                        qid, answer = row[0], row[3]
                        if not answer.startswith("Error:"):
                            existing_results[qid] = answer

                return existing_results
        else:
            return existing_results


    def Find(self):
        prompt_content = self.load_prompt_content()
        
        file_exists = os.path.exists(self.resultfile)
        
        if not file_exists:
            with open(self.resultfile, mode='w', newline='', encoding='utf-8') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(["ID", "Parameter1", "Parameter2", "BNFr", "Type", "FullResponse"])
        
        existing_results = self.load_existing_results(self.resultfile)
        
        with open(self.csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            rows = list(reader)
        
        with open(self.resultfile, mode='a', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            for row in rows[1:]:
                try:
                    if len(row) < 4:
                        writer.writerow([f"Warning: Row with insufficient columns: {row}", "", "", "", "", ""])
                        continue

                    id = row[0]
                    para1 = row[1]
                    para2 = row[2]
                    description1 = row[3]
                    description2 = row[4]

                    if id in existing_results:
                        print(f"Skipping ID {id}: already processed.")
                        continue
                    
                    question = (
                        f"{prompt_content}\n\n"
                        f"Parameter 1: {para1}\n"
                        f"Parameter 2: {para2}\n"
                        f"Documentation Snippet:\n"
                        f"{para1}:{description1}\n"
                        f"{para2}:{description2}\n"
                    )
                    
                    if self.model == 'dpseek':
                        finder_full_response = dpseek_qwen_chat(question)
                    elif self.model == 'doubao':
                        finder_full_response = doubao_chat(question)
                    elif self.model == 'qwen':
                        finder_full_response = qwen_chat(question)
                    else:
                        raise ValueError(f"Unsupported model: {self.model}")
                    
                    bnf = self.extract_bnf_formula(finder_full_response)
                    type = self.extract_type(finder_full_response)
                    print(f"ID {id} - BNFr: {bnf} - Type: {type}")
                    writer.writerow([id, para1, para2, bnf, type, finder_full_response])
                    out_file.flush()
                    
                except Exception as e:
                    writer.writerow([
                        id if 'id' in locals() else "ERROR", 
                        para1 if 'para1' in locals() else "", 
                        para2 if 'para2' in locals() else "",
                        "ERROR OCCURRED",
                        "ERROR OCCURRED",
                        str(e)
                    ])
                    print(f"Error processing row {row}: {str(e)}")
                    out_file.flush()


    def load_prompt_content(self):
        if not os.path.isfile(self.prompt_file):
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")
        with open(self.prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
            
if __name__ == '__main__':
    for model in ["dpseek"]:
        for software in ["cinder","glance","hdfs"]:  # Replace with your actual software name
            manualdepbase  = f"./ManualParser/dependency/{software}Dependency.csv"
            resultfile = f"./cot-result/{model}-{software}.csv"
            prompt_file = "./promptcot.txt"
            manualclassifyer = ManualClassifyer(manualdepbase, resultfile, prompt_file,model)
            manualclassifyer.Find()
            print("Done!")
