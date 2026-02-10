import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import io 

#===============================================================================================
@st.cache_data(show_spinner=False, ttl=300)
def load_image(image_file):
    return Image.open(image_file).convert('RGB')

@st.fragment
def gray_filter_fragment(image, original_width, original_height, filename):
    MAX_PIXELS = 500

    # 최대 픽셀 제한
    default_w = MAX_PIXELS if original_width > MAX_PIXELS else original_width
    default_h = MAX_PIXELS if original_height > MAX_PIXELS else original_height

    # [해상도 설정 / 원본 / 결과 ]
    col_edit, col_orig, col_res = st.columns([0.2, 0.4, 0.4], gap="medium")
    with col_edit:
        st.subheader("⚙️ 해상도 설정")
        new_width = st.number_input(
            "가로(Width) 픽셀", 
            min_value=1, 
            max_value=MAX_PIXELS,
            value=default_w,
            step=10,
            key="input_w" # 키 지정 권장
        )
        
        new_height = st.number_input(
            "세로(Height) 픽셀", 
            min_value=1, 
            max_value=MAX_PIXELS,
            value=default_h,
            step=10,
            key="input_h"
        )

        # 1) 리사이징 (축소 -> NEAREST)
        small_pil = image.resize((new_width, new_height), Image.Resampling.NEAREST)
        small_arr = np.array(small_pil)

        # 2) 그레이스케일 변환
        gray_matrix = np.round(np.mean(small_arr, axis=2)).astype(np.uint8)

        # 3) 시각화용 3채널 복구
        gray_stacked_arr = np.stack((gray_matrix, gray_matrix, gray_matrix), axis=2)
        gray_small_pil = Image.fromarray(gray_stacked_arr)

        # 4) 화면 표시용 확대 (원본 크기)
        preview_pil = gray_small_pil.resize((original_width, original_height), Image.Resampling.NEAREST)
        
    with col_orig:
        st.subheader("원본 이미지")
        st.image(image, caption=f"원본: {original_width}x{original_height} px", width="stretch")

    with col_res:
        st.subheader("그레이 필터")
        st.image(preview_pil, caption=f"변경됨: {new_width}x{new_height} px", width="stretch")


    with col_edit:
        st.divider()        
        output_excel = io.BytesIO()
        
        with st.spinner("엑셀 생성 중...", show_time=True):
            with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
                pd.DataFrame(gray_matrix).to_excel(writer, index=False, header=False, sheet_name='Gray_Data')
            excel_data = output_excel.getvalue()
            
        st.download_button(
            label="💾 픽셀 데이터(Excel) 받기",
            data=excel_data,
            file_name=f"gray_data_{new_width}x{new_height}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        with st.container(horizontal=True): # 컨테이너로 감싸서 caption과 버튼이 같은 줄에 있도록
            st.space("stretch")
            st.caption(f"※ 최대 {MAX_PIXELS}px 까지만 지원됩니다.")

#===============================================================================================

st.title("그레이 필터 이미지 데이터 다운로드")
with st.container(horizontal=True):
    st.space("stretch")
    st.page_link("https://mathzip.streamlit.app/ImageConversion", label="이미지의 데이터 변환 돌아가기", icon="⬅️", width="content")

# 이미지 업로드 창 생성
with st.expander("📂 이미지 업로드 열기/닫기", expanded=True):
    uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 1. 이미지 열기 (무조건 RGB 3채널로 변환)
    image = load_image(uploaded_file)
    original_width, original_height = image.size

    # 2. 프래그먼트 실행 (이미지와 정보만 넘김)
    gray_filter_fragment(image, original_width, original_height, uploaded_file.name)

else:
    st.info("👆 상단의 '이미지 업로드'를 열어 이미지 파일( png, jpg, jpeg )을 먼저 업로드해주세요.")
