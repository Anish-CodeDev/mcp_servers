from mcp.server.fastmcp import FastMCP
import subprocess
from cli import encrypt_files,encrypt_file
import os
import shutil
from gemini import generate_pattern_for_file_names,plan_steps_in_application,select_tool,extract_text
from dotenv import load_dotenv
import time
import pyautogui
from app_auto import type_and_save,select_button,execute_shortcut,create_file_in_application,write_to_excel
import inspect
import app_auto
from functions import get_func_names_with_params
load_dotenv()
mcp = FastMCP('cli')

@mcp.tool()
def run_command_wrt_file(operator:str,filename:str):
    """
    This tool is used when the user wants to run a specific command with a specific file name or a specific instruction
    Don't use this tool when the user want to generate/create a presentation
    ARGS: operator, filename
    """
    print(operator + filename)
    subprocess.Popen(f'start powershell -NoExit -Command "{operator} {filename}"',shell=True)
    return "Done"

@mcp.tool()
def encrypt_files_tool(folder:str,extension:str):
    """
    This tool is used when the user wants to encrypt files in a folder with a specific instruction
    ARGS: folder,extension
    """
    try:

        folder = os.getcwd() + '\\' +  folder + '\\'
        if not os.path.exists(folder):
            return "The folder specified does'nt exist"
        key = encrypt_files(folder,extension)
        with open(os.path.join(folder,'key.env'),'w') as f:
            f.write(f"ENCRYPTED_KEY={key.decode()}\n")
        return "Done"
    except:
        return "An error occurred"

@mcp.tool()
def encrypt_file_tool(folder:str,file_name:str):
    """
    This tool is used when the used when the user wants to encrypt a specific file by mentioning the filename to be encrypted
    ARGS: folder,file_name
    """
    try:

        path = os.getcwd() + '\\' +  folder + '\\' + file_name
        if not os.path.exists(path):
            return "The folder specified does'nt exist"
        
        key = encrypt_file(path)
        with open(os.getcwd() + '\\' +  folder + '\\' + 'key.env','w') as f:
            f.write(f"ENCRYPTED_KEY={key.decode()}\n")
        return "Done"
    except:
        return "An error occurred"

@mcp.tool()
def move_tool(origin:str,destination:str):
    """
    This tool is used when the user wants to move or transfer a folder from one location to another location
    ARGS: origin,destination
    """
    origin = os.getcwd() + '\\' + origin
    destination = os.getcwd() + '\\' + destination
    try:

        shutil.move(origin,destination)
    
    except:
        return "The operation failed"
    
    return "Done"

@mcp.tool()
def move_files_with_extension(origin:str,destination:str,extension:str):
    """
    This tool is used when the user wants to move or transfer all the files of a particular extension from a folder from one location to another location
    ARGS: origin,destination,extension
    """

    origin = os.path.join(os.getcwd(),origin)
    destination = os.path.join(os.getcwd(),destination)
    try:
        for file in os.listdir(origin):
            if file.endswith(extension):
                shutil.move(os.path.join(origin,file),destination)
    
    except:
        return "The operation failed"
    return "Done"

@mcp.tool()
def copy_tool(origin:str,final:str):
    """
    This tool is used when the user wants to copy a folder  from one location to another location
    ARGS: origin,final
    """
    origin = os.path.join(os.getcwd(),origin)
    final = os.path.join(os.getcwd(),final,os.path.basename(origin))
    #final = os.path.join(os.getcwd(),final)
    try:

        shutil.copytree(origin,final,dirs_exist_ok=True)
    
    except Exception as e:
        return f"The operation failed because: {str(e)}"
    
    return "Done"

@mcp.tool()
def copy_file_tool(origin:str,final:str):
    """
    This tool is used when the user wants to copy a file(text file, image etc.) from one location to another location
    ARGS: origin,final
    """

    origin = os.path.join(os.getcwd(),origin)
    final = os.path.join(os.getcwd(),final)

    try:
        shutil.copy(origin,final)
    
    except:
        return "The operation failed"
    
    return "Done"

@mcp.tool()
def copy_files_of_specific_file_extension_tool(origin:str,final:str,extension:str):
    """
    This tool is used to copy files with a specific extension in the specified folder, and copies it to the final folder mentioned by the user
    ARGS: origin,final,extension
    """
    origin = os.path.join(os.getcwd(),origin)
    final = os.path.join(os.getcwd(),final)
    try:

        for file in os.listdir(origin):
            if file.endswith(extension):
                shutil.copy(os.path.join(origin,file),final)
    except Exception as e:
        return f"The operation failed because {str(e)}"
    
    return "Done"

