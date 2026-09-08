import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="스피드 가위바위보", page_icon="✊", layout="centered")

st.title("✊✌️🖐️ [30초 스피드] 가위바위보 카드 배틀")
st.write("상대가 낸 카드를 보고 이기는 카드를 누구보다 빠르게 클릭하세요!")

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
            font-family: sans-serif;
            text-align: center;
        }
        #game-card {
            width: 450px;
            padding: 20px;
            background: #1e293b;
            border: 3px solid #10b981;
            border-radius: 12px;
            margin: 15px auto;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }
        .enemy-box {
            margin: 15px 0;
        }
        .enemy-card {
            font-size: 80px;
            margin: 10px 0;
        }
        .btn-group {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }
        .choice-btn {
            font-size: 40px;
            padding: 15px 25px;
            background: #334155;
            border: 2px solid #10b981;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.1s, background 0.2s;
        }
        .choice-btn:hover {
            background: #475569;
            transform: scale(1.05);
        }
        .choice-btn:active {
            transform: scale(0.95);
        }
        .hud {
            display: flex;
            justify-content: space-around;
            width: 450px;
            margin: 0 auto;
            font-size: 20px;
            font-weight: bold;
        }
        #start-btn {
            padding: 12px 24px;
            font-size: 18px;
            background-color: #10b981;
            color: #0f172a;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 10px;
        }
        #start-btn:hover { background-color: #34d399; }
        #result-msg {
            font-size: 18px;
            height: 30px;
            margin-top: 15px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="hud">
        <div>점수: <span id="score">0</span></div>
        <div>남은 시간: <span id="time">30</span>초</div>
    </div>

    <div id="game-card">
        <div class="enemy-box">
            <div style="font-size: 18px; color: #94a3b8;">상대방의 카드</div>
            <div class="enemy-card" id="enemy-display">❓</div>
        </div>
        
        <div style="font-size: 16px; color: #cbd5e1;">이기는 카드를 누르세요!</div>
        <div class="btn-group">
            <button class="choice-btn" onclick="play('scissors')">✌️</button>
            <button class="choice-btn" onclick="play('rock')">✊</button>
            <button class="choice-btn" onclick="play('paper')">🖐️</button>
        </div>
        <div id="result-msg"></div>
    </div>

    <button id="start-btn" onclick="startGame()">🎮 게임 시작!</button>

    <script>
        const choices = ['scissors', 'rock', 'paper'];
        const emojiMap = { 'scissors': '✌️', 'rock': '✊', 'paper': '🖐️' };
        const winMap = { 'scissors': 'rock', 'rock': 'paper', 'paper': 'scissors' }; // 내가 이기려면 내야 하는 카드

        let currentEnemy = '';
        let score = 0;
        let timeLeft = 30;
        let timer;
        let isPlaying = false;
        let isLock = false;

        const enemyEl = document.getElementById("enemy-display");
        const scoreEl = document.getElementById("score");
        const timeEl = document.getElementById("time");
        const startBtn = document.getElementById("start-btn");
        const resultEl = document.getElementById("result-msg");

        function startGame() {
            score = 0;
            timeLeft = 30;
            isPlaying = true;
            isLock = false;
            scoreEl.innerText = score;
            timeEl.innerText = timeLeft;
            startBtn.style.display = "none";
            resultEl.innerText = "";

            nextRound();

            timer = setInterval(() => {
                timeLeft--;
                timeEl.innerText = timeLeft;
                if (timeLeft <= 0) {
                    endGame();
                }
            }, 1000);
        }

        function nextRound() {
            const randomIndex = Math.floor(Math.random() * choices.length);
            currentEnemy = choices[randomIndex];
            enemyEl.innerText = emojiMap[currentEnemy];
            isLock = false;
        }

        function play(myChoice) {
            if (!isPlaying || isLock) return;
            isLock = true;

            const correctChoice = winMap[currentEnemy];

            if (myChoice === correctChoice) {
                score += 100;
                scoreEl.innerText = score;
                resultEl.style.color = "#4ade80";
                resultEl.innerText = "⭕ 승리! (+100점)";
                setTimeout(() => {
                    resultEl.innerText = "";
                    nextRound();
                }, 300);
            } else {
                score = Math.max(0, score - 50);
                scoreEl.innerText = score;
                resultEl.style.color = "#f87171";
                resultEl.innerText = `❌ 오답! 정답: [${emojiMap[correctChoice]}] (-50점)`;
                setTimeout(() => {
                    resultEl.innerText = "";
                    nextRound();
                }, 800);
            }
        }

        function endGame() {
            isPlaying = false;
            clearInterval(timer);
            enemyEl.innerText = "🏆";
            resultEl.style.color = "#facc15";
            resultEl.innerText = "게임 종료! 최종 점수: " + score + "점";
            startBtn.innerText = "🔄 다시 하기";
            startBtn.style.display = "inline-block";
        }
    </script>
</body>
</html>
