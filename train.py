import shutil
from distutils.dir_util import copy_tree

#mfa로 만든 text_grid zip파일로 만들기
shutil.make_archive('mfa', 'zip', '/home/hoeeun/kss_part2/mfa')

#작업하고 있는 곳 Fastspeech2-Korean으로 변경하기
cd Fastspeech2-Korean

##preprocess.py 실행하기
!python preprocess.py

##zip해제한 파일들 경로 변경하기
for num in range(1,5):
  copy_tree('./preprocessed/kss_part2/mfa/'+str(num), './preprocessed/kss_part2/mfa')

##preprocess.py 실행하기 -zip으로 만들기 전에 파일 옮겨서 오류 안나면 한 번에 하는게
!python preprocess.py

##train.py 실행하기
!python train.py