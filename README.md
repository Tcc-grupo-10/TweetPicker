# TweetPicker

#### Install Windows
    - Python 2.7
        - https://www.python.org/download/releases/2.7/
        - Export C:\Python27\ as env vars
            - Control Panel\System and Security\System -> Advanced System Settings -> Environment Variables -> Edit PATH
            - Remembering: Every export, you should close all your CMD windows
    - PIP install: 
        - Inside of this folder, run: 
            - python get-pip.py
        - Export the C:\Python27\Scripts as env var
    - PIP packages
        - pip install boto3
        - pip install unidecode
        - pip install emoji
        
        
#### Accounts to create
    - Twitter
        - Create a new app:
            - https://apps.twitter.com/
            - Choose a good name ;)
        - Save the Consumer Key/Consumer Secret at the "Keys and Access Tokens" tab 
        
#### Running 
    - Windows:
        - Edit the run.bat file and push your credentials
        - Just double click on it! (Windows been Windows)
    - Mac/Linux:
        - Edit the run.sh file and push your credentials
        - On terminal:
            - ./run.sh
        
    - DO NOT COMMIT/PUSH TO GITHUB THIS FILE!! 