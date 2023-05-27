# ChatBot API for Mental Counseling Session

This program utilizes the ChatGPT API to create an empathetic assistant for professional mental counselors in a mental counseling session. The program is designed to engage with clients who are seeking mental help and ask them 25 empathy curious deep open-ended questions to get more specific information about their problem. 

To run the program, please follow these steps:
1. Install the necessary requirements by running `pip install -r requirements.txt`
2. Run the program using `python chat_gradio.py`

## How to Use the Program

Once the program is running, the ChatBot will greet the client and ask them what brings them to counseling. From there, the ChatBot will ask 25 open-ended questions to gather information about the client's mental state and problem. 

It is important to note that the ChatBot is not intended to provide advice or suggestions to the client. Instead, the purpose of this conversation is to gather client information so that the real therapist can provide suggestions. 

After each answer, the ChatBot will show empathy without mentioning therapy. Please do not repeat questions or answers. 

The conversation will end with the ChatBot asking the client if they have any other concerns before reminding them that the program is here to support them. To close the session, the ChatBot will say "Goodbye!" 

Once the conversation has concluded, the user can click the "Finish conversation" button, and the program will print a short summary of the client's mental issue from the conversation. The summary will be within 250 words.

## Demo with Gradio

To make it easier for users to interact with the ChatBot, the program is integrated with Gradio. Gradio is a user-friendly tool that allows users to test the program's functionality in real-time. 

To use the Gradio demo, simply run the program and click the link that appears in the console. This will open the Gradio interface, where you can start the conversation with the ChatBot. 

Once the conversation is complete, you can click the "Finish conversation" button, and the program will display a short summary of the client's mental issue. 

## Disclaimer

It is important to note that this program is not intended to replace professional mental health counseling. It is merely a tool to assist mental health professionals in gathering information about their clients. If you are experiencing mental health issues, please seek professional help from a licensed therapist or counselor.
