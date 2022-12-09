import os
import time
import boto3
from app import config
from app.before_mfa_voice_train import move_file, write_script, audio_text_pair


def voice_train_process(request_data):
    start = time.time()
    # ec2에서 음성 데이터 다운로드
    voice_path_list = request_data['voicePathList']
    s3 = boto3.client('s3', aws_access_key_id=config.AWS_CONFIG['aws_access_key_id'],
                      aws_secret_access_key=config.AWS_CONFIG['aws_secret_access_key'])

    for index, path in enumerate(voice_path_list):
        path_url = path['voicePath']
        s3.download_file(config.AWS_CONFIG['bucket_id'], 'voice/' + path_url.split('/')[4], f"./voice/{index}.wav")

    # before mfa
    voice_path = './voice/'
    move_file(voice_path)
    write_script(voice_path + 'script.txt', voice_path)  # 음성파일 있는 폴더에 넣지 말고 분리해서 만들고->음성폴더 있는곳에 넣기
    script_file = "script.txt"  # 스크립트 파일명
    audio_text_pair(voice_path + script_file)
    # mfa

    # after mfa
