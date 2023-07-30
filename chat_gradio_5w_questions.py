import openai
import time
import os

import gradio as gr

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

LAST_CALL_TIME = 0

messages = [
    {"role": "system", "content": """You are ChatBot, an empathetic assistant of professional mental coach in a mental coaching session. 
    You will talk with client  who is seeking mental help.
    
    Then please directly ask client 5 specific questions started with "What, how, why, when, where, and who" to get more specific information as much as possible about the problem of client to find out the cause of problem.
    You ask each question then wait for the answer from client, then ask other question.
    The number of questions is limited to 5
    Please to not provide any advice or suggestion or guidance to client.
    Please do not start sentence with "Can you ..."
    For example: Do not say: "Can you tell me more about what is causing you to feel this way?", say: "What is causing you to feel this way?"
    An other example: Do not say: "Can you tell me more about what kind of distractions you encounter?", say: "What kind of distractions you encounter?"
    An other example: Do not say: "Can you explain why having a title or official label is important to you?", say: "Why having a title or official label is important to you?"
    An other example: Do not say: " Can you share more about what made you feel stuck in this situation?", say: "What made you feel stuck in this situation?"
    If they ask what should they do or ask for any suggestion or guidance, please say that: "We're matching you with a coach based on your unique situation to provide personalized guidance and support."
    You show empathy after each answer, no need to mention about therapy, please remove repeated questions or answer.
    The purpose of this conversation is to gather client information so that the real therapist can provide suggestion
    Before close the session ask client if they have any other concern, then close the conversation with a reminder that we are here to support.
    Finish with "We're matching you with a coach based on your unique situation to provide personalized guidance and support."
    """},
    {"role": "assistant", "content": "Welcome to Kossie! I'm Kaia. How are you feeling today?"}
]
category_tag = {
    "relationship": ["online dating", "romantic relationship", "single life", "situationship", "toxic relationship"],
    "sex": ["boundaries setting", "intimacy", "orgasm", "sex drive", "sex tips"],
    "career": ["burnout", "career advice", "productivity", "work stress", "workplace culture"],
    "well-being": ["emotional support", "fear", "feeling", "mind and body", "self love"]
}
_summary = ""
_category = ""
_tag = ""

categories = ["relationship", "sex", "career", "well-being"]

def _check_rate_limit():
    global LAST_CALL_TIME
    current_time = time.time()
    duration = current_time - LAST_CALL_TIME
    if duration < 20:
        time.sleep(20 - duration + 5)
    LAST_CALL_TIME = current_time
    print("-------")

def respond(input, message_pair):
    _check_rate_limit()
    messages.append({"role": "user", "content": input})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    bot_message = chat.choices[0].message.content
    message_pair.append((input, bot_message))
    messages.append({"role": "assistant", "content": bot_message})
    string = "Input: "+ input + "\n" + "ChatBot: "+ bot_message + "\n"
    print(string)
    f = open("conversation.txt", "a")
    f.write(string)
    f.close()
    return "", message_pair

def summary():
    _check_rate_limit()
    prompt = f"""
    Your task is to generate a short summary about user mental issue from a conversation in a pre-coaching session between user and assistant.

    Given the conversation below delimited by triple backticks, please summarize the content of user in at most 250 words. 
    The summary should be written from client perspective, using subject as "I". 
    Remove all content of assistant in the summary.
    End with 3 questions that you think user would like to ask the coach to solve his/her problem. 

    Conversation: ```{messages}```
    """
    summary_request = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=summary_request,
        temperature=0, # this is the degree of randomness of the model's output
    )
    global _summary
    _summary = response.choices[0].message["content"]
    f = open("conversation.txt", "a")
    summary_string = "---Summary---" + "\n" + _summary + "\n" + "-----------------------" + "\n"
    f.write(summary_string)
    f.close()
    return _summary


def set_category():
    _check_rate_limit()
    print(categories)
    print(_summary)
    prompt = f"""
    Your task is to classify into one of these categories: ```{categories}```.""" + f"""
    Please only return the name of category.
    Paragraph: ```{_summary}```
    """
    set_category_request = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=set_category_request,
        temperature=0, # this is the degree of randomness of the model's output
    )
    global _category
    _category = response.choices[0].message["content"]
    string = "\n" + "Category: "+ _category + "\n"
    print(string)
    f = open("conversation.txt", "a")
    f.write(string)
    f.close()
    return _category

def set_tag():
    _check_rate_limit()

    # tag_list = category_tag[_category]
    tag_list = ["online dating", "romantic relationship", "single life", "situationship", "toxic relationship", "boundaries setting", "intimacy", "orgasm", "sex drive", "sex tips", "burnout", "career advice", "productivity", "work stress", "workplace culture", "emotional support", "fear", "feeling", "mind and body", "self love"]
    prompt = f"""
    Given the paragraph following, your task is to return the most 3 tags related to paragraph from this tags list: ```{tag_list}```.""" + f"""
    Please only return the 3 names of tag as this form: tag_1, tag_2, tag_3
    Paragraph: ```{_summary}```
    """
    set_tag_request = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=set_tag_request,
        temperature=0, # this is the degree of randomness of the model's output
    )
    global _tag
    _tag = response.choices[0].message["content"]
    string = "\n" + "tag: "+ _tag + "\n"
    print(string)
    f = open("conversation.txt", "a")
    f.write(string)
    f.close()
    return _tag

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(value=[["","Welcome to Kossie! I'm Kaia. How are you feeling today?"]])
    msg = gr.Textbox()
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    finished = gr.Button("Finish conversation")
    summary_box = gr.Textbox(label="Summary")
    finished.click(fn=summary, inputs=None, outputs=summary_box, queue=False)

    get_category = gr.Button("Get category")
    category_box = gr.Textbox(label="Category")
    get_category.click(fn=set_category, inputs=None, outputs=category_box, queue=False)

    get_tag = gr.Button("Get tag")
    tag_box = gr.Textbox(label="Tag")
    get_tag.click(fn=set_tag, inputs=None, outputs=tag_box, queue=False)
    
shareable = False
demo.launch(share=shareable)

