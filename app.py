import os
import openai
import gradio as gr
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# Define the initial prompt
prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return response.choices[0].text.strip()

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history

def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Sorry, I couldn't understand that."
        except sr.RequestError:
            text = "Sorry, there was an error with the speech recognition service."
    return text

def tts_output(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
    return text

with gr.Blocks() as block:
    gr.Markdown("<h1><center>Build Your Own Voice-Enabled ChatGPT with OpenAI API & Gradio</center></h1>")
    chatbot = gr.Chatbot()
    state = gr.State()
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(placeholder="Type your message here...")
            submit_text = gr.Button("Send Text")
        with gr.Column():
            audio_input = gr.Audio(source="microphone", type="filepath")
            submit_audio = gr.Button("Send Audio")
    submit_text.click(chatgpt_clone, inputs=[text_input, state], outputs=[chatbot, state])
    submit_audio.click(transcribe_audio, inputs=audio_input, outputs=text_input)
    submit_audio.click(chatgpt_clone, inputs=[text_input, state], outputs=[chatbot, state])
    submit_audio.click(tts_output, inputs=chatbot, outputs=None)

block.launch(debug=True)
