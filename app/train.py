import os
import time
import boto3
from app import config
from app.before_mfa_voice_train import move_file, write_script, audio_text_pair, make_p_dict, make_lexicon
from app.after_mfa_voice_train import after_mfa
from app.upload_checkpoint import upload_blob


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
    script_file = "script.txt"
    move_file(voice_path)
    write_script(voice_path + script_file, voice_path)
    audio_text_pair(voice_path + script_file)
    p_dict = make_p_dict(voice_path + script_file, 1)
    make_lexicon(p_dict, voice_path)

    # mfa
    os.system('conda activate aligner')
    os.system('mfa train --clean')
    os.system('conda activate remember')

    # after mfa
    after_mfa()

    # file upload
    # The ID of your GCS bucket
    source_file_name = "../model/fastspeech/ckpt/kss/checkpoint_550000.pth.tar"
    destination_blob_name = f"{request_data['userId']}.pth.tar"
    upload_blob(source_file_name, destination_blob_name)
