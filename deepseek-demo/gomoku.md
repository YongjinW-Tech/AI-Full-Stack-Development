# 五子棋游戏 HTML 实现

以下是一个完整的五子棋游戏 HTML 实现，所有代码都在一个 HTML 文件中：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>五子棋游戏</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f5f5dc;
            margin: 0;
            padding: 20px;
        }
        
        h1 {
            color: #8B4513;
            margin-bottom: 10px;
        }
        
        .game-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
        }
        
        .board-container {
            position: relative;
            margin-bottom: 20px;
        }
        
        #board {
            background-color: #DEB887;
            border: 2px solid #8B4513;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        }
        
        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        button {
            padding: 8px 15px;
            background-color: #8B4513;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        
        button:hover {
            background-color: #A0522D;
        }
        
        .status {
            font-size: 18px;
            font-weight: bold;
            color: #8B4513;
            margin-bottom: 15px;
            height: 24px;
        }
        
        .game-info {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>五子棋游戏</h1>
    
    <div class="game-container">
        <div class="status" id="status">黑方回合</div>
        
        <div class="board-container">
            <canvas id="board" width="450" height="450"></canvas>
        </div>
        
        <div class="controls">
            <button id="restart">重新开始</button>
            <button id="undo">悔棋</button>
        </div>
    </div>
    
    <div class="game-info">
        <h3>游戏规则：</h3>
        <p>1. 黑方先行，双方轮流在棋盘上下子</p>
        <p>2. 先在横、竖或斜方向连成五子的一方获胜</p>
        <p>3. 点击"悔棋"可以撤销上一步操作</p>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const canvas = document.getElementById('board');
            const ctx = canvas.getContext('2d');
            const statusDisplay = document.getElementById('status');
            const restartButton = document.getElementById('restart');
            const undoButton = document.getElementById('undo');
            
            const BOARD_SIZE = 15;
            const CELL_SIZE = canvas.width / BOARD_SIZE;
            const PIECE_RADIUS = CELL_SIZE * 0.4;
            
            let board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(0));
            let currentPlayer = 1; // 1 for black, 2 for white
            let gameOver = false;
            let moveHistory = [];
            
            // 初始化棋盘
            function initBoard() {
                // 绘制棋盘背景
                ctx.fillStyle = '#DEB887';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // 绘制网格线
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 1;
                
                for (let i = 0; i < BOARD_SIZE; i++) {
                    // 横线
                    ctx.beginPath();
                    ctx.moveTo(CELL_SIZE / 2, i * CELL_SIZE + CELL_SIZE / 2);
                    ctx.lineTo(canvas.width - CELL_SIZE / 2, i * CELL_SIZE + CELL_SIZE / 2);
                    ctx.stroke();
                    
                    // 竖线
                    ctx.beginPath();
                    ctx.moveTo(i * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE / 2);
                    ctx.lineTo(i * CELL_SIZE + CELL_SIZE / 2, canvas.height - CELL_SIZE / 2);
                    ctx.stroke();
                }
                
                // 绘制五个星位点
                const starPoints = [3, 7, 11];
                ctx.fillStyle = '#000000';
                
                for (let i of starPoints) {
                    for (let j of starPoints) {
                        ctx.beginPath();
                        ctx.arc(
                            i * CELL_SIZE + CELL_SIZE / 2,
                            j * CELL_SIZE + CELL_SIZE / 2,
                            CELL_SIZE * 0.1,
                            0,
                            Math.PI * 2
                        );
                        ctx.fill();
                    }
                }
            }
            
            // 绘制棋子
            function drawPiece(x, y, player) {
                const centerX = x * CELL_SIZE + CELL_SIZE / 2;
                const centerY = y * CELL_SIZE + CELL_SIZE / 2;
                
                // 绘制棋子阴影
                ctx.beginPath();
                ctx.arc(centerX, centerY, PIECE_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = player === 1 ? '#333333' : '#DDDDDD';
                ctx.fill();
                
                // 绘制棋子高光
                if (player === 1) {
                    ctx.beginPath();
                    ctx.arc(centerX - PIECE_RADIUS * 0.3, centerY - PIECE_RADIUS * 0.3, PIECE_RADIUS * 0.1, 0, Math.PI * 2);
                    ctx.fillStyle = '#666666';
                    ctx.fill();
                } else {
                    ctx.beginPath();
                    ctx.arc(centerX - PIECE_RADIUS * 0.2, centerY - PIECE_RADIUS * 0.2, PIECE_RADIUS * 0.15, 0, Math.PI * 2);
                    ctx.fillStyle = '#FFFFFF';
                    ctx.fill();
                }
            }
            
            // 检查是否获胜
            function checkWin(x, y, player) {
                const directions = [
                    [1, 0],   // 水平
                    [0, 1],   // 垂直
                    [1, 1],   // 对角线
                    [1, -1]   // 反对角线
                ];
                
                for (const [dx, dy] of directions) {
                    let count = 1;
                    
                    // 正向检查
                    for (let i = 1; i < 5; i++) {
                        const nx = x + i * dx;
                        const ny = y + i * dy;
                        if (nx >= 0 && nx < BOARD_SIZE && ny >= 0 && ny < BOARD_SIZE && board[nx][ny] === player) {
                            count++;
                        } else {
                            break;
                        }
                    }
                    
                    // 反向检查
                    for (let i = 1; i < 5; i++) {
                        const nx = x - i * dx;
                        const ny = y - i * dy;
                        if (nx >= 0 && nx < BOARD_SIZE && ny >= 0 && ny < BOARD_SIZE && board[nx][ny] === player) {
                            count++;
                        } else {
                            break;
                        }
                    }
                    
                    if (count >= 5) {
                        return true;
                    }
                }
                
                return false;
            }
            
            // 检查是否平局
            function checkDraw() {
                for (let i = 0; i < BOARD_SIZE; i++) {
                    for (let j = 0; j < BOARD_SIZE; j++) {
                        if (board[i][j] === 0) {
                            return false;
                        }
                    }
                }
                return true;
            }
            
            // 处理点击事件
            function handleClick(event) {
                if (gameOver) return;
                
                const rect = canvas.getBoundingClientRect();
                const x = Math.floor((event.clientX - rect.left) / CELL_SIZE);
                const y = Math.floor((event.clientY - rect.top) / CELL_SIZE);
                
                if (x >= 0 && x < BOARD_SIZE && y >= 0 && y < BOARD_SIZE && board[x][y] === 0) {
                    // 记录移动历史
                    moveHistory.push({x, y, player: currentPlayer});
                    
                    // 更新棋盘
                    board[x][y] = currentPlayer;
                    drawPiece(x, y, currentPlayer);
                    
                    // 检查胜负
                    if (checkWin(x, y, currentPlayer)) {
                        gameOver = true;
                        statusDisplay.textContent = currentPlayer === 1 ? '黑方获胜！' : '白方获胜！';
                        return;
                    }
                    
                    // 检查平局
                    if (checkDraw()) {
                        gameOver = true;
                        statusDisplay.textContent = '平局！';
                        return;
                    }
                    
                    // 切换玩家
                    currentPlayer = currentPlayer === 1 ? 2 : 1;
                    statusDisplay.textContent = currentPlayer === 1 ? '黑方回合' : '白方回合';
                }
            }
            
            // 重新开始游戏
            function restartGame() {
                board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(0));
                currentPlayer = 1;
                gameOver = false;
                moveHistory = [];
                statusDisplay.textContent = '黑方回合';
                initBoard();
            }
            
            // 悔棋
            function undoMove() {
                if (gameOver || moveHistory.length === 0) return;
                
                const lastMove = moveHistory.pop();
                board[lastMove.x][lastMove.y] = 0;
                currentPlayer = lastMove.player;
                gameOver = false;
                statusDisplay.textContent = currentPlayer === 1 ? '黑方回合' : '白方回合';
                
                // 重绘整个棋盘
                initBoard();
                for (const move of moveHistory) {
                    drawPiece(move.x, move.y, move.player);
                }
            }
            
            // 事件监听
            canvas.addEventListener('click', handleClick);
            restartButton.addEventListener('click', restartGame);
            undoButton.addEventListener('click', undoMove);
            
            // 初始化游戏
            initBoard();
        });
    </script>
</body>
</html>
```

## 游戏功能说明

1. **基本功能**：
   - 15×15 标准五子棋棋盘
   - 黑方先行，双方轮流下子
   - 自动判断胜负（横、竖、斜方向连成五子）
   - 自动判断平局（棋盘填满无胜负）

2. **操作功能**：
   - 点击棋盘下子
   - 重新开始按钮
   - 悔棋按钮（可撤销上一步操作）

3. **界面设计**：
   - 木质风格的棋盘
   - 黑白棋子有立体效果
   - 清晰的游戏状态显示
   - 游戏规则说明

4. **响应式设计**：
   - 适应不同屏幕尺寸
   - 清晰的视觉反馈

您可以将这段代码保存为HTML文件（例如`gomoku.html`），然后在浏览器中打开即可开始游戏。