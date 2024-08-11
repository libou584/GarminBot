import garminconnect
import datetime
import matplotlib.pyplot as plt
import os






if __name__ == "__main__" :

    client = garminconnect.Garmin(os.environ["GARMIN_CONNECT_EMAIL"], os.environ["GARMIN_CONNECT_PSW"])
    client.login()


    activity = client.get_steps_data()
    for key in activity.keys() :
        print(key)
