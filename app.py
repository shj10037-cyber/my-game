import streamlit as st
import random

st.set_page_config(page_title="LOL 텍스트 시뮬레이터", page_icon="⚔️")

st.title("⚔️ 리그 오브 레전드: 소환사의 협곡")
st.write("챔피언을 선택하고 라인전과 한타를 승리로 이끌어 넥서스를 파괴하세요!")

# 상태 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = "pick" # pick, ingame, result
if "champ" not in st.session_state:
    st.session_state.champ = None
if "gold" not in st.session_state:
    st.session_state.gold = 500
if "kda" not in st.session_state:
    st.session_state.kda = {"k": 0, "d": 0, "a": 0}
if "tower_hp" not in st.session_state:
    st.session_state.tower_hp = 100
if "log" not in st.session_state:
    st.session_state.log = []

# 1. 픽창 (챔피언 선택)
if st.session_state.game_state == "pick":
    st.subheader("🛡️ 챔피언을 선택하세요")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗡️ 야스오 (미드 - 피지컬형)", use_container_width=True):
            st.session_state.champ = {"name": "야스오", "role": "미드", "skill": "하사기! 바람장막!"}
            st.session_state.game_state = "ingame"
            st.rerun()
            
        if st.button("🏹 카이사 (원딜 - 캐리형)", use_container_width=True):
            st.session_state.champ = {"name": "카이사", "role": "원딜", "skill": "사냥의 본능!"}
            st.session_state.game_state = "ingame"
            st.rerun()

    with col2:
        if st.button("🔮 사일러스 (미드 - 돌진형)", use_container_width=True):
            st.session_state.champ = {"name": "사일러스", "role": "미드", "skill": "강탈!"}
            st.session_state.game_state = "ingame"
            st.rerun()
            
        if st.button("💥 벡스 (미드 - 제압형)", use_container_width=True):
            st.session_state.champ = {"name": "벡스", "role": "미드", "skill": "황량한 파도!"}
            st.session_state.game_state = "ingame"
            st.rerun()

# 2. 인게임 (협곡 진행)
elif st.session_state.game_state == "ingame":
    champ = st.session_state.champ
    kda = st.session_state.kda
    
    st.write(f"### 🎮 내 챔피언: **{champ['name']}** ({champ['role']})")
    
    # 전황판
    col1, col2, col3 = st.columns(3)
    col1.metric("KDA", f"{kda['k']} / {kda['d']} / {kda['a']}")
    col2.metric("보유 골드", f"{st.session_state.gold} G")
    col3.metric("적 포탑 체력", f"{st.session_state.tower_hp}%")

    st.markdown("---")
    st.subheader("⚔️ 라인전 & 행동 선택")

    action1, action2, action3 = st.columns(3)
    
    # 행동 1: CS 수급 / 딜교
    with action1:
        if st.button("🌾 CS 먹기 & 딜교", use_container_width=True):
            rand = random.random()
            if rand > 0.3:
                st.session_state.gold += 150
                st.session_state.log.insert(0, "🌾 막타를 잘 쳐서 150골드를 획득했습니다.")
            else:
                st.session_state.kda['d'] += 1
                st.session_state.log.insert(0, "💀 딜교 실패! 갱킹을 맞아 사망했습니다.")
            st.rerun()

    # 행동 2: 솔로 킬 시도
    with action2:
        if st.button(f"⚡ 궁극기 사용 ({champ['skill']})", use_container_width=True):
            rand = random.random()
            if rand > 0.4:
                st.session_state.kda['k'] += 1
                st.session_state.gold += 300
                st.session_state.tower_hp = max(0, st.session_state.tower_hp - 25)
                st.session_state.log.insert(0, f"🔥 {champ['skill']} 화려한 피지컬로 솔로킬 성공! (+300G)")
            else:
                st.session_state.kda['d'] += 1
                st.session_state.log.insert(0, "💀 뇌절! 타워 다이브를 치다 역으로 따였습니다.")
            st.rerun()

    # 행동 3: 로밍 / 오브젝트 한타
    with action3:
        if st.button("🐉 용/바론 한타 참여", use_container_width=True):
            rand = random.random()
            if rand > 0.5:
                st.session_state.kda['k'] += 2
                st.session_state.kda['a'] += 1
                st.session_state.gold += 500
                st.session_state.tower_hp = max(0, st.session_state.tower_hp - 40)
                st.session_state.log.insert(0, "🎉 대규모 한타 대승! 용을 획득하고 포탑을 밀어붙입니다.")
            else:
                st.session_state.kda['d'] += 1
                st.session_state.log.insert(0, "💀 한타 패배... 팀원이 '미드 차이'를 외칩니다.")
            st.rerun()

    # 승리 조건 (포탑 파괴)
    if st.session_state.tower_hp <= 0:
        st.session_state.game_state = "result"
        st.rerun()

    # 플레이 기록 출력
    st.markdown("---")
    st.write("📜 **경기 진행 상황**")
    for l in st.session_state.log[:5]:
        st.write(f"- {l}")

# 3. 결과 창
elif st.session_state.game_state == "result":
    st.balloons()
    st.success("🎉 VICTORY! 적 넥서스가 파괴되었습니다!")
    
    kda = st.session_state.kda
    st.write(f"### 최종 KDA: **{kda['k']} / {kda['d']} / {kda['a']}**")
    st.write(f"### 최종 획득 골드: **{st.session_state.gold} G**")
    
    if kda['k'] >= 5:
        st.write("👑 **평가**: 당신은 팀을 캐리한 명예 5단계 플레이어입니다!")
    else:
        st.write("👍 **평가**: 1인분은 하고 승리했습니다.")

    if st.button("🔄 다음 판 하기"):
        st.session_state.game_state = "pick"
        st.session_state.gold = 500
        st.session_state.kda = {"k": 0, "d": 0, "a": 0}
        st.session_state.tower_hp = 100
        st.session_state.log = []
        st.rerun()
