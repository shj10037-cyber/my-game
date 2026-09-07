import streamlit as st
import random
import time

st.set_page_config(page_title="LOL 텍스트 시뮬레이터 2.0", page_icon="⚔️", layout="wide")

st.title("⚔️ 리그 오브 레전드: 소환사의 협곡 2.0")
st.write("아이템을 구매하고 스킬을 찍으며, 포탑 3개와 억제기를 밀어 넥서스를 파괴하세요!")

# 스킬 정보
SKILLS = {
    "야스오": {"Q": "강철의 폭풍", "W": "바람장막", "E": "질풍검", "R": "최후의 숨결"},
    "사일러스": {"Q": "사슬 후려치기", "W": "국왕의 처형", "E": "도주/억압", "R": "강탈"},
    "벡스": {"Q": "안개파동", "W": "공포 침식", "E": "어둠의 파도", "R": "황량한 파도"},
    "카이사": {"Q": "이케시아의 우량", "W": "공허의 추적자", "E": "고속 충전", "R": "사냥의 본능"}
}

# 상점 아이템 정보
ITEMS = {
    "도란의 검 (+100 HP, +10 공격력)": {"price": 450, "hp": 100, "atk": 10},
    "광전사의 신발 (+15 공격력)": {"price": 1100, "hp": 0, "atk": 15},
    "몰락한 왕의 단검 (+30 공격력)": {"price": 3300, "hp": 0, "atk": 30},
    "무한의 대검 (+70 공격력)": {"price": 3400, "hp": 0, "atk": 70},
    "워모그의 갑옷 (+500 HP)": {"price": 3100, "hp": 500, "atk": 0}
}

# 게임 상태 초기화
if "state" not in st.session_state:
    st.session_state.state = "pick"
if "champ" not in st.session_state:
    st.session_state.champ = None
if "level" not in st.session_state:
    st.session_state.level = 1
if "exp" not in st.session_state:
    st.session_state.exp = 0
if "hp" not in st.session_state:
    st.session_state.hp = 500
if "max_hp" not in st.session_state:
    st.session_state.max_hp = 500
if "atk" not in st.session_state:
    st.session_state.atk = 50
if "gold" not in st.session_state:
    st.session_state.gold = 500
if "kda" not in st.session_state:
    st.session_state.kda = {"k": 0, "d": 0, "a": 0}
if "cs" not in st.session_state:
    st.session_state.cs = 0
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "turrets" not in st.session_state:
    st.session_state.turrets = ["1차 포탑", "2차 포탑", "억제기 포탑", "억제기", "쌍둥이 포탑/넥서스"]
if "turret_hp" not in st.session_state:
    st.session_state.turret_hp = 100
if "log" not in st.session_state:
    st.session_state.log = []

# 경험치 및 레벨업 체크
def check_levelup():
    req_exp = st.session_state.level * 100
    if st.session_state.exp >= req_exp:
        st.session_state.level += 1
        st.session_state.exp -= req_exp
        st.session_state.max_hp += 80
        st.session_state.hp = st.session_state.max_hp
        st.session_state.atk += 8
        st.session_state.log.insert(0, f"🆙 레벨 업! {st.session_state.level}레벨이 되었습니다! (최대 HP/공격력 증가)")

# 1. 챔피언 선택 화면
if st.session_state.state == "pick":
    st.subheader("🛡️ 소환사의 협곡 - 챔피언 선택")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("🗡️ 야스오", use_container_width=True):
            st.session_state.champ = "야스오"
            st.session_state.state = "game"
            st.rerun()
    with c2:
        if st.button("🔮 사일러스", use_container_width=True):
            st.session_state.champ = "사일러스"
            st.session_state.state = "game"
            st.rerun()
    with c3:
        if st.button("💥 벡스", use_container_width=True):
            st.session_state.champ = "벡스"
            st.session_state.state = "game"
            st.rerun()
    with c4:
        if st.button("🏹 카이사", use_container_width=True):
            st.session_state.champ = "카이사"
            st.session_state.state = "game"
            st.rerun()

