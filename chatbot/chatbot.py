import tkinter as tk
from tkinter import Text, END, DISABLED, NORMAL
from PIL import Image, ImageTk, ImageSequence
import pyttsx3
import speech_recognition as sr
import webbrowser
import asyncio
from threading import Thread
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os
import torch

# voice setup
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# conversational pipeline
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
chat_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
chat_history = []

# generate response with memory
def generate_response(query):
    global chat_history
    new_input_ids = tokenizer.encode(query + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat(chat_history + [new_input_ids], dim=-1) if chat_history else new_input_ids
    output = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    chat_history = [output]
    reply = tokenizer.decode(output[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return reply.strip()

# Speak response
def speak(text):
    engine.say(text)
    engine.runAndWait()

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis Assistant (Enhanced)")
        self.root.geometry("800x600")
        self.root.bind("<F2>", lambda e: Thread(target=self.listen_voice).start())

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.chat_log = Text(self.root, bg="#000000", fg="sky blue", font=("Consolas", 10), wrap='word', bd=0)
        self.chat_log.place(x=0, y=500, width=800, height=80)
        self.chat_log.insert(END, "[System] Type your command or press F2 to speak.\n")
        self.chat_log.config(state=DISABLED)

        self.entry = tk.Entry(self.root, font=("Segoe UI", 13), bg="#1a1a1a", fg="white", bd=3, insertbackground='white')
        self.entry.place(x=20, y=580, width=700, height=30)
        self.entry.bind("<Return>", self.send_text)

        send_button = tk.Button(self.root, text="Send", command=self.send_text, bg="#222222", fg="white", relief='flat')
        send_button.place(x=730, y=580, width=50, height=30)

        try:
            gif = Image.open("C:\\Users\\thekr\\Downloads\\AI material full\\jarvis.gif")
            frame_size = (800, 600)
            self.frames = [
                ImageTk.PhotoImage(img.resize(frame_size, Image.LANCZOS).convert('RGBA'))
                for img in ImageSequence.Iterator(gif)
            ]
            self.gif_index = 0
            self.bg_image = self.canvas.create_image(0, 0, anchor='nw', image=self.frames[0])
            self.animate()
        except FileNotFoundError:
            print("GIF not found. Using fallback.")
            self.canvas.create_rectangle(0, 0, 800, 600, fill="black")

    def animate(self):
        self.canvas.itemconfig(self.bg_image, image=self.frames[self.gif_index])
        self.gif_index = (self.gif_index + 1) % len(self.frames)
        self.root.after(100, self.animate)

    def send_text(self, event=None):
        user_input = self.entry.get()
        self.entry.delete(0, END)
        if user_input:
            self.add_text("You: " + user_input)
            Thread(target=lambda: asyncio.run(self.handle_command(user_input))).start()

    def add_text(self, text):
        self.chat_log.config(state=NORMAL)
        self.chat_log.insert(END, text + "\n")
        self.chat_log.config(state=DISABLED)
        self.chat_log.see(END)

    def listen_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.add_text("[Listening...]")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                self.add_text("You (Voice): " + command)
                asyncio.run(self.handle_command(command))
            except Exception as e:
                self.add_text("[Voice Error] " + str(e))

    async def handle_command(self, command):
        if "open" in command.lower():
            await self.open_any_website(command)
        elif "exit" in command.lower():
            self.add_text("[System] Exiting...")
            self.root.quit()
        else:
            response = generate_response(command)
            self.add_text("AI: " + response)
            speak(response)

    async def open_any_website(self, command):
        known_sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "instagram": "https://www.instagram.com",
            "chatgpt": "https://chat.openai.com",
            "github": "https://github.com",
            "spotify": "https://open.spotify.com"
        }
        for name, url in known_sites.items():
            if name in command.lower():
                self.add_text(f"AI: Opening {name}")
                await asyncio.to_thread(webbrowser.open, url)
                speak(f"Opening {name}")
                return
        self.add_text("AI: Website not recognized.")
        speak("Website not recognized.")

def main():
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()

if __name__ == "__main__": 
    main()