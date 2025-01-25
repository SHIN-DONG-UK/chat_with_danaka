import tkinter as tk
from gui.tts_gui import TTS_GUI
from gui.openai_gui import OpenAIChatApp

if __name__ == "__main__":
    root = tk.Tk()
    #app = TTS_GUI(root)
    app = OpenAIChatApp(root)
    root.mainloop()