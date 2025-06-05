import csv
import os
from component.embedding import Zhipuembedding, BGEembedding
from component.data_chunker import ReadFile
from component.databases import Vectordatabase
from component.llms import Openai_model


class RAGProcessor:
    def __init__(self, csv_file, result_file, prompt_file, openai_instance):
        self.csv_file = csv_file
        self.result_file = result_file
        self.prompt_file = prompt_file
        self.openai_instance = openai_instance

    def load_prompt_content(self):
        """Load the prompt content from the specified file."""
        if not os.path.isfile(self.prompt_file):
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")
        with open(self.prompt_file, 'r', encoding='utf-8') as f:
            return f.read()

    def process(self):
        """Process the input CSV file and generate results using RAG."""
        prompt_content = self.load_prompt_content()

        # Check if the result file exists
        file_exists = os.path.exists(self.result_file)

        # If the file doesn't exist, create it and write the header
        if not file_exists:
            with open(self.result_file, mode='w', newline='', encoding='utf-8') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(["Parameter1", "FullResponse"])

        # Read the input data
        with open(self.csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            rows = list(reader)

        # Append results to the result file
        with open(self.result_file, mode='a', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            # Extract the first column as a list of parameters
            parameters = [row[0] for row in rows if len(row) > 0]

            # Process each row starting from the second row
            for row in rows[1:]:
                # try:
                    param1 = row[0]

                    # Use the OpenAI instance to get the response
                    response = self.openai_instance.chat(str(param1),parameters)

                    # Write the result to the CSV file
                    writer.writerow([param1, response])
                    print(f"Processed Parameter: {param1} - Response: {response}")
                    out_file.flush()

                # except Exception as e:
                #     writer.writerow([param1 if 'param1' in locals() else "", "ERROR OCCURRED", str(e)])
                #     print(f"Error processing row {row}: {str(e)}")
                #     out_file.flush()


if __name__ == '__main__':
    # Initialize OpenAI model instance
    api_key = "Your api key"
    base_url = "https://api.deepseek.com"
    embedding_model = Zhipuembedding()


    # Define software list and process each software
    software_list = ["cinder","glance"]
    for software in software_list:
        openai_instance = Openai_model(api_key=api_key, base_url=base_url, embedding_model=embedding_model,software=software)
        csv_file = f"ManualParser/manual/{software}-defaultConfig.csv"
        result_file = f"./Comparative/Result/rag/{software}.csv"
        prompt_file = "Comparative/RAGPrompt.txt"

        processor = RAGProcessor(csv_file, result_file, prompt_file, openai_instance)
        processor.process()
        print(f"Processing for {software} completed!")