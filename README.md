# AI-Full-Stack-Development
This is a personal learning project designed to document and organize the learning process and code practices in "AI Full Stack Development". Through this project, I will systematically learn various aspects of AI full stack development.

### Acknowledgment
This project is built upon the course repository **DjangoPeng/deepseek-quickstart**（https://github.com/DjangoPeng/deepseek-quickstart）, which provided the initial structure and inspiration. Many thanks to the author for making it publicly available and well-structured for learners.

### Clone repository (pull code)
```bash
git clone https://github.com/YongjinW-Tech/AI-Full-Stack-Development.git
```
Enter the project directory:
```bash
cd AI-Full-Stack-Development
```

### Synchronize code
- If you need to synchronize code changes on GitHub locally, you can use the following command:
```bash
git pull origin main
```

### Install Miniconda

```shell
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

After installation, it is recommended to create a new Python virtual environment named 'ai-development'.

### (Optional) Create and activate virtual environments (Conda is recommended)

```shell
conda create -n ai-development python=3.13

# To activate this environment, use
conda activate ai-development

# To deactivate an active environment, use
conda deactivate
```

After each use, this environment needs to be activated.


### Install Python dependency packages `requirements.txt`

```shell
pip install -r requirements.txt
```

### Configure DeepSeek API Key

According to the command-line tool you are using, configure the `DEEPSEEK_API_KEY` environment variable in `~/.bashrc` or `~/.zshrc`:

```shell
export DEEPSEEK_API_KEY="xxxx"
```

### Install and configure Jupyter Lab

After installing the above development environment, use Miniconda to install **Jupyter Lab**:

```shell
conda install -c conda-forge jupyterlab
```

The best practice for developing with Jupyter-Lab is to have a background resident. Here are the relevant configurations (using root user as an example):

```shell
# Generate Jupyter Lab configuration file
jupyter lab --generate-config
```

After opening the configuration file `jupyter_1ab_comfig.py` that executes the output above, modify the following configuration items:

```python
c.ServerApp.allow_root = True  # Non root user startup, no modification required
c.ServerApp.ip = '*'
```

Starting Jupyter Lab with `nohup` backend
```shell
$ nohup jupyter lab --port=8000 --NotebookApp.token='Replace with your password' --notebook-dir=./ &
```

The logs output by Jupyter Lab will be saved in the `nohup.out` file (filtered in. gitignore).
