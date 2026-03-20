import streamlit as st
import pandas as pd
import platform
import sys

# 1. 앱 제목 및 기본 정보 출력
st.title("🚀 Streamlit 배포 환경 테스트")
st.write(f"**Python 버전:** {sys.version}")
st.write(f"**운영체제:** {platform.system()} {platform.release()}")

# 2. 필수 라이브러리 체크
st.subheader("📦 라이브러리 로드 테스트")
try:
    import sqlalchemy
    import oracledb
    st.success("✅ sqlalchemy 및 oracledb 로드 성공!")
except ImportError as e:
    st.error(f"❌ 라이브러리 로드 실패: {e}")
    st.info("requirements.txt에 해당 라이브러리가 있는지 확인하세요.")

# 3. 샘플 데이터 출력 (UI 작동 확인)
st.subheader("📊 데이터프레임 렌더링 테스트")
sample_data = pd.DataFrame({
    'ticker': ['AAPL', 'TSLA', 'MSFT'],
    'per': [31.5, 45.2, 35.8],
    'pbr': [42.1, 8.5, 12.3],
    'roe': [1.52, 0.15, 0.38]
})

# 최신 버전의 'stretch' 옵션 경고 방지 (use_container_width 사용)
st.dataframe(sample_data, use_container_width=True)

# 4. DB 연결 환경 변수 체크 (Secrets)
st.subheader("🔐 보안 설정(Secrets) 체크")
if "db_user" in st.secrets:
    st.info("✅ DB 사용자 정보(Secrets)를 읽어왔습니다.")
else:
    st.warning("⚠️ st.secrets에 설정된 값이 없습니다. (Streamlit Cloud Settings 확인 필요)")

st.divider()
st.write("이 화면이 정상적으로 보인다면 Streamlit 서버는 잘 작동하는 것입니다.")
st.write("만약 이 화면조차 안 나온다면 `packages.txt`나 `requirements.txt` 설정을 다시 확인해야 합니다.")