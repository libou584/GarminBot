import garminconnect
import datetime
import os
import openai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def addSleepData(client, date) :
    promptpart = "Sleep data (sleep time and resting heart rate) :\n"
    for i in range(1, 8) :
        sleep = client.get_sleep_data((date - datetime.timedelta(days = i+1)).strftime("%Y-%m-%d"))
        promptpart += "On day " + str(i) + " : " + str(round(sleep["dailySleepDTO"]["sleepTimeSeconds"]/3600, 1)) + " hours, " + str(sleep["restingHeartRate"]) + " bpm\n"
    return promptpart + "\n"


def addDailyStepsData(client, date) :
    promptpart = "Daily steps data :\n"
    steps = client.get_daily_steps((date - datetime.timedelta(days = 8)).strftime("%Y-%m-%d"), (date - datetime.timedelta(days = 2)).strftime("%Y-%m-%d"))
    for i in range(7) :
        promptpart += "On day " + str(i+1) + " : " + str(steps[i]["totalSteps"]) + "\n"
    return promptpart + "\n"


def addStressData(client, date) :
    promptpart = "Average stress levels (out of 100) :\n"
    for i in range(1, 8) :
        stress = client.get_stress_data((date - datetime.timedelta(days=i+1)).strftime("%Y-%m-%d"))
        promptpart += "On day " + str(i) + " : " + str(stress["avgStressLevel"]) + "\n"
    return promptpart + "\n"


def addActivityMinutesData(client, date) :
    activities = client.get_activities_by_date((date - datetime.timedelta(days = 8)).strftime("%Y-%m-%d"), (date - datetime.timedelta(days = 2)).strftime("%Y-%m-%d"))
    totalMinutes = 0
    for activity in activities :
        totalMinutes += int(activity["duration"]/60)
    return "Activity data : " + str(totalMinutes) + " minutes total\n\n"


def main(date) :

    client = garminconnect.Garmin(os.environ["MY_EMAIL"], os.environ["GARMIN_CONNECT_PSW"])
    client.login()

    prompt = "You are a personal health assistant analyzing my weekly health data. Your task is to provide insights, and offer recommendations based on the following data of the last 7 days :\n\n"
    prompt += addSleepData(client, date)
    prompt += addDailyStepsData(client, date)
    prompt += addStressData(client, date)
    prompt += addActivityMinutesData(client, date)
    prompt += "Please analyze this information and provide:\n1. A summary of my overall health status\n2. Identification of any notable patterns or trends\n3. Personalized recommendations for improvement\n4. Any potential health concerns based on the data\n\n"
    prompt += "Focus on actionable insights and maintain a supportive, encouraging tone. If you notice any significant deviations from healthy norms, please highlight them.\n\nConstraints:\n- Do not diagnose specific medical conditions\n- Limit your analysis to the data provided\n- Express uncertainty when appropriate\n\nYour response should be concise yet informative, around 200 words. Answer in plain text with no bold text."

    # print(prompt)

    client = openai.OpenAI()
    completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    # print(completion.choices[0].message.content)

    sender_email = os.environ["SENDER_EMAIL"]
    password = os.environ["GARMINBOT_APP_PSW"]
    receiver_email = os.environ["MY_EMAIL"]

    subject = "[Automated Email] Weekly Health Review"
    body = completion.choices[0].message.content

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()




if __name__ == "__main__" :
    date = datetime.datetime.today()
    if date.weekday() == 1 :
        main(date)