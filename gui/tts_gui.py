import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from modules.custom_openvoice import Custom_Openvoice
from modules.audio_player import AudioPlayer

class TTS_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TTS Demo")
        self.root.geometry("500x600")

        # 여기에 모델 갈아끼우면 될듯
        # 모듈 초기화
        self.tts_module = Custom_Openvoice()
        self.tts_module.set_model()

        self.audio_player = AudioPlayer()

        # GUI 요소 생성
        self.create_widgets()
        self.log("TTS System Initialized.")

    def create_widgets(self):
        """GUI 요소 생성"""
        # 샘플 화자 음성 파일 입력
        self.label_sample = tk.Label(self.root, text="Sample MP3 File:")
        self.label_sample.pack()
        self.entry_sample = tk.Entry(self.root, width=40)
        self.entry_sample.pack()
        self.btn_browse = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.btn_browse.pack()

        self.btn_load_sample = tk.Button(self.root, text="Load Sample Voice", command=self.load_sample_voice)
        self.btn_load_sample.pack()

        # 텍스트 입력
        self.label_text = tk.Label(self.root, text="Text for TTS:")
        self.label_text.pack()
        self.entry_text = tk.Entry(self.root, width=40)
        self.entry_text.pack()

        self.btn_generate_tts = tk.Button(self.root, text="Generate TTS", command=self.generate_tts)
        self.btn_generate_tts.pack()

        # TTS 음성 재생 버튼
        self.btn_play_tts = tk.Button(self.root, text="Play TTS", command=self.play_tts)
        self.btn_play_tts.pack()

        # 출력 창
        self.output_text = scrolledtext.ScrolledText(self.root, height=10, width=50)
        self.output_text.pack()

    def log(self, message):
        """출력창에 로그 메시지 추가"""
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)

    def browse_file(self):
        """샘플 음성 파일 선택"""
        file_path = filedialog.askopenfilename(
            title="Select MP3 File",
            filetypes=(("Audio files", "*.mp3;*.wav"), ("All files", "*.*"))
        )
        if file_path:
            self.entry_sample.delete(0, tk.END)
            self.entry_sample.insert(0, file_path)

    def load_sample_voice(self):
        """샘플 화자 음성 로드"""
        sample_path = self.entry_sample.get()
        if os.path.exists(sample_path):
            self.log(f"Loading sample voice from {sample_path}")
            self.tts_module.get_reference_speaker(speaker_path=sample_path)
            self.log("Sample voice loaded successfully.")
        else:
            messagebox.showerror("Error", "Sample MP3 file not found.")

    def generate_tts(self):
        """TTS 생성"""
        text = self.entry_text.get()
        if text:
            self.log(f"Generating TTS for text: {text}")
            threading.Thread(target=self._tts_thread, args=(text, 1.3,)).start()
        else:
            messagebox.showerror("Error", "Please enter text for TTS.")

    def _tts_thread(self, text, speed):
        """TTS 생성 비동기 작업"""
        try:
            self.tts_module.make_speech(text, speed)
            self.log("TTS generation completed.")
        except Exception as e:
            self.log(f"Error generating TTS: {e}")

    def play_tts(self):
        """TTS 음성 재생"""
        #tts_path = f'./output/result_{self.tts_module.result_cnt - 1}.wav'
        tts_path = f'./output/result.wav'
        try:
            self.log("Playing generated TTS.")
            self.audio_player.play_audio(tts_path)
            self.log("TTS playback completed.")
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
