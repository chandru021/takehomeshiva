from openai import OpenAI
import json

data = {}


def present(file_type):
    with open("cache.json", "r") as json_file:
      global data
      data = json.load(json_file)
      return file_type in data.keys()



def prompt(file_type):

    if(present(file_type)):
       return data[file_type]





    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4",
        messages = [
            {"role": "system", "content": "Given a document type (e.g., invoice, email, news article) and a list of desired key information to extract (e.g., invoice number, date, author), generate a prompt that specifies the structure and content of a well-structured JSON format representing the extracted data from the corresponding raw text document. The prompt should focus on describing the desired JSON schema, including the necessary fields and their data types."},
            {"role": "user", "content": f"generate ONLY the prompt for document type : {file_type}"},
                    ]
        
    )
    response = completion.choices[0].message.content
    data[file_type] = response

    with open("cache.json", "w") as json_file:
      json.dump(data, json_file, indent=4)

    return response