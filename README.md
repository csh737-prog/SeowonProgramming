# 너와 나의 유전자 🧬

선택에 따라 호감도와 엔딩이 달라지는 한국어 비주얼 노벨 프로토타입입니다.
Python과 Streamlit으로 실행합니다.

## 파일 구성

- `main.py`: 게임 코드
- `requirements.txt`: 실행에 필요한 라이브러리
- `assets/`: 캐릭터 일러스트와 배경 이미지

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Streamlit Community Cloud 배포

1. 이 프로젝트 파일을 GitHub 저장소에 업로드합니다.
2. Streamlit Community Cloud에서 저장소를 연결합니다.
3. Main file path에 `main.py`를 입력하고 Deploy를 누릅니다.

## 게임 기능

- 세 명의 캐릭터와 대화하는 3개 장면
- 선택에 따른 호감도 변화
- 캐릭터별 엔딩
- 호감도 현황 및 선택 기록
- 다시 플레이하기

참고: 제공된 일러스트는 게임 화면용으로 편집한 콘셉트 이미지입니다.
