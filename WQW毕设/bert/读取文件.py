import os

folder_path = "../景点评价"

file_names = os.listdir(folder_path)

texts = []

for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        texts.append(text)

print(len(texts))
