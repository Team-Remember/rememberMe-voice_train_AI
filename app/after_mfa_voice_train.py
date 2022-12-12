import shutil,os
from distutils.dir_util import copy_tree
import subprocess
from Fastspeech2_Korean.preprocess import preprocess

def after_mfa():
    #mfa로 만든 text_grid zip파일로 만들기
    shutil.make_archive('mfa', 'zip', './mfa')

    #작업하고 있는 곳 Fastspeech2-Korean으로 변경하기
    os.system('cd Fastspeech2-Korean')

    ##preprocess.py 실행하기
    preprocess()

    ##zip해제한 파일들 경로 변경하기
    for num in range(1,5):
        copy_tree('./preprocessed/kss_part2/mfa/'+str(num), './preprocessed/kss_part2/mfa')

    ##preprocess.py 실행하기 -zip으로 만들기 전에 파일 옮겨서 오류 안나면 한 번에 하는게
    preprocess()

    ##train.py 실행하기
    os.system('!python train.py')