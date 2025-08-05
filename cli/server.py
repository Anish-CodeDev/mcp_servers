from mcp.server.fastmcp import FastMCP
import subprocess
from cli import encrypt_files,encrypt_file
import os
import shutil
from gemini import generate_pattern_for_file_names
from dotenv import load_dotenv
load_dotenv()
mcp = FastMCP('cli')

@mcp.tool()
def run_command_wrt_file(operator:str,filename:str):
    """
    This tool is used when the user wants to run a specific command with a specific file name or a specific instruction
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
    folder = os.getcwd() + '\\' +  folder + '\\'
    if not os.path.exists(folder):
        return "The folder specified does'nt exist"
    key = encrypt_files(folder,extension)
    with open("env/key.env",'w') as f:
        f.write(f"ENCRYPTED_KEY={key.decode()}\n")
    return "Done"

@mcp.tool()
def encrypt_file_tool(folder:str,file_name:str):
    """
    This tool is used when the used when the user wants to encrypt a specific file by mentioning the filename to be encrypted
    ARGS: folder,file_name
    """
    path = os.getcwd() + '\\' +  folder + '\\' + file_name
    if not os.path.exists(path):
        return "The folder specified does'nt exist"
    
    key = encrypt_file(path)
    with open(os.getcwd() + '\\' +  folder + '\\' + 'key.env','w') as f:
        f.write(f"ENCRYPTED_KEY={key.decode()}\n")
    return "Done"

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
        os.rename(os.path.join(os.getcwd(),path),new_name)
    
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
    
mcp.run(transport='stdio')