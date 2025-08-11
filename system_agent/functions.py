import app_auto
import inspect

functions = inspect.getmembers(app_auto,inspect.isfunction)

func_names = [name for name,_ in functions]

def get_func_names_with_params():

    arr =[]
    for name,func in functions:
        params = []
        sig = inspect.signature(func)
        for param_name,_ in sig.parameters.items():
            params.append(param_name)
        
        arr.append({"name":name,"params":params})
    
    

    return arr

#get_functions_with_params = get_func_names_with_params()
#func = 'select_button'
#print([name['params'] for name in get_functions_with_params if name['name'] == func][0])