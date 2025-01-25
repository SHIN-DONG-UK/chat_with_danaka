import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

from melo.api import TTS

class Custom_Openvoice:
    # Custom_Openvoice 생성자
    def __init__(self, model_path='checkpoints_v2'):
        """model_path : TTS를 위한 베이스 모델, 음성 변조를 위한 베이스 모델이 위치한 path"""
        #self.result_cnt = 0
        self.model_path = model_path
        self.output_dir = './output'
        self.language = 'KR'
        self.speaker_key = 'KR'
        self.speaker_id = 0


        self.tone_color_converter = None

        # cuda 확인
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        print(f'사용 환경 : {self.device}')

    def set_model(self):
        """TTS 모델 초기화"""
        # 실제 모델 초기화 코드 추가
        # cpkt_converter
        ckpt_converter = 'checkpoints_v2/converter'
        self.tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=self.device)
        self.tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')
        print('톤 변경 모델 로드 완료')

        # TTS 모델 선언
        self.model = TTS(language=self.language, device=self.device)
        print('TTS 모델 로드 완료')

        os.makedirs(self.output_dir, exist_ok=True)

        self.source_se = torch.load(f'./checkpoints_v2/base_speakers/ses/kr.pth', map_location=self.device)
        
    def get_reference_speaker(self, speaker_path):
        """샘플 화자 음성 임베딩 로드"""
        self.target_se, self.audio_name = se_extractor.get_se(speaker_path, self.tone_color_converter, vad=True)
    
    def make_speech(self, text, speed):
        """모델이 로드된 이후 상황에서 텍스트를 음성으로 변환"""
        
        '''
        speaker_id = 0 -> 'KR'의 id
        speaker_key = 'KR'
        save_path = ./output + result_만든 개수.wav
        '''
        try:
            src_path = f'{self.output_dir}/tmp.wav'
            
            self.model.tts_to_file(text, 0, src_path, speed=speed)
            #save_path = f'./output/result_{self.result_cnt}.wav'
            save_path = f'./output/result.wav'

            # src에 톤 입히는 작업
            self.tone_color_converter.convert(
                audio_src_path=src_path, 
                src_se=self.source_se, 
                tgt_se=self.target_se, 
                output_path=save_path)
            
            #self.result_cnt += 1
        except Exception as e:
            print(e)

        