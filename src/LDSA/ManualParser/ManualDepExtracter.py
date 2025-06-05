import csv
import os

def find_options_in_description(input_file_path, software):
    with open(input_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        options = list(reader)

        option_dict = {row[0]: row[1] for row in options}
        results = []

        for option in options:
            option_a_name = option[0]
            option_a_description = option[1]
            mentioned_options = [name for name in option_dict if name in option_a_description and name != option_a_name]

            for option_b_name in mentioned_options:
                option_b_description = option_dict[option_b_name]
                results.append([software, option_a_name, option_b_name, option_a_description, option_b_description])

    return results


softwares = ["core"]

all_results = []

for software in softwares:
    input_file_path = f'ManualParser/python-manual/glance_config_options.csv'
    output_file_path = f'./ManualParser/dependency/glanceDependency.csv'
    software_results = find_options_in_description(input_file_path, software)
    all_results.extend(software_results)

with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(['ID', 'Software', 'Option A', 'Option B', 'Option A Description', 'Option B Description'])
    
    for idx, result in enumerate(all_results, start=1):
        writer.writerow([idx] + result)

print(f"All dependencies have been written to {output_file_path}.")
