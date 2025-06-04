from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
import os

# 환경변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# GPT에게 알려줄 정보(개인적인 정보)
context = '''
📌 기관 개요
운영 기관: 대한상공회의소 인력개발사업단
운영 지역: 서울, 부산, 인천, 광주, 경기, 충남, 전북 등 전국 7개 인력개발원
주요 사업:
직업능력개발훈련 사업
취업역량 강화 사업
개발도상국 지원사업
교육 대상: 청년, 재직자, 신중년, 직업계고 학생 등
교육 분야: SW개발, 스마트제조·로봇, 전기전자, 기계·자동차, 가구인테리어, 드론 등

🎯 주요 교육과정
다양한 분야에서 실무 중심의 교육과정을 운영하고 있으며, 일부 대표적인 과정은 다음과 같습니다:
[Intel] 엣지 AI SW 아카데미(8기)
교육기간: 2025.07.08 ~ 2026.01.22 (6개월, 900시간)
교육장소: 서울 본원
분야: 정보통신
특징: 인텔 현업 엔지니어 직강, 임베디드 시스템 교육 

(천안) 공장자동화를 위한 제조로봇 엔지니어
교육기간: 2025.07.08 ~ 2026.02.06 (7개월, 960시간)
교육장소: 충남 천안기술교육센터
분야: 스마트제조·로봇
특징: PLC, 로봇, ROS, 파이썬 등 공장자동화 기술 교육 

Unreal 디지털트윈 3D에셋 개발자
교육기간: 2025.07.22 ~ 2025.11.14 (5개월, 530시간)
교육장소: 광주 본원
분야: 정보통신
특징: Unreal Engine을 활용한 디지털트윈 및 3D 에셋 개발 교육 

(천안) 생성형AI활용AWS웹서비스개발
교육기간: 2025.06.10 ~ 2025.10.02 (5개월, 600시간)
교육장소: 충남 천안기술교육센터
분야: 정보통신
특징: 생성형 AI와 AWS를 활용한 웹서비스 개발 교육

🏫 개발원 안내
각 지역의 인력개발원은 다음과 같습니다:
서울기술교육센터: 서울특별시 강서구 화곡로 179
부산인력개발원: 부산광역시 동구 중앙대로 176 3F
인천인력개발원: 인천광역시 남동구 남동서로205번길 32
광주인력개발원: 광주광역시 광산구 소촌로152번길 37
경기인력개발원: 경기도 파주시 와석순환로172번길 16
충남인력개발원: 충청남도 공주시 의당면 의당전의로 415
전북인력개발원: 전라북도 군산시 동장산로 119

📞 문의 및 상담
구직자 교육상담: 02-6050-3913
근로자 교육상담: 02-6050-3913
상담시간: 평일 09:00 ~ 18:00 (점심시간 11:30 ~ 12:30 제외)

현재 대한상공회의소 회장은 최태원 회장임
'''

def ask_gpt(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                            "너는 친절하고 귀여운 상공봇이야.\n"
                            f"{context}\n"
                            "간결하고 핵심만 대답하되 매우 귀여워야 해.\n"
                            "텍스트 정렬을 좀 해줘. 이모티콘 많이 써도 돼.\n"
                                )
                },
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❗ 오류 발생: {str(e)}"

# Flask 앱 초기화
app = Flask(__name__)
chat_history = []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', chat=[])

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")
        answer = ask_gpt(question)
        return jsonify({"answer": answer})
    except Exception as e:
        print("❗ ask() 에러:", e)  # 🔥 서버 로그에 오류 출력
        return jsonify({"answer": f"❗ 서버 오류: {str(e)}"}), 500

# 🔥 Render에서는 app.run() 없이도 작동하므로 제외
# if __name__ == '__main__':
#     app.run(debug=True)

