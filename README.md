# Tex2Lambda Web App
## Description
This flask app provides a graphical user interface for users to upload their latex file in which they want to convert to lambda feedback jsonfile and select the filter which they intend to use for the conversion. 
## Setup 
### Step 1: Clonning
```
git clone https://github.com/xavierfork/tex2lambda_web.git
cd tex2lambda_web

```
### Step 2: Install Necessary Packages
There are two ways to do this, one is to use:
```
poetry install
poetry shell
```
The second option is to：
```
# python >= 3.10

python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
### Step 3: Run
Run the line:
```
flask run
```
The flask app will be running on http://127.0.0.1:5000
