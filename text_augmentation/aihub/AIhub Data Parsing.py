import os
import json
from tqdm import tqdm
import csv 
import re

root_path = "./txt"
filtered_entries = []
# List all files in the folder
folder_list = os.listdir(root_path)
idx = 0;


def preprocess_sentence(sentence):
    sentence = sentence.lower().strip()
    # Remove & characters
    sentence = re.sub(r'[&,{,},(,)]', '', sentence)
    # Remove English letters and numbers
    sentence = re.sub(r'[A-Za-z0-9]', '', sentence)
    # Remove extra spaces resulting from the above replacements
    sentence = re.sub(r'\s+', ' ', sentence)
    sentence = sentence.strip()
    return sentence

# 폴더 리스트 탐색s
for folder_name in folder_list:
    print("="* 5 ,folder_name)
    folder_path = f"{root_path}/{folder_name}"
    file_list = os.listdir(folder_path)

    # 파일 리스트 탐색
    for file_name in tqdm(file_list):
        
        if file_name.endswith(".json"): 
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r") as json_file:
                data = json.load(json_file)

                # filtered_entries = [node for node in data["utterance"] if "협박" in node.get("intent", "")]
                if "utterance" in data and isinstance(data["utterance"], list):
                    
                    for node in data["utterance"]:
                        # Check if "intent" key exists and is a string
                        if "intent" in node and isinstance(node["intent"], list):
                            # Check if "intimidation" is present in the intent
                            if "협박" in node["intent"][0]:
                                txt = node["original_form"] 
                                #txt = preprocess_sentence(txt)
                                if len(txt) >= 5 :
                                    data = [idx, "협박", txt]
                                    filtered_entries.append(data)
                                    idx+=1
                else:
                    print("Error: Invalid data structure or missing key 'utterance' in data.")


unique_values = {}

# Iterate through the data and update the dictionary
for item in filtered_entries:
    if item[2] not in unique_values:
        unique_values[item[2]] = item

# Create a list of unique items from the dictionary
unique_data = list(unique_values.values())


fields = ['idx', 'class', 'conversation']
with open('test_원본.csv', 'w',newline='') as f: 
      
    # using csv.writer method from CSV package 
    write = csv.writer(f) 
      
    write.writerow(fields) 
    write.writerows(unique_data)