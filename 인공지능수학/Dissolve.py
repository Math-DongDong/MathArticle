import streamlit as st
import numpy as np
from PIL import Image
import io 
import time

# ==============================================================================
@st.cache_data(show_spinner=False, ttl=300)
def load_image(image_file):
    return Image.open(image_file)

@st.cache_data(show_spinner=False, ttl=300)
def get_image_arrays(name1, size1, name2, size2, _bytes1, _bytes2, target_w, target_h):
    """바이트 데이터를 이미지 배열로 변환 (캐싱됨)"""
    img1 = Image.open(io.BytesIO(_bytes1)).convert('RGB').resize((target_w, target_h))
    img2 = Image.open(io.BytesIO(_bytes2)).convert('RGB').resize((target_w, target_h))
    
    arr1 = np.array(img1, dtype=float) / 255.0
    arr2 = np.array(img2, dtype=float) / 255.0
    
    return arr1, arr2

@st.fragment
def dissolve_interface(file1, file2):
    temp_img = load_image(file1)
    orig_w, orig_h = temp_img.size
    default_w = 800 if orig_w > 800 else orig_w
    default_h = int(orig_h * (default_w / orig_w))

    # [설정 / 디졸브 / 소스]
    col1, col2, col3 = st.columns([0.25, 0.5, 0.25])
    with col1:
        st.subheader("⚙️ 설정 및 제어")
        st.caption("해상도 설정")

        wcol1, wcol2 = st.columns(2)
        with wcol1:
            target_w = st.number_input("가로 픽셀", 10, 800, default_w, 10)
        with wcol2:
            target_h = st.number_input("세로 픽셀", 10, value=default_h, step=10)
        
        # 자동/수동 제어
        auto_mode = st.toggle("자동 실행", value=False)            
        
        if auto_mode:
            st.caption("자동 제어 중...")
            if st.button("⏯️ 재생/일시정지", width="stretch"):
                st.session_state.animation_running = not st.session_state.animation_running
                if st.session_state.animation_running and st.session_state.current_alpha >= 1.0:
                    st.session_state.current_alpha = 0.0

            if st.session_state.animation_running:
                st.success(f"▶️ 재생 중: {st.session_state.current_alpha:.2f}")
            else:
                st.info("⏸️ 일시 정지")
            
            alpha = st.session_state.current_alpha
        else:
            st.session_state.animation_running = False 
            st.caption("수동 제어 중...")
            manual_alpha = st.slider(
                "가중치 (Alpha)",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.current_alpha, # 현재 상태값 유지
                step=0.01,
                key="slider_val"
            )
            alpha = manual_alpha
            st.session_state.current_alpha = manual_alpha

    arr1, arr2 = get_image_arrays(
        file1.name, file1.size,
        file2.name, file2.size,
        file1.getvalue(),
        file2.getvalue(),
        target_w, target_h
    )

    with col2:
        st.subheader("✨ 결과")
        blended = (arr1 * (1 - alpha)) + (arr2 * alpha)
        
        st.image(blended, width="stretch", clamp=True)

        # 애니메이션 로직
        if auto_mode and st.session_state.animation_running:
            time.sleep(0.1) # 0.2초는 조금 느려서 0.1초로 조정 (취향껏 변경)
            st.session_state.current_alpha += 0.02
            
            if st.session_state.current_alpha >= 1.0:
                st.session_state.current_alpha = 1.0
                st.session_state.animation_running = False
            
            # [중요] 전체 앱이 아니라, 이 'dissolve_interface' 함수만 다시 실행함
            st.rerun(scope="fragment")

    with col3:
        st.subheader("소스")
        st.image(file1, width="stretch")
        st.image(file2, width="stretch")


# 상단 헤더
st.title("디졸브 효과")
with st.container(horizontal=True):
    st.space("stretch")
    st.page_link("https://mathzip.streamlit.app/ImageConversion", label="이미지의 데이터 변환 돌아가기", icon="⬅️", width="content")

# 세션 상태 초기화
if 'animation_running' not in st.session_state:
    st.session_state.animation_running = False
if 'current_alpha' not in st.session_state:
    st.session_state.current_alpha = 0.0

# [1] 파일 업로드 (이 부분은 프래그먼트 밖에서 실행 -> 리로드 시 깜빡임 방지)
with st.expander("📂 이미지 업로드 열기/닫기", expanded=True):
    up_c1, up_c2 = st.columns(2)
    f1 = up_c1.file_uploader("첫 번째 이미지", type=["png", "jpg", "jpeg"], key="img1")
    f2 = up_c2.file_uploader("두 번째 이미지", type=["png", "jpg", "jpeg"], key="img2")

# [2] 파일이 준비되면 프래그먼트 실행
if f1 and f2:
    dissolve_interface(f1, f2)

else:
    st.info("👆 상단의 '이미지 업로드'를 열어 두 개의 이미지를 넣어주세요.")