import streamlit as st

st.set_page_config(page_title="병맛 키우기", page_icon="🥊")

st.title("🥊 병맛 캐릭터 키우기 & 맞짱 게임")
st.write("버튼을 미친듯이 누르고 캐릭터를 진화시켜 보스를 제압하세요!")

# 데이터 저장 공간 만들기
if "power" not in st.session_state:
    st.session_state.power = 10

# 전투력에 따른 캐릭터 진화
power = st.session_state.power
if power >= 500:
    char_name = "👑 우주 최강 헬스 짱가"
elif power >= 250:
    char_name = "🦖 3단 변신 헬창 공룡"
elif power >= 100:
    char_name = "🥋 3년 차 동네 짱"
elif power >= 40:
    char_name = "🐔 빡친 중닭"
else:
    char_name = "🐣 갓 태어난 병아리"

# 스탯 출력
st.subheader(f"현재 캐릭터: {char_name}")
st.metric(label="내 전투력", value=f"{power} CP")

# 클릭해서 능력치 올리기
col1, col2 = st.columns(2)
with col1:
    if st.button("💪 운동하기 (+5 CP)", use_container_width=True):
        st.session_state.power += 5
        st.rerun()

with col2:
    if st.button("🍗 닭가슴살 먹기 (+15 CP)", use_container_width=True):
        st.session_state.power += 15
        st.rerun()

st.markdown("---")
st.subheader("⚔️ 맞짱 신청하기")

# 보스 목록
bosses = [
    {"name": "길 가던 초딩", "req": 30, "msg": "초딩의 떡볶이를 빼앗아 승리했습니다!"},
    {"name": "동네 비둘기 대장", "req": 100, "msg": "비둘기 떼를 물리치고 구청을 접수했습니다!"},
    {"name": "민트초코 몬스터", "req": 250, "msg": "민트초코를 다 먹어서 퇴치했습니다!"},
    {"name": "최종보스: 전교 1등 안경", "req": 500, "msg": "안경을 벗겨 최종 승리했습니다!"}
]

for boss in bosses:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write(f"**{boss['name']}** (필요 전투력: {boss['req']} CP)")
    with col_b:
        if st.button(f"덤비기", key=boss['name']):
            if power >= boss['req']:
                st.balloons()
                st.success(f"🎉 승리! {boss['msg']}")
                st.session_state.power += 20
            else:
                st.error("💀 패배! 전투력이 부족합니다. 운동을 더 하세요!")

st.markdown("---")
if st.button("🔄 리셋 (처음부터 다시)"):
    st.session_state.power = 10
    st.rerun()
