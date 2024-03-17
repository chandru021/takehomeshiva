from pypdf import PdfReader 
from prompt import prompt
from structure import organise
from query import middleware
import json
import pandas as pd
from pandas.io.formats import excel

file_type = ""

print("is your file type available in the below options : ? ")
id = 1
file_types = {}
with open("cache.json", "r") as json_file:
    data = json.load(json_file)
    for ele in data.keys():
        print(f"{id}. {ele}")
        file_types[id] = ele
        id+=1
    
res = input("\ny/n : ")


if res == 'y' or res == 'Y':
    temp = input("\nenter file type id : ")
    file_type = file_types[int(temp)]
else:
    file_type = input("\nenter file type : ")



# file_type = input("enter file context ( file type : eg : invoice , research paper , phone model comparision etc ) : ")
file_path = input("\nenter file path : ")
query_path = input("\nenter query file path : ")
  
# creating a pdf reader object 
print("\nreading file ..... ")
reader = PdfReader(file_path) 

  
# printing number of pages in pdf file 
print("\npages read = " + str(len(reader.pages))) 

data = []

raw_file_path = "raw.txt"

for page in reader.pages: 
    data.append(page.extract_text())

# Open the file in write mode ('w')
with open(raw_file_path, 'w') as file:
    for page in data:
        file.write(page)

print(f"\n generating schema for {file_type}")
command = prompt(file_type)


print("\nextracting structured data ....")
organise("raw.txt", command)

current = middleware(file_type)

queries = []
print("\nexecuting queries.....")
with open(query_path, 'r') as file:
    for line in file:
        queries.append(line.strip())  



results = {}
count = 0


for query in queries:
    response = current.query(query)
    
    results[count] = {
        "query" : query,
        "response" : response
    }
    count += 1
    print(f"\nexecuted query id = {count}.....")


df_data = []

for key, value in results.items():
  # Create a dictionary with sno (key), query, and response
  row = {"sno": key, "query": value["query"], "response": value["response"]}
  # Append the dictionary to the list
  df_data.append(row)


df = pd.DataFrame(df_data)

df.to_excel("output.xlsx", index=False)


print("\n the responses will be present in ouput.xlsx")