import pandas as pd

# Replace 'your_file.xlsx' with the path to your .xlsx file
file_path = 'attractions.xlsx'

# Read the Excel file
df = pd.read_excel(file_path)

# Extract the '景点名称' and '网址' columns
site_names = df['景点名称'].tolist()
urls = df['网址'].tolist()

# # If you need to print the extracted data
# for name, url in zip(site_names, urls):
#     print(f'Site Name: {name}, URL: {url}')

for i in range(0, len(urls)):
    print(site_names[i])
