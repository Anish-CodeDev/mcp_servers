import pandas as pd
import pyautogui
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image
import re
import base64
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

def get_coordinates(img_path,ele_name,ele_type='button'):
    img = Image.open(img_path)
    width = img.width
    height = img.height
    with open(img_path,'rb') as f:
        img_bytes = f.read()
    res = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
                data=img_bytes,
                mime_type='image/jpeg'
            ),
            f"""
              Given the image below, detect the UI {ele_type} labeled {ele_name}. Return the bounding box of the {ele_type} in normalized coordinates from 0 to 1000.
                Only include the most relevant {ele_name} {ele_type}, and no extra explanation.
                The final response must be a list with no triple backticks
            """
        ]   
    )
    print(res.text)
    res = eval(res.text)

    x_min,y_min,x_max,y_max = res[0],res[1],res[2],res[3]
    x_min = (x_min / 1000) * width
    y_min = (y_min / 1000) * height
    x_max = (x_max / 1000) * width
    y_max = (y_max / 1000) * height
    center_x = (x_min + x_max)/ 2
    center_y = (y_min + y_max)/2
    print("X: ",center_x)
    print("Y: ",center_y)
    return center_x,center_y

def extract_text(message,params):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            Your job is to extract information from the string enclosed using triple backticks, so that it fits it to the arguments of a given function: {params}
            The response must be a list containing the values to be passed to the function.
            ```{message}```
            """
        ]
    )
    print(res.text)
    return eval(res.text)
def plan_steps_in_application(message:str):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            Generate a step-by step interaction with a gui interface for an agent like a human would interact for the process enclosed by triple backticks

            ```{message}```

            Just include the steps and not any additional information.

            The steps planned must be the steps required after the application is opened(ie, Don't include open application, these operations are used after the application is ready to accept the user's interaction)
            Assume that the application is in its latest version
            Don't specify the reason why you are selecting the text,
            While generating the steps, instead of mentioning the steps mention the shortcuts instead if applicable

            Seperate the steps by comma(,) and don't include numbering
            """
        ]
    )
    print(res.text)
    return res.text

def select_tool(task,func_names_list):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
             Given that name of the functions are enclosed within triple backticks select the best function for the task: {task}
             ```{func_names_list}```

             Respond with the best function_name
            """
        ]
    )
    print(res.text)
    return res.text



def get_coordinates_of_textbox(path:str,placeholder:str):
    img = Image.open(path)
    width = img.width
    height = img.height
    with open(path,'rb') as f:
        img_bytes = f.read()
    
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
           
            f"""
            I will give you an image of my screen. In that image, find the input box that has placeholder: {placeholder}
                Return the bounding box of the suitable textbox in normalized coordinates from 0 to 1000.
                Do not explain your reasoning or include extra text.
                The final response must be in the form of a list: [x_min,y_min,x_max,y_max]

                I don't want the final output to be in the form of a json


                The x and y axis must point to the center of the textbox

            """,
             types.Part.from_bytes(
                data=img_bytes,
                mime_type='image/jpeg'
            ),
        ]
    )
    print(res.text)
    res = eval(res.text)
    x_min,y_min,x_max,y_max = res[0],res[1],res[2],res[3]
    x_min = (x_min / 1000) * width
    y_min = (y_min / 1000) * height
    x_max = (x_max / 1000) * width
    y_max = (y_max / 1000) * height
    center_x = (x_min + x_max)// 2
    center_y = (y_min + y_max)//2
    print("X: ",center_x)
    print("Y: ",center_y)       
    #pyautogui.click(center_x,center_y)
    return [center_x,center_y]

def select_best_placeholder(path,task):
    with open(path,'rb') as f:
        img_bytes = f.read()
    

    res = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=[
            types.Part.from_bytes(
                data=img_bytes,
                mime_type='image/jpeg'
            ),
            f"""
            From the  image provided to you, identify the textbox whose placeholder best matches the task described between triple backticks.
            ```{task}```
            Respond only with the exact placeholder text of that textbox which was selected by you,
            Do not include explanations, formatting, or any other text in your answer.,
            """,
            
            
        ]        
    )
    print(res.text)
    return res.text

def gen_pandas_df(content):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
          f""" Generate valid Python code that creates a pandas DataFrame for the following topic: {content}.

            Requirements:
            1. The DataFrame should be realistic and relevant to the topic.
            2. Include column names
            3. Don't include any python code snippets
            4. Return the final response in the form of json
            5. Don't include any triple backticks in the final response like (```)
            6. Don't include any null value
            """
        ]
    )
    

    res = eval(res.text)
    
    df = pd.DataFrame(res['data'])
    return df
def gen_presentation(topic:str):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
   f"""         You are an expert presentation creator. 
            Given a topic, generate a structured presentation outline suitable for PowerPoint or Google Slides.

            For the given topic:
            1. Provide a title slide with a main title, subtitle, and a suggestion for a visual.
            2. Create 8-10 additional slides.
            3. For each slide, include:
            - A short, clear slide title
            - 3-5 concise bullet points (presentation-friendly wording)
            - A suggestion for an appropriate visual or diagram
            4. Keep bullet points short and impactful, avoiding long sentences.
            5. Ensure the slides follow a logical flow, starting with an introduction and ending with a conclusion.
            6. The final response must be in the form of json, specify the title under the key title,slide title under the key slide_title, bullet points under the key bullet_points and visual suggestions under the key visual_suggestion
            7. Don't use any triple backticks in the final response
            Topic: {topic}
            """

        ]
    )
    res = re.sub('json','',res.text)
    
    res = eval(res)
    #print(res['slides'])
    print(res['slides'][0]['bullet_points'])
    return res

def generate_image(topic:str):
    res = client.models.generate_images(
        model='imagen-4.0-generate-preview-06-06',
        prompt=topic,
        config=types.GenerateImagesConfig(number_of_images=1)
    )
    for img in res.generated_images:
        img_encoded = base64.b64decode(img.image.base64_data)

        with open('test.png',"wb") as f:
            f.write(img_encoded)

        print('Success')

def get_rgb(color:str):
    res  = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            Get the RGB format for the colour enclosed using triple backticks
            ```{color}```
            Just return the response as a list and don't return any irrelevant text
            """
        ]
    )
    res = eval(res.text)
    print(res)
    return res


def extract_color_params(message):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            Extract the color of the background,slide title,content from {message}

            The final response must be a string, each of the results of the above params must be seperated by commas
            If not specified by the user, consider the content color and title color to be the same
            The response must be in lowercase
            """
        ]
    )
    print(res.text)
    return res.text
def extract_content(message):
    res = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            f"""
            Extract the topic from the message: {message}, return only the extracted topic
            """
        ]

    )
    print(res.text)
    return res.text
#extract_content('Generate a presentation of the topic AI Agents,the background must be in black, the text must be in white')
#extract_color_params('Generated a presentation on the topic AI Agents, the background must be in black, the text must be in white')
#generate_image('Applications of AI')
#for model in client.models.list():
#    print(model.name)