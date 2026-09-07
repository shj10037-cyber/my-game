import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="2D 아케이드 슈팅", page_icon="🚀", layout="centered")

st.title("🚀 우주 슈팅 아케이드 게임")
st.write("💡 **게임 시작 전 아래 검은색 게임 화면을 마우스로 한 번 클릭하세요!**")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
        }
        body {
            margin: 0;
            padding: 0;
            background-color: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: #fff;
            font-family: sans-serif;
            overflow: hidden;
        }
        #gameCanvas {
            border: 2px solid #00ffcc;
            box-shadow: 0 0 15px #00ffcc;
            background: #0d0f18;
            cursor: pointer;
        }
        .info {
            margin-top: 10px;
            font-size: 14px;
            color: #00ffcc;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="500" height="550" tabindex="1"></canvas>
    <div class="info">🎮 조작법: [←][→] 이동 | [Space] 미사일 발사</div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // 게임 시작 시 바로 키보드 포커스 맞추기
        window.onload = () => { canvas.focus(); };
        canvas.addEventListener("click", () => { canvas.focus(); });

        let player = { x: 230, y: 470, width: 40, height: 40, speed: 7, hp: 100 };
        let bullets = [];
        let enemies = [];
        let score = 0;
        let gameOver = false;
        let keys = {};

        // 방향키 및 스페이스바 입력 시 브라우저 스크롤 방지
        window.addEventListener("keydown", (e) => {
            if (["ArrowLeft", "ArrowRight", "Space", "ArrowUp", "ArrowDown"].includes(e.code)) {
                e.preventDefault();
            }
            keys[e.code] = true;
        }, false);

        window.addEventListener("keyup", (e) => {
            keys[e.code] = false;
        }, false);

        function spawnEnemy() {
            if (gameOver) return;
            let size = Math.random() * 20 + 20;
            enemies.push({
                x: Math.random() * (canvas.width - size),
                y: -size,
                width: size,
                height: size,
                speed: Math.random() * 2 + 2
            });
        }
        setInterval(spawnEnemy, 700);

        let lastShot = 0;
        function shoot() {
            let now = Date.now();
            if (now - lastShot > 120) {
                bullets.push({ x: player.x + player.width / 2 - 3, y: player.y, width: 6, height: 12, speed: 9 });
                lastShot = now;
            }
        }

        function update() {
            if (gameOver) return;

            if (keys["ArrowLeft"] && player.x > 0) player.x -= player.speed;
            if (keys["ArrowRight"] && player.x < canvas.width - player.width) player.x += player.speed;
            if (keys["Space"]) shoot();

            for (let i = bullets.length - 1; i >= 0; i--) {
                bullets[i].y -= bullets[i].speed;
                if (bullets[i].y < 0) bullets.splice(i, 1);
            }

            for (let i = enemies.length - 1; i >= 0; i--) {
                enemies[i].y += enemies[i].speed;

                if (
                    player.x < enemies[i].x + enemies[i].width &&
                    player.x + player.width > enemies[i].x &&
                    player.y < enemies[i].y + enemies[i].height &&
                    player.y + player.height > enemies[i].y
                ) {
                    player.hp -= 20;
                    enemies.splice(i, 1);
                    if (player.hp <= 0) gameOver = true;
                    continue;
                }

                for (let j = bullets.length - 1; j >= 0; j--) {
                    if (
                        bullets[j].x < enemies[i].x + enemies[i].width &&
                        bullets[j].x + bullets[j].width > enemies[i].x &&
                        bullets[j].y < enemies[i].y + enemies[i].height &&
                        bullets[j].y + bullets[j].height > enemies[i].y
                    ) {
                        enemies.splice(i, 1);
                        bullets.splice(j, 1);
                        score += 100;
                        break;
                    }
                }

                if (enemies[i] && enemies[i].y > canvas.height) {
                    enemies.splice(i, 1);
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (gameOver) {
                ctx.fillStyle = "#ff0055";
                ctx.font = "bold 32px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);
                ctx.fillStyle = "#fff";
                ctx.font = "18px sans-serif";
                ctx.fillText("최종 점수: " + score, canvas.width / 2, canvas.height / 2 + 20);
                ctx.fillText("화면을 새로고침(F5)하여 다시 시작", canvas.width / 2, canvas.height / 2 + 60);
                return;
            }

            // 비행기 그리기
            ctx.fillStyle = "#00ffcc";
            ctx.beginPath();
            ctx.moveTo(player.x + player.width / 2, player.y);
            ctx.lineTo(player.x, player.y + player.height);
            ctx.lineTo(player.x + player.width, player.y + player.height);
            ctx.closePath();
            ctx.fill();

            // 총알
            ctx.fillStyle = "#ffea00";
            bullets.forEach(b => ctx.fillRect(b.x, b.y, b.width, b.height));

            // 적
            ctx.fillStyle = "#ff0055";
            enemies.forEach(e => ctx.fillRect(e.x, e.y, e.width, e.height));

            // 점수 및 체력
            ctx.fillStyle = "#fff";
            ctx.font = "bold 16px sans-serif";
            ctx.textAlign = "left";
            ctx.fillText("점수: " + score, 15, 30);
            ctx.fillText("체력: " + player.hp, 15, 55);
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

components.html(game_html, height=620)
