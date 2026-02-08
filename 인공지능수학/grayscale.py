import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import io 

# --- 앱 제목 ---
st.title("그레이 필터 이미지 데이터 다운로드")

# 상단 네비게이션
with st.container(horizontal=True):
    st.space("stretch")
    st.page_link("https://mathzip.streamlit.app/ImageConversion", label="이미지의 데이터 변환 돌아가기", icon="⬅️", width="content")

# 이미지 업로드 창 생성
with st.expander("📂 이미지 업로드 열기/닫기", expanded=True):
    uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 1. 이미지 열기 (무조건 RGB 3채널로 변환)
    image = Image.open(uploaded_file).convert('RGB')
    original_width, original_height = image.size

    # =========================================================
    # [요청사항 반영] 최대 픽셀 제한 로직 (500px)
    # =========================================================
    MAX_PIXELS = 500

    # 기본값 계산: 원본이 500보다 크면 500으로, 작으면 원본 크기 그대로
    default_w = MAX_PIXELS if original_width > MAX_PIXELS else original_width
    default_h = MAX_PIXELS if original_height > MAX_PIXELS else original_height

    # ---------------------------------------------------------
    # 메인 레이아웃 (설정 | 원본 | 결과)
    # ---------------------------------------------------------
    col_edit, col_orig, col_res = st.columns([0.2, 0.4, 0.4], gap="medium")
    
    with col_edit:
        st.subheader("⚙️ 해상도 설정")
        
        # [수정] max_value를 500으로 제한하고, 위에서 계산한 default 값을 적용
        new_width = st.number_input(
            "가로(Width) 픽셀", 
            min_value=1, 
            max_value=MAX_PIXELS, # 최대값 제한
            value=default_w,      # 계산된 기본값
            step=10
        )
        
        new_height = st.number_input(
            "세로(Height) 픽셀", 
            min_value=1, 
            max_value=MAX_PIXELS, # 최대값 제한
            value=default_h,      # 계산된 기본값
            step=10
        )

        # --- 이미지 처리 로직 ---
        # 1) 리사이징 (작은 크기로 축소 -> NEAREST 사용)
        small_pil = image.resize((new_width, new_height), Image.Resampling.NEAREST)
        small_arr = np.array(small_pil)

        # 2) 그레이스케일 변환 (단순 평균법 + 반올림)
        # (H, W, 3) -> (H, W)
        gray_matrix = np.round(np.mean(small_arr, axis=2)).astype(np.uint8)

        # 3) 시각화용 3채널 복구
        gray_stacked_arr = np.stack((gray_matrix, gray_matrix, gray_matrix), axis=2)
        gray_small_pil = Image.fromarray(gray_stacked_arr)

        # 4) 화면 표시용 뻥튀기 (원본 크기에 맞춤)
        preview_pil = gray_small_pil.resize((original_width, original_height), Image.Resampling.NEAREST)
        
        st.write("") # 공백

    # [2열] 원본
    with col_orig:
        st.subheader("원본 이미지")
        st.image(image, caption=f"원본: {original_width}x{original_height} px", width='stretch')

    # [3열] 결과
    with col_res:
        st.subheader("그레이 필터")
        st.image(preview_pil, caption=f"변경됨: {new_width}x{new_height} px", width='stretch')


    # 1열 다운로드 파일 요소 추가
    with col_edit:
        st.divider()
        
        # 엑셀 다운로드 (픽셀 데이터)
        output_excel = io.BytesIO()
        
        # 해상도가 500px로 제한되었으므로 엑셀 생성 속도가 보장됩니다.
        with st.spinner("엑셀 파일 생성 중...", show_time=True):
            with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
                # 2차원 그레이스케일 데이터 저장
                pd.DataFrame(gray_matrix).to_excel(writer, index=False, header=False, sheet_name='Gray_Data')
            excel_data = output_excel.getvalue()
            
        st.download_button(
            label="💾 픽셀 데이터(Excel) 받기",
            data=excel_data,
            file_name=f"gray_data_{new_width}x{new_height}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch' # width='stretch' 대체 (최신 문법)
        )
        st.caption(f"※ 최대 {MAX_PIXELS}px 까지만 지원됩니다.")

else:
    st.info("👆 상단의 '이미지 업로드'를 열어 이미지 파일( png, jpg, jpeg )을 먼저 업로드해주세요.")
