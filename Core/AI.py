
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
from Core.Memo.last_memory import load_memory,save_conversation
from Core.Memo.summery import get_table_data

locations = location()
client = Groq(api_key="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")

MODEL = "deepseek-r1-distill-llama-70b"

def massage(prompt,person):
    with open("Core/Memo/person_report.txt", "r") as file:
        person_report = file.read()
    with open(r'VisualIntelligence\output.txt', "r") as file:
        env_report = file.read()


    system_message = {
        "role": "system",
        "content": (
            "Your name is AiTOMM (pronounced as Atom). Answer in simple sentences with in 30 words."
            f"Genaral User Report: {person_report} if he/she is an stranger and the environmental decribtion is {env_report}."
            f"Location is {locations} and adapt to the local culture and its Current Date and Time is {datetime.now()} & {temparature()}."
        ),
    }

    messages = [system_message]  
    messages.extend(load_memory(person))
    # print("last 5:", messages)
    messages.extend(relamemo(person,prompt))
    # print("\nrelated:", messages)

    messages.append({'role': 'user', 'content': prompt})
    #print(messages)
    return messages


def core(prompt, person):
    print("<=- CHORE -=>")

    try:
        messages = massage(prompt,person)
        response = client.chat.completions.create(
            messages= messages,
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
        # Count occurrences
        counter = Counter(person_list)
        most_common_person, count = counter.most_common(1)[0]  # Get the most common item and its count
        new_person = most_common_person

    # Check if the person has changed
    if not hasattr(mainframe, "last_person"):
        mainframe.last_person = None
    if mainframe.last_person != new_person:
        get_table_data([new_person])
        mainframe.last_person = new_person

    print(f"<=----------------------- {new_person} : {text} -----------------------------=>")
    response = core(text, new_person)
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    save_conversation(new_person, text, response)
    return response


if __name__ == "__main__":
    test_prompt = "Genarate a file for an LLM exicution"
    response = mainframe(test_prompt)
    print(response)
