import streamlit as st

# 1. 페이지 레이아웃 설정
# layout="wide"로 설정 For 상단 메뉴바 표시
st.set_page_config(
    page_title="동동쌤의 수학모음",
    page_icon="./기타/동동이.PNG",
    layout="wide"
)

# 2. 메뉴바 설정(각 페이지의 실제 콘텐츠는 별도의 파일에 존재).
pages = {
    "인공지능 수학": [
        st.Page("./인공지능수학/Dissolve.py", title="디졸브 효과"),
    ],
}

# 3. 네비게이션 UI 생성(메뉴바 위치)
pg = st.navigation(pages, position="hidden")

# 4. 사용자가 선택한 페이지 실행
pg.run()