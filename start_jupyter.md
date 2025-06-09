## 🚀 使用 nohup 后台启动 Jupyter Lab 的完整教程

### ✅ 步骤 1：设置 Token（提高安全性）

使用 `./generate_token.py` 文件生成 token 随机码

🔧 方法一：临时设置（推荐测试用）

在命令行中临时设置：
```bash
export JPY_TOKEN="your-token"
```
这只在当前终端有效。

🔧 方法二：永久设置（推荐长期使用）

将 token 写入 `~/.bashrc` 或 `~/.zshrc`：
```bash
echo "export JPY_TOKEN=your-token" >> ~/.bashrc
source ~/.bashrc
```

⸻

### ✅ 步骤 2：使用 nohup 命令启动 Jupyter Lab

在你的项目目录下运行以下命令：
```bash
nohup jupyter lab --ip=0.0.0.0 --port=8000 --NotebookApp.token=$JPY_TOKEN --notebook-dir=./ &
```
参数说明：
--ip=0.0.0.0	监听所有 IP，允许远程访问
--port=8000	设置端口为 8000
--NotebookApp.token=$JPY_TOKEN	使用自定义 token
--notebook-dir=./	指定工作目录（你可以改为绝对路径）
& 符号将命令放入后台执行。 这意味着命令会在后台运行，而不会阻塞当前的终端会话

执行成功后，你会看到提示：
```bash
nohup: ignoring input and appending output to 'nohup.out'
```
Jupyter Lab 就在后台运行了。

⸻

### ✅ 步骤 3：检查是否运行成功，并处理冲突

🔍 1. 检查运行状态
```bash
ps -ef | grep jupyter
```
你应该能看到包含 jupyter-lab 的进程，说明已成功运行。

🔍 2. 检查是否成功监听端口
```bash
lsof -i:8000
```
输出中应包含：
```bash
jupyter-lab  ...  TCP *:8000 (LISTEN)
```
表示端口 8000 已成功绑定。

❌ 3. 如果启动失败或端口冲突

你可能看到两个进程使用同一个端口：
```bash
ps -ef | grep jupyter
```
此时你需要 kill 掉旧的冲突进程：
```bash
kill <旧进程PID>
```
比如：
```bash
kill 2758220
```
然后重新运行 nohup 命令。

⸻

### ✅ 步骤 4：在浏览器访问 Jupyter Lab

📍 格式：
```bash
http://<服务器IP>:8000/?token=你的token
```
例如：
```bash
http://192.168.1.100:8000/?token=MySecureToken123
```
	•	若在本机使用浏览器访问，IP 就是 localhost 或 127.0.0.1
	•	若你在远程服务器运行 Jupyter，需要使用该服务器的公网或内网 IP

⸻

🧱 补充说明：
	•	若你是公网服务器，确保已开放端口 8000
	•	若是内网访问，可使用 ssh -L 命令建立本地端口转发
	•	你可以用 tail -f jupyter.log 查看运行日志

⸻

✅ 示例总结
```bash
export JPY_TOKEN=MySecureToken123
nohup jupyter lab --ip=0.0.0.0 --port=8000 --NotebookApp.token=$JPY_TOKEN --notebook-dir=./ > jupyter.log 2>&1 &
```
浏览器访问：
```bash
http://<你的服务器IP>:8000/?token=MySecureToken123
```