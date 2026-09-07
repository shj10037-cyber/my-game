import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="병맛 자음 스피드 퀴즈", page_icon="🧩", layout="centered")

st.title("🧩 [초스피드] 병맛 자음 맞추기 배틀")
st.write("화면에 나오는 초성을 보고 제한시간 안에 정답을 맞추세요!")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * { box-sizing: border-box; user-select: none; }
        body {
            margin: 0; padding: 0;
            background-color: #0f172a;
            color: #fff;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
        }
        #quiz-card {
            width: 480px;
            padding: 20px;
            background: #1e293b;
            border: 3px solid #38bdf8;
            border-radius: 12px;
            margin: 15px auto;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
        }
        .initials {
            font-size: 54px;
            font-weight: bold;
            color: #facc15;
            letter-spacing: 10px;
            margin: 15px 0;
        }
        .hint {
            font-size: 18px;
            color: #94a3b8;
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 80%;
            padding: 12px;
            font-size: 20px;
            text-align: center;
            border: 2px solid #38bdf8;
            border-radius: 8px;
            background: #0f172a;
            color: #fff;
            outline: none;
        }
        .hud {
            display: flex;
            justify-content: space-around;
            width: 480px;
            margin: 0 auto;
            font-size: 20px;
            font-weight: bold;
        }
        button {
            padding: 12px 24px;
            font-size: 18px;
            background-color: #38bdf8;
            color: #0f172a;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }
        button:hover { background-color: #7dd3fc; }
        #result-msg {
            font-size: 20px;
            height: 30px;
            margin-top: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="hud">
        <div>점수: <span id="score">0</span></div>
        <div>남은 시간: <span id="time">30</span>초</div>
    </div>

    <div id="quiz-card">
        <div class="hint" id="hint-text">게임 시작 버튼을 누르세요!</div>
        <div class="initials" id="initials-text">🔍</div>
        <input type="text" id="user-input" placeholder="정답 입력 후 Enter" disabled onkeydown="checkEnter(event)">
        <div id="result-msg"></div>
    </div>

    <button id="start-btn" onclick="startGame()">🎮 게임 시작!</button>

    <script>
        const quizData = [
            { initials: "ㄹㄱㅇㅂㄹㅈㄷ", answer: "리그오브레전드", hint: "유명한 5v5 MOBA 게임" },
            { initials: "ㅁㅌㅊㅋ", answer: "민트초코", hint: "호불호 끝판왕 디저트" },
            { initials: "ㅂㄷㄱ", answer: "비둘기", hint: "길거리 구곡물 섭취자" },
            { initials: "ㅋㅍㅇ", answer: "커피", hint: "잠 깨려고 마시는 음료" },
            { initials: "ㅍㅇㅆ", answer: "피씨방", hint: "친구들과 라면 먹으러 가는데" },
            { initials: "ㅊㅋ", answer: "치킨", hint: "승리했을 때 먹는 음식" },
            { initials: "ㄷㄱㅂㅁ", answer: "닭갈비", hint: "철판에 볶아먹는 맛있는 요리" },
            { initials: "ㅎㅂㄱ", answer: "햄버거", hint: "패스트푸드 대표 메뉴" }
        ];

        let currentQuiz = {};
        let score = 0;
        let timeLeft = 30;
        let timer;
        let isPlaying = false;

        const hintEl = document.getElementById("hint-text");
        const initialsEl = document.getElementById("initials-text");
        const inputEl = document.getElementById("user-input");
        const scoreEl = document.getElementById("score");
        const timeEl = document.getElementById("time");
        const startBtn = document.getElementById("start-btn");
        const resultEl = document.getElementById("result-msg");

        function startGame() {
            score = 0;
            timeLeft = 30;
            isPlaying = true;
            scoreEl.innerText = score;
            timeEl.innerText = timeLeft;
            startBtn.style.display = "none";
            inputEl.disabled = false;
            inputEl.focus();

            nextQuiz();

            timer = setInterval(() => {
                timeLeft--;
                timeEl.innerText = timeLeft;
                if (timeLeft <= 0) {
                    endGame();
                }
            }, 1000);
        }

        function nextQuiz() {
            const randomIndex = Math.floor(Math.random() * quizData.length);
            currentQuiz = quizData[randomIndex];
            hintEl.innerText = "💡 힌트: " + currentQuiz.hint;
            initialsEl.innerText = currentQuiz.initials;
            inputEl.value = "";
            resultEl.innerText = "";
        }

        function checkEnter(e) {
            if (e.key === "Enter" && isPlaying) {
                const val = inputEl.value.trim().replace(/\s+/g, "");
                if (val === currentQuiz.answer) {
                    score += 100;
                    scoreEl.innerText = score;
                    resultEl.style.color = "#4ade80";
                    resultEl.innerText = "⭕ 정답! (+100점)";
                    nextQuiz();
                } else {
                    resultEl.style.color = "#f87171";
                    resultEl.innerText = "❌ 땡! 다시 생각해보세요.";
                }
            }
        }

        function endGame() {
            isPlaying = false;
            clearInterval(timer);
            inputEl.disabled = true;
            hintEl.innerText = "🏆 게임 종료!";
            initialsEl.innerText = "🎉";
            resultEl.style.color = "#facc15";
            resultEl.innerText = "최종 점수: " + score + "점";
            startBtn.innerText = "🔄 다시 하기";
            startBtn.style.display = "inline-block";
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=520)
