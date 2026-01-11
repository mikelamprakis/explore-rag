import os
import glob
from dotenv import load_dotenv
from pathlib import Path
import gradio as gr
from openai import OpenAI

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
MODEL = "gpt-4.1-nano"
openai = OpenAI()

knowledge = {}

def load_all_employees_data_from_files():
    filenames = glob.glob("knowledge-base/employees/*")
    for filename in filenames:
        name = Path(filename).stem.split(' ')[-1]
        with open(filename, "r", encoding="utf-8") as f:
            knowledge[name.lower()] = f.read()

def load_all_products_data_from_files():
    filenames = glob.glob("knowledge-base/products/*")
    for filename in filenames:
        name = Path(filename).stem
        with open(filename, "r", encoding="utf-8") as f:
            knowledge[name.lower()] = f.read()


SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""

def get_relevant_context_simple(message):
    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    words = text.lower().split()
    relevant_context = []
    for word in words:
        if word in knowledge:
            relevant_context.append(knowledge[word])
    return relevant_context  

# This is just a more pythonic way to write the above get_relevant_context_simple()
def get_relevant_context(message):
    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    words = text.lower().split()
    return [knowledge[word] for word in words if word in knowledge]   

def additional_context(message):
    relevant_context = get_relevant_context(message)
    if not relevant_context:
        result = "There is no additional context relevant to the user's question."
    else:
        result = "The following additional context might be relevant in answering the user's question:\n\n"
        result += "\n\n".join(relevant_context)
    return result

def chat(message, history):
    system_message = SYSTEM_PREFIX + additional_context(message)
    # With type="messages", history is already a list of OpenAI-style message dictionaries
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

if __name__ == "__main__":
    load_all_employees_data_from_files()
    # print(knowledge)
    # print(knowledge["lancaster"])
    load_all_products_data_from_files()
    # print(knowledge.keys())
    relevant_context = get_relevant_context_simple("Who is lancaster?")
    relevant_context = get_relevant_context("Who is Lancaster and what is carllm?")
    refined_relevant_context = additional_context("Who is Alex Lancaster?")
    print(refined_relevant_context)
    
    # Launch a UI to chat with the content via an LLM
    view = gr.ChatInterface(chat, type="messages").launch(inbrowser=True)