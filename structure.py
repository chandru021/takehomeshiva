from openai import OpenAI


def read_text_file(file_path):
    """Reads the content of a text file and returns it."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def query_gpt3(text_data,prompt):
    
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4",
        
        messages = [
    {"role": "system", "content": "Given instructions {prompt} , convert the raw data given by user to a structured json entirely"},
    {"role": "user", "content": f"data : {text_data}"}
]
     
    )
    response = completion.choices[0].message.content
    with open("structured.txt", 'w') as file:

        file.write(response)

def organise(file_path, prompt):

    
    text_data = read_text_file(file_path)

    query_gpt3(text_data, prompt)

