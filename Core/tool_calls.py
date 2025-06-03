import json
import time

from Tools.youtube_controll import youtube  
from Tools.APPS import open_app
from Tools.Small_Functions import webpage
from Tools.write import write
from Tools.Whatsapp_controller import chat_handler
from Tools.update import update,image_update
from Tools.launch_imageGen import launch_third_terminal

AVAILABLE_FUNCTIONS = {
            "write": write,
            "update":update,
            "save_user_name":image_update,
            "open_app":open_app,
            
            "youtube": youtube,            
            "webpage":webpage,
            "chat":chat_handler,

            "Image_genarator": launch_third_terminal,

}

def load_system_tools(json_file_path: str):
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            tools = json.load(file)
        return tools
    except Exception as e:
        print(f"Error loading system tools from {json_file_path}: {e}")
        return []
    
SYSTEM_TOOLS = load_system_tools("Core/system_tools.json")  

def call_tool_with_retry(function, kwargs, max_retries=3, delay=1):

    attempts = 0
    while attempts < max_retries:
        try:
            return function(**kwargs)
        except Exception as e:
            attempts += 1
            print(f"Error calling {function.__name__} with {kwargs}: {e}. Retry {attempts}/{max_retries}")
            if attempts < max_retries:
                time.sleep(delay)
            else:
                return f"Error processing tool call after {max_retries} retries: {e}"

def process_tool_call(tool_call):

    try:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        result = call_tool_with_retry(AVAILABLE_FUNCTIONS[function_name], function_args)
        return tool_call.id, function_name, result
    except Exception as e:
        return tool_call.id, tool_call.function.name, f"Error processing tool call: {e}"