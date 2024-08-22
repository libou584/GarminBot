import garminconnect
import datetime
import os



def addSleepData(client, date) :
    promptpart = "Sleep data :\n"
    for i in range(1, 8) :
        sleep = client.get_sleep_data((date - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        promptpart += "On day " + str(i) + ", sleep time : " + str(round(sleep["dailySleepDTO"]["sleepTimeSeconds"]/3600, 1)) + " hours, resting heart rate : " + str(sleep["restingHeartRate"]) + "\n"
    return promptpart + "\n"


def addDailyStepsData(client, date) :
    promptpart = "Daily steps data :\n"
    steps = client.get_daily_steps((date - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    for i in range(7) :
        promptpart += "On day " + str(i+1) + ", steps : " + str(steps[i]["totalSteps"]) + "\n"
    return promptpart + "\n"


def main() :

    client = garminconnect.Garmin(os.environ["GARMIN_CONNECT_EMAIL"], os.environ["GARMIN_CONNECT_PSW"])
    client.login()

    # date = datetime.datetime.today()
    date = datetime.datetime(2024, 8, 19)

    prompt = "You are a personal health assistant analyzing my weekly health data. Your task is to provide insights, and offer recommendations based on the following data of the last 7 days :\n\n"
    prompt += addSleepData(client, date)
    prompt += addDailyStepsData(client, date)

    print(prompt)
    # activity = client.get_stress_data("2024-08-12")["avgStressLevel"]
    # activity = client.get_activities_by_date("2024-08-19", "2024-08-22")
    # for a in activity:
    #     print(a["activityType"]["typeKey"])
    # print(activity)


if __name__ == "__main__" :
    main()