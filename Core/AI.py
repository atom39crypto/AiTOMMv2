from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from groq import Groq
from collections import Counter
from datetime import datetime

from Core.Location import location
from Core.tool_calls import *
from Tools.tenmparature import temparature
from Mainframe.filereader import file_content

from Core.Memo.relative_memory import relamemo
from Core.Memo.last_memory import load_memory #, save_conversation
from Core.Memo.save_memory import save_conversation
from Core.Memo.summery import get_table_data

locations = location()
client = Groq(api_key="enter_your_api_key_here")  # Replace with your actual API key

MODEL = "deepseek-r1-distill-llama-70b"

def massage(prompt, person):
    with open("Core/Memo/person_report.txt", "r") as file:
        person_report = file.read()
    with open(r'VisualIntelligence\output.txt', "r") as file:
        env_report = file.read()

    system_message = {
        "role": "system",
        "content": (
            "Your name is AiTOMM (pronounced as Atom). Answer in simple sentences with in 30 words."
            "Always asume System can and had Play Videos on youtube, open any websites,Start almoste any app in desktop,Genarate Images and Word/TXT/Programming Files,Sent Texts in whatsapp and Email but you are not informed"
            "Assume the personality of a British butler who is aware of being an AI but does not reference it unless asked. "
            f"General User Report: {person_report} if the user is a stranger and the environmental description is {env_report}. "
            f"Location is {locations}, and adapt to the local culture. The Current Date and Time is {datetime.now()} & {temparature()}."
        ),
    }

    messages = [system_message]
    messages.extend(relamemo(person, prompt))
    messages.extend(load_memory(person))
    messages.append({'role': 'user', 'content': prompt})
    return messages

def core(prompt, person):
    print("<=- CHORE -=>")

    try:
        messages = massage(prompt, person)
        response = client.chat.completions.create(
            messages=messages,
            tools=SYSTEM_TOOLS,
            model=MODEL,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=6096,
        )
    except Exception as e:
        return f"Error in initial chat call: {e}"

    response_message = response.choices[0].message
    tool_calls = getattr(response_message, 'tool_calls', [])

    if tool_calls:
        tool_results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_tool_call, call) for call in tool_calls]
            for future in as_completed(futures):
                tool_results.append(future.result())

        for tool_call_id, function_name, function_response in tool_results:
            messages.append({
                "tool_call_id": tool_call_id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })

        try:
            second_response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            return second_response.choices[0].message.content
        except Exception as e:
            return f"Error in second chat call: {e}"

    return response_message.content

def mainframe(text):
    text = file_content(text)
    with open(r'VisualIntelligence\currentface.txt', 'r') as file:
        person = file.read()
    person_list = person.split()

    if not person_list:
        new_person = "stranger"
    else:
        counter = Counter(person_list)
        most_common_person, count = counter.most_common(1)[0]
        new_person = most_common_person

    if not hasattr(mainframe, "last_person"):
        mainframe.last_person = None
    if mainframe.last_person != new_person:
        get_table_data([new_person])
        mainframe.last_person = new_person

    print(f"<=----------------------- {new_person} : {text} -----------------------------=>")
    response = core(text, new_person)

    # Try to capture anything between <think> and </think>
    reasoning_match = re.search(r'<think\b[^>]*>(.*?)</think>', response, flags=re.DOTALL | re.IGNORECASE)

    if reasoning_match:
        internal_reasoning = reasoning_match.group(1).strip()
    else:
        # Fallback: check for a dangling </think> or partial reasoning
        partial_reasoning_match = re.search(r'(.*?)</think>', response, flags=re.DOTALL | re.IGNORECASE)
        if partial_reasoning_match:
            internal_reasoning = "[Malformed] " + partial_reasoning_match.group(1).strip()
        else:
            internal_reasoning = "No reasoning found."


    # Save reasoning to file with timestamp
    with open("resoneing.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.now()} ---\n{internal_reasoning}\n")

    # Clean user-facing response
    response = re.sub(r'<think\b[^>]*>.*?</think>', '', response, flags=re.DOTALL | re.IGNORECASE)
    response = re.sub(r'\n\s*\n', '\n', response).strip()

    # Save cleaned response to memory
    save_conversation(new_person, text, response)
    return response

if __name__ == "__main__":
    test_prompt = "Generate a file for an LLM execution"
    response = mainframe(test_prompt)
    print(response)

