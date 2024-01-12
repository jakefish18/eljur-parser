# eljur-parser
Parser for eljur written using Python.

## Getting started

### Installation
First clone the repository using the next command in terminal
```
git clone https://github.com/jakefish18/eljur-parser.git
```
Go to the directory where you cloned the derictory and create venv for project with next command
```
python -m venv venv/
```
To activate venv you need next command for bash shell
```
source venv/activate/bin
```
for fish shell
```
source venv/activate/bin.fish
```
Install requirements using pip
```
pip install -r requirements.txt
```

### Using
After you have installed everything, you need change the environment variable using in the programm.

Create .env file in the same directory as ```eljur_parser.py```
```
touch .env
```
And edit with favorite text redactor. Example is below
```
# Eljur user settings.
USER_NAME = ""
USER_PASSWORD = ""

# Project settings.
STUDENT_DATA_STORE_PATH = ""
```

After all you can run ```eljur_parser.py``` with command
```
python3 eljur_parser.py
```
All files will be saved in student_data folder with .xslx file format.

