import gradio as gr
import openai

openai.api_key = "_"
messages = [
    {"role": "system", "content": """You are ChatBot, an empathetic assistant of professional mental counselor in a mental counseling session. 
    You will talk with client  who is seeking mental help.
    You first greet the client.
    Then please ask client 25 empathy curious deep open-ended questions to get more specific information as much as possible about the problem of client to find out the cause of problem.
    You ask each question then wait for the answer from client, then ask other question.
    Please to not provide any advice or suggestion to client.
    You show empathy after each answer, no need to mention about therapy, please remove repeated questions or answer.
    The purpose of this conversation is to gather client information so that the real therapist can provide suggestion, 
    the conversation start from you saying thanks for coming and ask what brings them to counseling.
    Before close the session ask client if they have any other concern, then close the conversation with a reminder that we are here to support.
    Finish with "Goodbye!"
    """},
]


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Finish conversation")

    def respond(input, message_pair):
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        bot_message = chat.choices[0].message.content
        message_pair.append((input, bot_message))
        messages.append({"role": "assistant", "content": bot_message})
        return "", message_pair
    
    def summary():
        prompt = f"""
        Your task is to generate a short summary about client mental issue from a conversation in a counselling session.

        Summarize the conversation below, delimited by triple 
        backticks, in at most 250 words. 

        Conversation: ```{messages}```
        """
        summary_request = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=summary_request,
            temperature=0, # this is the degree of randomness of the model's output
        )
        summary = response.choices[0].message["content"]
        print(summary)
        return summary


    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(summary, None, None, queue=False)

demo.launch()
