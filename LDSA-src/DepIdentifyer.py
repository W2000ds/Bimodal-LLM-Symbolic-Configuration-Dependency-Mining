# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI
import csv
import requests
import os
import re
from LLMChat import dpseek_chat, doubao_chat,qwen_chat,dpseek_qwen_chat


class DepIdentifyer:
    def __init__(self, csv_file, resultfile, prompt_file,model):
        self.csv_file = csv_file
        self.resultfile = resultfile
        self.prompt_file = prompt_file
        self.model = model  


    def extract_answer(self,text):
        pattern = r'"ans":\s*"(\bYes\b|\bNo\b)"'
        match = re.search(pattern, text)
        return match.group(1) if match else None 

    def load_existing_results(self, resultfile):

        existing_results = {}
        if os.path.exists(resultfile) and os.stat(resultfile).st_size > 0:
            with open(resultfile, mode='r', encoding='utf-8', errors='replace') as file:  # Added `errors='replace'`
                reader = csv.reader(file)
                next(reader) 
                for row in reader:
                    if len(row) >= 2: 
                        qid, answer = row[0], row[1]
                        if not answer.startswith("Error:"): 
                            existing_results[qid] = answer

                return existing_results
        else:
            return existing_results

    def load_prompt_content(self):
            if not os.path.isfile(self.prompt_file):
                raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                return f.read()
            

    def Find(self):
        prompt_content = self.load_prompt_content()
        

        file_exists = os.path.exists(self.resultfile)
        

        if not file_exists:
            with open(self.resultfile, mode='w', newline='', encoding='utf-8') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(["id", "Parameter1", "Parameter2", "ans", "FullResponse"])
        

        existing_results = self.load_existing_results(self.resultfile)
        

        with open(self.csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            rows = list(reader)

        with open(self.resultfile, mode='a', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            
            for row in rows[1:]:
                try:
                    if len(row) < 5:
                        writer.writerow([f"Warning: Row with insufficient columns: {row}", "", "", "", ""])
                        continue
                    
                    id = row[0]
                    para1 = row[2]
                    para2 = row[4]
                    localvar1 = row[3]
                    localvar2 = row[5]
                    method_code = row[6]
                    if id in existing_results:
                        print(f"Skipping ID {id}: already processed.")
                        continue
                    
                    question = (
                        f"{prompt_content}\n\n"
                        f"Configuration A: {para1}\n"
                        f"Configuration B: {para2}\n"
                        f"Configuration A corresponding variable in code snippet: {localvar1}\n"
                        f"Configuration B corresponding variable in code snippet: {localvar2}\n"
                        f"Code Snippet:\n"
                        f"Complete method code with this line is:\n{method_code}"
                    )
                    

                    if self.model == 'dpseek':
                        finder_full_response = dpseek_qwen_chat(question)
                    elif self.model == 'doubao':
                        finder_full_response = doubao_chat(question)
                    elif self.model == 'qwen':
                        finder_full_response = qwen_chat(question)
                    else:
                        raise ValueError(f"Unsupported model: {self.model}")

                    answer = self.extract_answer(finder_full_response)


                    print(f"ID {id} - Answer: {answer}")
                    writer.writerow([id, para1, para2, answer, finder_full_response])
                    out_file.flush()

                except Exception as e:
                    writer.writerow([
                        id if 'id' in locals() else "ERROR",
                        para1 if 'para1' in locals() else "", 
                        para2 if 'para2' in locals() else "",
                        "ERROR OCCURRED",
                        str(e)
                    ])
                    out_file.flush()
                    print(f"Error processing row {row}: {str(e)}")


if __name__ == "__main__":
    CodeDepBase = 'CodeDepBase.csv'
    prompt_file = 'prompt1.txt'
    Finderresultfile = 'Finderresult.csv'

    finder = DepIdentifyer(CodeDepBase, Finderresultfile, prompt_file)
    finder.Find()
    print("Find Done!")
