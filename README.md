
# Getting Started

### Requirements(linux)
python -m venv .env   
source .env/bin/activate  
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

### Requirements(windows)
python -m venv .env   
cd .env/bin/activate 
activate.bat
cd ../..
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

### 生成requirements.txt
pip freeze > requirements.txt

