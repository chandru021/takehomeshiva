from openai import OpenAI

class middleware():

    def __init__(self, file_type):

        self.structured_data_str = ""
        with open('structured.txt', 'r') as file:
            self.structured_data_str = file.read()
        self.file_type = file_type
        self.client = OpenAI()

    
    def query(self, query):
        prompt = f"Given the following {self.file_type} data:\n{self.structured_data_str}\n\nBased on this data, {query}"
        completion = self.client.chat.completions.create(
        model="gpt-4",
        messages=[
        {"role": "user", "content": f"{prompt}"}
        ]
        )
        response = completion.choices[0].message.content
        return response
        # with open("response.txt", 'a+') as file:
        #     file.write(response + "\n")



