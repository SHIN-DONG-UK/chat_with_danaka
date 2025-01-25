import os
import pygame

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()

    def play_audio(self, file_path):
        """음성 파일 재생"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # 재생이 끝날 때까지 대기
        while pygame.mixer.music.get_busy():
            continue

        # 재생 완료 후 정지
        pygame.mixer.music.stop()
        print(f"Playback completed for {file_path}")
