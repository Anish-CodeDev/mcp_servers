from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def generate_pattern_for_file_names(pattern,num_elements):

    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
        f"""
        The pattern is enclosed between triple backticks, you'll have to generate a list of {str(num_elements)} filenames  which will suit that pattern
        ```{pattern}``` of the type .txt
        Just include the filename generated and do not the name of provided pattern in the file name.
        Seperate the elements by using commas.

        Donot include any triple backticks in the final response
        """
        ]
    )
    print(res.text.split(','))
    print(res.text.split(',')[0])
    print(type(res.text.split(',')))
    return res.text.split(',')

#generate_pattern_for_file_names('The alphabets of english language',5)