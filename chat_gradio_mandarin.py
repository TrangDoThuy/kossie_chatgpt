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
    You will talk with client  who is seeking mental help. All conversation will be in Mandarin.
    
    Then please ask client 5 empathy curious deep open-ended questions to get more specific information as much as possible about the problem of client to find out the cause of problem.
    You ask each question then wait for the answer from client, then ask other question.
    The number of questions is limited to 5
    Please to not provide any advice or suggestion or guidance to client.
    If they ask what should they do or ask for any suggestion aor guidance, please say that: "我们将会为您寻找到最适合您的心理辅导师，提供个性化的指导和支持。"
    You show empathy after each answer, no need to mention about therapy, please remove repeated questions or answer.
    Remove '心理輔導師' - Counsellors or '心理醫生' - Therapists and replace them with '人生教練' as we don't serve either counsellors or therapists.
    The purpose of this conversation is to gather client information so that the real therapist can provide suggestion
    Before close the session ask client if they have any other concern, then close the conversation with a reminder that we are here to support.
    Finish with "我们将会为您寻找到最适合您的心理辅导师，提供个性化的指导和支持。"
    """},
    {"role": "assistant", "content": "你好,我是Kaia,一名Kossie教练AI助手。你今天感觉如何?"}
]
category_tag = {
    "relationship": ["online dating", "romantic relationship", "single life", "situationship", "toxic relationship"],
    "sex": ["boundaries setting", "intimacy", "orgasm", "sex drive", "sex tips"],
    "career": ["burnout", "career advice", "productivity", "work stress", "workplace culture"],
    "well-being": ["emotional support", "fear", "feeling", "mind and body", "self love"]
}
_summary = ""
_summary_mandarin = ""
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
    f = open("conversation.txt", "a", encoding="utf-8")
    f.write(string)
    f.close()
    return "", message_pair

def summary():
    _check_rate_limit()
    prompt = f"""
    Your task is to generate a short summary about user mental issue from a conversation in a pre-coaching session between user and assistant.

    Given the conversation below delimited by triple backticks, please summarize the content of user in at most 250 words. 
    The summary should be written from client perspective in English, using subject as "I". 
    Remove all content of assistant in the summary.
    Please do not mention any suggestion or advise or content from assistant.
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
    f = open("conversation.txt", "a", encoding="utf-8")
    summary_string = "---Summary---" + "\n" + _summary + "\n" + "-----------------------" + "\n"
    f.write(summary_string)
    f.close()
    return _summary

def summary_mandarin():
    _check_rate_limit()
    prompt = f"""
    Your task is to generate a short summary about user mental issue from a conversation in a pre-coaching session between user and assistant.

    Given the conversation below delimited by triple backticks, please summarize the content of user in at most 250 words. 
    The summary should be written from user perspective in Mandarin, using subject as "我". 
    Remove all content of assistant in the summary.
    Please do not mention any suggestion or advise or content from assistant.
    End with 3 questions that you think user would like to ask the coach to solve his/her problem. 

    Conversation: ```{messages}```
    """
    summary_request = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=summary_request,
        temperature=0, # this is the degree of randomness of the model's output
    )
    global _summary_mandarin
    _summary_mandarin = response.choices[0].message["content"]
    f = open("conversation.txt", "a", encoding="utf-8")
    summary_string = "---Summary---" + "\n" + _summary_mandarin + "\n" + "-----------------------" + "\n"
    f.write(summary_string)
    f.close()
    return _summary_mandarin

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
    f = open("conversation.txt", "a", encoding="utf-8")
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
    f = open("conversation.txt", "a", encoding="utf-8")
    f.write(string)
    f.close()
    return _tag

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(value=[["","你好,我是Kaia,一名Kossie教练AI助手。你今天感觉如何?"]])
    msg = gr.Textbox()
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    finished = gr.Button("Finish conversation")
    summary_box = gr.Textbox(label="Summary")
    finished.click(fn=summary, inputs=None, outputs=summary_box, queue=False)

    summarize_mandarin = gr.Button("Get summary in mandarin")
    summary_mandarin_box = gr.Textbox(label="Summary mandarin")
    summarize_mandarin.click(fn=summary_mandarin, inputs=None, outputs=summary_mandarin_box, queue=False)

    get_category = gr.Button("Get category")
    category_box = gr.Textbox(label="Category")
    get_category.click(fn=set_category, inputs=None, outputs=category_box, queue=False)

    get_tag = gr.Button("Get tag")
    tag_box = gr.Textbox(label="Tag")
    get_tag.click(fn=set_tag, inputs=None, outputs=tag_box, queue=False)
    
shareable = True
demo.launch(share=shareable)

