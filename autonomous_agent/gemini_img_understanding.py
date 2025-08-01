from google.genai import types
from google import genai
import re
import os
client = genai.Client(api_key='AIzaSyCFJ3RwiHvLTy9QYMhraasRH1D3h7zZ2G0')
def extract(ques):

    with open('./screenshots/img.jpg','rb') as f:
        images_bytes = f.read()

    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            types.Part.from_bytes(
                data=images_bytes,
                mime_type='image/jpeg'
            ),
            f"""{ques}, don't include any other details"
            """
        ]
    )

    print(response.text)
    return response.text

def select_best_rated_hotels(choice:str):
    with open('screenshots/img.jpg','rb') as f:
         img_1 = f.read()
    with open('screenshots/img_1.jpg','rb') as f:
         img_2 = f.read()
    with open('screenshots/img_2.jpg','rb') as f:
         img_3 = f.read()
    with open('screenshots/img_3.jpg','rb') as f:
         img_4 = f.read()
    with open('screenshots/img_4.jpg','rb') as f:
         img_5 = f.read()
    with open('screenshots/img_5.jpg','rb') as f:
         img_6 = f.read()

    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            types.Part.from_bytes(
                data=img_1,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_2,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_3,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_4,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_5,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_6,
                mime_type='image/jpeg'
            ),
            f"""
            From the images given to you select the hotel which is {choice}, select only one hotel.
            Return the final result in the form a list, the first element is the name of the hotel, the second one is the cost.
            Just return the list and not anything else.
            """
        ]
    )   
    return eval(response.text)

def extract_no_of_members(num_members:int):
    with open('screenshots/num_members.jpg','rb') as f:
         img_bytes = f.read()
    
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            types.Part.from_bytes(
                 data=img_bytes,
                 mime_type='image/jpeg'
            ),
            f"From the image provided by how many times must the no of adults be incremented to match {num_members}, do not provide any additional information, give the response as a number"             
        ]
    )
    print(response.text)
    return int(response.text)

def extract_no_of_rooms(num_rooms:int):
    with open('screenshots/num_members.jpg','rb') as f:
         img_bytes = f.read()
    
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            types.Part.from_bytes(
                 data=img_bytes,
                 mime_type='image/jpeg'
            ),
            f"From the image provided by how many times must the no of rooms be incremented to match {num_rooms}, do not provide any additional information, give the response as a number"             
        ]
    )
    print(response.text)
    return int(response.text)

def checkIfMonthSatisfiesCheckInCheckOut(checkInMo,checkOutMo):
    with open('screenshots/dates.jpg','rb') as f:
         img_bytes = f.read()
    
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            types.Part.from_bytes(
                 data=img_bytes,
                 mime_type='image/jpeg'
            ),
            f"Are the names of the months {checkInMo} and {checkOutMo} present in the image, responsd with a yes or no with no explanation."
        ]        
    )
    return response.text


def extract_placeholder(ques,path:str):

    with open(path,'rb') as f:
        images_bytes = f.read()

    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            types.Part.from_bytes(
                data=images_bytes,
                mime_type='image/jpeg'
            ),
            f"""{ques}, don't include any other details"
            """
        ]
    )

    print(response.text)
    return response.text

def select_best_item(criterion):
    with open('screenshots/shopping/img.jpg','rb') as f:
         img_1 = f.read()
    with open('screenshots/shopping/img_1.jpg','rb') as f:
         img_2 = f.read()
    with open('screenshots/shopping/img_2.jpg','rb') as f:
         img_3 = f.read()
    with open('screenshots/shopping/img_3.jpg','rb') as f:
         img_4 = f.read()
    with open('screenshots/shopping/img_4.jpg','rb') as f:
         img_5 = f.read()
    with open('screenshots/shopping/img_5.jpg','rb') as f:
         img_6 = f.read()
    with open('screenshots/shopping/img_6.jpg','rb') as f:
         img_7 = f.read()
    
    with open('screenshots/shopping/img_7.jpg','rb') as f:
         img_8 = f.read()
    
    with open('screenshots/shopping/img_8.jpg','rb') as f:
         img_9 = f.read()
    
    with open('screenshots/shopping/img_9.jpg','rb') as f:
       
        img_10 = f.read()
    
    with open('screenshots/shopping/img_10.jpg','rb') as f:
        img_11 = f.read()
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=[
            types.Part.from_bytes(
                data=img_1,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_2,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_3,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_4,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_5,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_6,
                mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                data=img_7,
                mime_type='image/jpeg' 
            ),
            types.Part.from_bytes(
                 data=img_8,
                 mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                 data=img_9,
                 mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                 data=img_10,
                 mime_type='image/jpeg'
            ),
            types.Part.from_bytes(
                 data=img_11,
                 mime_type='image/jpeg'
            ),
            f"""
            From the images uploaded, select the best item according to the {criterion}, do not include any additional in
            Just return the header of the item. Just give one best item as the output. Also only select items which are in stock.
            """
        ]
    )   
    return response.text

def extract_field_names():
    img_bytes_list = []
    for i in range(len(os.listdir('./screenshots/forms'))):
         with open(f'screenshots/forms/img_{i+1}.jpg','rb') as f:
              img_bytes_list.append(f.read())
    img_parts = [types.Part.from_bytes(data=img_bytes,mime_type='image/jpeg') for img_bytes in img_bytes_list]
    response = client.models.generate_content(
         model='gemini-2.5-flash-lite',
         contents=[   
         img_parts,
         "From the uploaded images, extract the names of the fields of the form. Return the names of the extracted fields which are seperated from commas"
         ]
    )
    
    print(response.text)
    return response.text

def extract_info_for_list_of_fields(fields_list,args):
     res =  client.models.generate_content(
         model='gemini-2.5-flash-lite',
         contents=[
              f"""
                You are given with a list of fields: {fields_list}, your job is to extract information for those fields from the message enclosed within triple backticks
                ```{args}```
                Return the inputs for those fields as a list in the same order of the fields in the {fields_list} list.
                In the final response donot include triple backticks
              """
         ]
     )
     print(type(eval(res.text)))
     return eval(res.text)
#extract_info_for_list_of_fields(['Name', ' Email', ' Address', ' Phone number'],'My name is Anish, my email address is abc@xyz.com, my address is ABC,Bengaluru. My phone number is 1234567892')