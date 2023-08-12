#파일을 다운 받는다.
import speech_recognition as sr
import os
import glob
import shutil
from jamo import h2j,hangul_to_jamo,j2hcj
from g2pk import G2p
import jamotools
import math
import tqdm

##폴더 만들기(4개로 분리)->파일을 분리해서 폴더별로 넣기
def move_file(path):
    # 해당 경로에 폴더를 4개 생성한다
    for i in range(1, 5):
        try:
            os.mkdir(path + "/" + str(i))
        except:
            pass

    file_list = []
    for file in os.listdir(path):
        if file.endswith('.wav'):
            file_list.append(file)

    n = math.ceil(len(file_list) / 4)
    #파일 개수/4 ->올림해서 폴더마다 넣을 파일 개수 정하기

    #개수에 맞게 파일 4개의 폴더로 분리해서 넣기
    result_list = []
    for i in range(0, len(file_list), n):
        result_list.append(file_list[i:i + n])

    for num in range(len(result_list)):
        for file in result_list[num]:
            shutil.move(path + file, path + str(num + 1) + '/' + file)
            #print('{} has been moved to new folder!'.format(file))

move_file(path) #내가 사용한 path = 'C:/Users/HP/Desktop/test/'

##STT활용해서 스크립트 작성하기(양식: 파일주소|스크립트 내용) *못 읽으면 다 인코딩 문제
def write_script(script_ad, path):
    script = open(script_ad,'w',encoding='UTF-8')

    for (path, dir, files) in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            #wav파일만 가져와서 stt만들고 스크립트까지 만들기
            if ext == '.wav':
                print("%s/%s" % (path, filename))
                AUDIO_FILE = "%s/%s" % (path, filename)
                r = sr.Recognizer() #패키지 사용
                with sr.AudioFile(AUDIO_FILE) as source:
                    audio = r.record(source)
                try:
                    result_sound = r.recognize_google(audio, language='ko-KR') #STT
                    #print("%s/%s" % (path, filename)+"|"+result_sound+'.')
                    script.write("%s/%s" % filename+"|"+result_sound+'.'+'\n',encoding='UTF-8') #경로 확인 한 번 필요 (스크립트 형식 ex: 1/2_0000.wav)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    script.close()

write_script('./script.txt', path) #음성파일 있는 폴더에 넣지 말고 분리해서 만들고->음성폴더 있는곳에 넣기
 #만약 돌렸을때 스크립트가 순서대로 잘 생기면 path경로에 script파일 제작

 ##wav&lab 파일 생성
def audio_text_pair(meta_path):

  with open(meta_path,"r", encoding='UTF-8') as m:
    for line in m:
      wav_path=line.split("|")[0] #wav 파일의 위치
      content=line.split("|")[1] #문장

      text_path=wav_path.replace("wav","lab")

      with open(os.path.join(base,text_path),"w", encoding='UTF-8') as t:
        t.write(content)

meta_name="script.txt" #스크립트 파일명
base="C:/Users/HP/Desktop/test/" #데이터가 분리돼서 들어간 곳
audio_text_pair(base+meta_name)

##lexicon.txt 파일 생성
# 한글 문장을 초/중/종성 형태로 분리, 단독 사용 안함
g2p = G2p()  # grapheme to phoneme

def jamo_split(content):
    content = g2p(content)
    jamo = h2j(content).split(" ")

    return jamo

## word_to_phoneme 딕셔너리 , lexiocn 파일을 만드는 함수
def make_p_dict(meta_path,position):

  p_dict={}

  with open(meta_path,"r") as f:
    for line in tqdm.tqdm(f.readlines()):
      line=line.rstrip()
      content=line.split("|")[position] #meta data 내의 텍스트가 기록된 위치
      word_list=content.split(" ")

      for idx,word in enumerate(word_list):
        print(word) #잘 들어갔는지 확인용
        if not word in p_dict.keys():
          p_dict[word]=" ".join(jamo_split(word)[0])

  return p_dict

p_dict=make_p_dict(base+meta_name,1)

def make_lexicon(p_dict):
  with open(path+"p_lexicon.txt","w") as f:
    for k,v in p_dict.items():
      f.write("{}\t{}\n".format(k,v))

make_lexicon(p_dict)