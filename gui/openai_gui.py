import openai
import tkinter as tk
from tkinter import scrolledtext, messagebox
#import pyttsx3  # 음성출력 라이브러리
from modules.custom_openvoice import Custom_Openvoice
from modules.audio_player import AudioPlayer

'''OpenAI API key'''
openai.api_key = "your key"

class OpenAIChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenAI Chat")
        self.root.geometry("500x600")

        # tts moudle 초기화
        self.tts_module = Custom_Openvoice()
        self.tts_module.set_model()

        self.audio_player = AudioPlayer()
        self.tts_module.get_reference_speaker('./resources/danaka.wav')
        self.tts_module.make_speech('시작', 1.3)

        #self.engine = pyttsx3.init()
        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets"""
        self.label_input = tk.Label(self.root, text="Your Message:")
        self.label_input.pack()
        self.entry_input = tk.Entry(self.root, width=50)
        self.entry_input.pack(pady=5)
        self.btn_send = tk.Button(self.root, text="Send", command=self.send_message)
        self.btn_send.pack(pady=5)
        self.label_output = tk.Label(self.root, text="Conversation:")
        self.label_output.pack()
        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, width=60)
        self.output_text.pack(pady=10)

    def send_message(self):
        """Send user input to OpenAI API and display the response"""
        user_message = self.entry_input.get().strip()

        if not user_message:
            self.output_text.insert(tk.END, "Please enter a message.\n")
            self.output_text.see(tk.END)
            return

        self.output_text.insert(tk.END, f"You: {user_message}\n")
        self.output_text.see(tk.END)
        self.entry_input.delete(0, tk.END)

        # Call OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", 
                     "content" : "너는 로봇 집사야. 집 안에서 사용자의 명령을 수행하는 일을 하고 있어. 사용자와 대화도 가능해."},
                    {"role": "user", "content": user_message}],
            )
            bot_message = response.choices[0].message.content
            self.output_text.insert(tk.END, f"Bot: {bot_message}\n")
            self.output_text.see(tk.END)

            # 음성 출력
            self.speak(bot_message)

        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")
            self.output_text.see(tk.END)

    def speak(self, text):
        """텍스트를 음성으로 출력"""
        #self.engine.say(text)
        #self.engine.runAndWait()

        #tts_path = f'./output/result_{self.tts_module.result_cnt}.wav'
        tts_path = f'./output/result.wav'
        self.tts_module.make_speech(text, 1.3)
        try:
            self.audio_player.play_audio(tts_path)
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))