# 2. 메인 게임 화면
elif st.session_state.state == "game":
    champ = st.session_state.champ
    skills = SKILLS[champ]
    current_target = st.session_state.turrets[0] if st.session_state.turrets else "넥서스"
    
    # 상단 정보바
    st.markdown(f"### 🎮 **{champ}** (Lv.{st.session_state.level}) | 목표: **{current_target} 파괴**")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    col_stat1.metric("체력 (HP)", f"{st.session_state.hp} / {st.session_state.max_hp}")
    col_stat2.metric("공격력 / 골드", f"{st.session_state.atk} ATK / {st.session_state.gold} G")
    col_stat3.metric("KDA (CS)", f"{st.session_state.kda['k']}/{st.session_state.kda['d']}/{st.session_state.kda['a']} ({st.session_state.cs} CS)")
    col_stat4.metric("목표 구조물 HP", f"{st.session_state.turret_hp}%")
    
    st.progress(st.session_state.hp / st.session_state.max_hp, text="내 체력")
    st.progress(st.session_state.turret_hp / 100, text=f"{current_target} 체력")
    
    st.markdown("---")
    
    # 탭 구분: 라인전/전투, 상점, 가방
    tab1, tab2, tab3 = st.tabs(["⚔️ 라인전 & 전투", "🛒 귀환 & 상점", "🎒 아이템 가방"])
    
    with tab1:
        st.subheader("라인전 선택지")
        act1, act2, act3, act4 = st.columns(4)
        
        with act1:
            if st.button("🌾 CS 막타 치기", use_container_width=True):
                earned_cs = random.randint(3, 6)
                earned_gold = earned_cs * 21
                st.session_state.cs += earned_cs
                st.session_state.gold += earned_gold
                st.session_state.exp += 35
                check_levelup()
                st.session_state.log.insert(0, f"🌾 미니언 {earned_cs}마리를 섭취했습니다. (+{earned_gold}G / +35 EXP)")
                st.rerun()
                
        with act2:
            if st.button(f"⚡ 스킬 딜교 ({skills['Q']})", use_container_width=True):
                damage = st.session_state.atk + random.randint(10, 30)
                taken_damage = random.randint(20, 60)
                st.session_state.hp = max(0, st.session_state.hp - taken_damage)
                st.session_state.turret_hp = max(0, st.session_state.turret_hp - 10)
                st.session_state.exp += 50
                check_levelup()
                
                if st.session_state.hp == 0:
                    st.session_state.kda['d'] += 1
                    st.session_state.hp = st.session_state.max_hp
                    st.session_state.log.insert(0, f"💀 딜교 중 사망했습니다! 우물에서 부활합니다. (-{taken_damage} HP)")
                else:
                    st.session_state.log.insert(0, f"🔥 {skills['Q']} 스킬로 딜교 성공! 적 포탑 압박 (+{damage} 데미지 / -{taken_damage} HP 받음)")
                st.rerun()

        with act3:
            if st.button(f"💥 궁극기 솔킬 시도 ({skills['R']})", use_container_width=True):
                win_rate = 0.5 + (st.session_state.atk - 50) * 0.005
                if random.random() < win_rate:
                    st.session_state.kda['k'] += 1
                    st.session_state.gold += 300
                    st.session_state.exp += 120
                    st.session_state.turret_hp = max(0, st.session_state.turret_hp - 25)
                    check_levelup()
                    st.session_state.log.insert(0, f"🩸 {skills['R']}! 화려한 피지컬로 솔로 킬을 올렸습니다! (+300G / +120 EXP)")
                else:
                    st.session_state.kda['d'] += 1
                    st.session_state.hp = st.session_state.max_hp
                    st.session_state.log.insert(0, f"💀 궁극기가 빗나가 역으로 킬을 따였습니다. 우물 부활!")
                st.rerun()

        with act4:
            if st.button("🐉 바론/내셔 남작 한타", use_container_width=True):
                if random.random() > 0.4:
                    st.session_state.kda['k'] += 2
                    st.session_state.kda['a'] += 1
                    st.session_state.gold += 600
                    st.session_state.exp += 200
                    st.session_state.turret_hp = max(0, st.session_state.turret_hp - 40)
                    check_levelup()
                    st.session_state.log.insert(0, "🎉 바론 버프 획득! 대규모 한타 대승으로 적 포탑을 대량 파괴합니다.")
                else:
                    st.session_state.kda['d'] += 1
                    st.session_state.hp = st.session_state.max_hp
                    st.session_state.log.insert(0, "💀 바론 둥지 한타에서 대패했습니다...")
                st.rerun()

    with tab2:
        st.subheader("상점 (아이템 구매 / HP 회복)")
        if st.button("💊 우물 귀환 (HP 100% 회복)"):
            st.session_state.hp = st.session_state.max_hp
            st.session_state.log.insert(0, "🏠 귀환하여 체력을 완전히 회복했습니다.")
            st.rerun()
            
        st.markdown("---")
        for item_name, info in ITEMS.items():
            b_col1, b_col2 = st.columns([3, 1])
            b_col1.write(f"**{item_name}** - {info['price']}G")
            if b_col2.button("구매", key=item_name):
                if st.session_state.gold >= info['price']:
                    st.session_state.gold -= info['price']
                    st.session_state.max_hp += info['hp']
                    st.session_state.hp += info['hp']
                    st.session_state.atk += info['atk']
                    st.session_state.inventory.append(item_name)
                    st.session_state.log.insert(0, f"🛒 {item_name}을(를) 구매했습니다!")
                    st.rerun()
                else:
                    st.error("골드가 부족합니다!")

    with tab3:
        st.subheader("착용 중인 아이템")
        if st.session_state.inventory:
            for inv in st.session_state.inventory:
                st.write(f"- {inv}")
        else:
            st.write("구매한 아이템이 없습니다.")

    # 구조물 파괴 체크
    if st.session_state.turret_hp <= 0:
        destroyed = st.session_state.turrets.pop(0)
        st.session_state.log.insert(0, f"💥 **{destroyed}**을(를) 파괴했습니다!")
        if st.session_state.turrets:
            st.session_state.turret_hp = 100
        else:
            st.session_state.state = "win"
        st.rerun()

    # 진행 로그
    st.markdown("---")
    st.write("📜 **실시간 게임 진행 상황**")
    for l in st.session_state.log[:6]:
        st.write(f"- {l}")

# 3. 승리 화면
elif st.session_state.state == "win":
    st.balloons()
    st.success("🎉 VICTORY! 적 넥서스가 완전히 파괴되었습니다!")
    st.write(f"### 최종 레벨: **Lv.{st.session_state.level}**")
    st.write(f"### 최종 KDA: **{st.session_state.kda['k']} / {st.session_state.kda['d']} / {st.session_state.kda['a']} ({st.session_state.cs} CS)**")
    
    if st.button("🔄 다음 게임 시작하기"):
        st.session_state.state = "pick"
        st.session_state.level = 1
        st.session_state.exp = 0
        st.session_state.hp = 500
        st.session_state.max_hp = 500
        st.session_state.atk = 50
        st.session_state.gold = 500
        st.session_state.kda = {"k": 0, "d": 0, "a": 0}
        st.session_state.cs = 0
        st.session_state.inventory = []
        st.session_state.turrets = ["1차 포탑", "2차 포탑", "억제기 포탑", "억제기", "쌍둥이 포탑/넥서스"]
        st.session_state.turret_hp = 100
        st.session_state.log = []
        st.rerun()