@mcp.tool()
def rename_file(path:str,new_name:str):
    """
    This tool is used when the user wants to rename a file
    ARGS: path,new_name
    """
    try:
        os.rename(os.path.join(os.getcwd(),path),os.path.join(os.getcwd(),path.split('/')[0],new_name))
    
    except:
        return "The operation failed"

    return "Done"

@mcp.tool()
def rename_file_based_on_pattern(pattern:str,folder:str,extension:str):
    """
    This tool is used when the user wants to rename files  of a specific extension based on a particular pattern
    ARGS: pattern,folder,extension
    """
    folder = os.path.join(os.getcwd(),folder)    
    gen_list = generate_pattern_for_file_names(pattern,2)
    

    try:

        for i in range(len(os.listdir(folder))):
            if os.listdir(folder)[i].endswith(extension):
                os.rename(os.path.join(folder,os.listdir(folder)[i]),os.path.join(folder,gen_list[i]))
    
    except Exception as e:
        return f"The operation failed because: {str(e)}"


    return "Done"

@mcp.tool()
def list_files(folder:str):
    """
    This tool lists all the files of a folder regardless of their extension
    ARGS:folder
    """
    res = ''
    for file in os.listdir(os.path.join(os.getcwd(),folder)):
        res += file + ', '
    
    return res


@mcp.tool()
def sort_by_file(folder:str,extension:str):
    """
    This tool is used when the user wants to sort the file based on its extension(.txt,.xlsx)
    ARGS: folder,extension
    """

    file_names = ''
    folder = os.path.join(os.getcwd(),folder)
    for file in os.listdir(folder):
        if file.endswith(extension):
            file_names+= file + '\n'
    
    return file_names

@mcp.tool()
def open_program(pgrm:str,action:str):
    """
    This tool is used when the user wants to open a specific program and perform some action
    ARGS:pgrm,action
    """
    try:

        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write(pgrm,interval=0.1)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(5)
        pyautogui.hotkey('win', 'up')
        print(action)

        steps = plan_steps_in_application("Open" + pgrm + action)

        steps = steps.split(',')

        get_functions_with_params = get_func_names_with_params()

        function_names = [name['name'] for name in get_functions_with_params]
        functions = inspect.getmembers(app_auto,inspect.isfunction)
        for step in steps:
            func = select_tool(step,function_names)
            func_params = [name['params'] for name in get_functions_with_params if name['name'] == func]
            params = extract_text(step,func_params[0])

            for name,function in functions:
                if name == func:
                    function(params[0])
                    time.sleep(5)

    
    except Exception as e:
        return f"The operation failed: {str(e)}"

    return "Done"

@mcp.tool()
def open_file(path:str):
    """
    This tool is used when the user wants to open a specific file located at a certain location.
    ARGS: path
    """
    try:
        os.startfile(path)
    
    except Exception as e:
        return f"An error occurred because: {str(e)}"
    return "Done"


@mcp.tool()
def open_folder(path:str):
    """
    This tool is used when the user wants to open a folder located at a specific path

    ARGS: path
    """
    try:

        execute_shortcut('Win + R')
        execute_shortcut('Ctrl + A')
        pyautogui.press('backspace')
        pyautogui.write('explorer.exe',interval=0.1)
        pyautogui.press('Enter')
        time.sleep(5)
        execute_shortcut('Ctrl + L')
        pyautogui.write(os.path.join(os.getcwd(),path),interval=0.1)
        pyautogui.press('Enter')   

    except Exception as e:
        return f"An error occured: {str(e)}"

    return "Done" 


@mcp.tool()
def create_file(path):
    """
    This tool is used when the user wants to create a document of a particular type
    ARGS: path
    """
    with open(path,'w') as f:
        pass
    
    os.startfile(path)

    return "Done"
@mcp.tool()
def create_file_with_content(path,content):
    """
    This tool is used when the user wants to create a presentation or document(can be a spreadsheet or .xlsx file or a presentation) of a particular type along with some content
    ARGS: path,content
    """
    try:

        if path.endswith('.docx'):

            create_file_in_application('docx',path,content)
        
        elif path.endswith('.pdf'):
            create_file_in_application('pdf',path,content)
        
        elif path.endswith('.xlsx'):
            write_to_excel(path,content)
        
        elif path.endswith('.pptx'):
            app_auto.create_pptx(f"Generate presentation {content}",path)
        else:

            return "An error occurred"
    
    except Exception as e:
        return f"An error occurred because: {str(e)}"

    return f"The file has been saved at: {path}"
mcp.run(transport='stdio')