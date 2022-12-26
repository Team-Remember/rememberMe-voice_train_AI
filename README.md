## 음성 학습 파이프라인
![voice pipeline](https://github.com/Team-Remember/rememberMe-voice_train_AI/blob/main/img/voice%20pipeline.png)
- 모델 : Fast speech2
- 개인별 목소리 학습 파이프 라인으로 학습이 완료된 checkpoint는 google cloud storage에서 관리합니다.
- 개인별 checkpoint는 추론시에 로드되어 사용됩니다.
- 학습을 위한 목소리는 google api의 stt를 사용하여 음성을 텍스트로 변환합니다.
- 텍스트 스크립트와 음성파일을 통하여 학습되며 약 3000개의 문장을 5시간 정도 학습한 결과는 다음과 같습니다.<br>
[리멤버팀 정말 감사합니다.](https://github.com/Team-Remember/rememberMe-voice_train_AI/blob/main/img/remember%20team%20thankyou.wav)