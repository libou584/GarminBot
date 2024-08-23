import garminconnect
import datetime
import os



def addSleepData(client, date) :
    promptpart = "Sleep data (sleep time and resting heart rate) :\n"
    for i in range(1, 8) :
        sleep = client.get_sleep_data((date - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        promptpart += "On day " + str(i) + " : " + str(round(sleep["dailySleepDTO"]["sleepTimeSeconds"]/3600, 1)) + " hours, " + str(sleep["restingHeartRate"]) + " bpm\n"
    return promptpart + "\n"


def addDailyStepsData(client, date) :
    promptpart = "Daily steps data :\n"
    steps = client.get_daily_steps((date - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    for i in range(7) :
        promptpart += "On day " + str(i+1) + " : " + str(steps[i]["totalSteps"]) + "\n"
    return promptpart + "\n"


def addStressData(client, date) :
    promptpart = "Average stress levels (out of 100) :\n"
    for i in range(1, 8) :
        stress = client.get_stress_data((date - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        promptpart += "On day " + str(i) + " : " + str(stress["avgStressLevel"]) + "\n"
    return promptpart + "\n"


def addActivityMinutesData(client, date) :
    activities = client.get_activities_by_date((date - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    totalMinutes = 0
    for activity in activities :
        totalMinutes += int(activity["duration"]/60)
    return "Activity data : " + str(totalMinutes) + " minutes total\n\n"


def main() :

    client = garminconnect.Garmin(os.environ["GARMIN_CONNECT_EMAIL"], os.environ["GARMIN_CONNECT_PSW"])
    client.login()

    # date = datetime.datetime.today()
    date = datetime.datetime(2024, 8, 19)

    prompt = "You are a personal health assistant analyzing my weekly health data. Your task is to provide insights, and offer recommendations based on the following data of the last 7 days :\n\n"
    prompt += addSleepData(client, date)
    prompt += addDailyStepsData(client, date)
    prompt += addStressData(client, date)
    prompt += addActivityMinutesData(client, date)

    print(prompt)


if __name__ == "__main__" :
    main()