# GarminBot

(With the help of ChatGPT, Github Copilot and Claude)

### Overview :

GarminBot is an automated tool designed to send weekly summaries of your Garmin Connect activities and overall health via email on Tuesdays for the week prior.

### Usage :

- Create a python virtual environment
- Install the requirements
- Set the ```OPENAI_API_KEY```, ```MY_EMAIL```, ```GARMIN_CONNECT_PSW```, ```GARMINBOT_APP_PSW``` and ```SENDER_EMAIL``` environment variables (explainations : In this case ```MY_EMAIL``` is both the garmin account email and the receiver of the weekly review, ```GARMINBOT_APP_PSW``` is the app password of the sender email)
- Set the daily execution of ```main.py``` (can be done easily with anacron under linux)