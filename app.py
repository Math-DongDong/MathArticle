import streamlit as st
import os

# 1. 페이지 레이아웃 설정
st.set_page_config(
    page_title="동동쌤의 수학모음",
    page_icon="./기타/동동이.PNG",
    layout="wide"
)

# 2. 메인 페이지 정의
def main_page():
    # 메인 페이지 타이틀 및 설명
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>동동쌤의 수학 모음</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>원하는 학습 주제를 선택하여 바로 이동해보세요!</p>", unsafe_allow_html=True)

    # 💡 [설정 영역] 선생님께서 이미지 경로와 링크 주소를 입력하는 곳입니다!
    # 이미지가 없다면 우선 비워두셔도 에러가 나지 않도록 처리해 두었습니다.
    cards_data = [
        {
            "title": "📐 중학 수학",
            "image": "./기타/middle_math.png",   # 1. 중학 수학 이미지 경로 
            "link": "https://mathzip.streamlit.app" # 1. 중학 수학 앱 링크
        },
        {
            "title": "🤖 인공지능 수학",
            "image": "./기타/ai_math.png",       # 2. 인공지능 수학 이미지 경로
            "link": "https://ai-math.streamlit.app" # 2. 인공지능 수학 앱 링크
        },
        {
            "title": "🏭 산업 수학",
            "image": "./기타/industry_math.png", # 3. 산업 수학 이미지 경로
            "link": "https://https://industrialmath.streamlit.app/" # 3. 산업 수학 앱 링크
        },
        {
            "title": "💬 챗봇",
            "image": "./기타/chatbot.png",       # 4. 챗봇 이미지 경로
            "link": "https://dongdongbot.streamlit.app/" # 4. 챗봇 앱 링크
        }
    ]

    # 4개의 열을 만들어서 4등분 배치
    cols = st.columns(4)

    for idx, col in enumerate(cols):
        data = cards_data[idx]
        with col:
            # st.container(border=True)를 쓰면 예쁜 회색 테두리 박스(카드)가 생깁니다.
            with st.container(border=True):
                
                # 1. 이미지 표시 (경로에 실제 파일이 있는지 검사 후 출력)
                if os.path.exists(data["image"]):
                    st.image(data["image"], use_container_width=True)
                else:
                    # 파일이 아직 없을 때는 에러 대신 빈 박스 안내문구를 보여줍니다.
                    st.info("🖼️ (이미지 준비 중)", icon="ℹ️")

                # 2. 제목 표시
                st.subheader(data["title"])

                # 3. 링크 이동 버튼
                # st.link_button은 클릭 시 새 탭이나 현재 탭에서 지정된 URL로 이동시킵니다.
                st.link_button("🚀 바로가기", url=data["link"], use_container_width=True)


# 3. 메뉴바 설정(각 페이지의 실제 콘텐츠는 별도의 파일에 존재).
pages = {
    "메인페이지": [
        st.Page(main_page, title="홈 화면", default=True),
    ],
    "인공지능 수학": [
        st.Page("./인공지능수학/GrayScale.py", title="그레이 필터 이미지 데이터 다운로드"),
    ],
}

# 4. 네비게이션 UI 생성(메뉴바 위치)
pg = st.navigation(pages, position="hidden")

# 5. 사용자가 선택한 페이지 실행
pg.run()