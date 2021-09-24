import requests
from bs4 import BeautifulSoup
import json


web_hook = "https://chat.googleapis.com/v1/spaces/AAAApHe5z1c/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=PevrVu-x86rutudUyoa-Bn5lQ8rWZIE94B1schr5UQ0%3D"

# Iterate through days from current date to https://www.lohitennis.com/classes/2021-10-28/
list_of_days = []
i = 1
x = 27

while (x < 31):
    list_of_days.append("https://www.lohitennis.com/classes/2021-{month}-{day}/".format(month = "09", day = x))
    x += 1
while (i < 30):
    list_of_days.append("https://www.lohitennis.com/classes/2021-{month}-{day}/".format(month = "10", day = i))
    i += 1

my_schedule = [
    "September 28",
    "October 7",
    "October 14",
    "October 20",
    "October 21",
    "October 28"
]

def send_class_to_chat(event):
    date = str(event.find(class_="tribe-event-date-start").get_text().strip())
    title = str(event.find(class_="tribe-events-calendar-day__event-title-link").get_text().strip())
    spots = str(event.find(class_="tribe-events-c-small-cta__stock").get_text().strip())
    url = str(event.find_all('a', href=True)[0]['href'])
    event_text = "{} \n{} \n{} \n{}".format(date, title, spots, url)
    data = json.dumps({'text': event_text})
    r = requests.post(web_hook, data=data)
    print(r.status_code)

def print_class(event):
    print("*" * 20)
    print(event.find(class_="tribe-event-date-start").get_text().strip())
    print(event.find(class_="tribe-events-calendar-day__event-title-link").get_text().strip())
    print(event.find(class_="tribe-events-c-small-cta__stock").get_text().strip()) #Event spots left
    links = (event.find_all('a', href=True))
    print(links[0]['href'])

def check_events(events):
    for event in events:
        # check whether title contains "Advanced"
        event_title = event.find(class_="tribe-events-calendar-day__event-title-link").get_text()
        if ("Advanced" or "Intermediate" in event_title) and ("Beginner" not in event_title):  #Event Title
        # if true; check if class is full
            try:
                event.find(class_="tribe-events-c-small-cta__stock").get_text()
                # Check if I already scheduled a class that day
                if (" ".join((event.find(class_="tribe-event-date-start").get_text().strip().split()[0:2]))) not in my_schedule:
                    # print_class(event)
                    send_class_to_chat(event)
                    print("New Class Available")
                else:
                    print("You already booked a class this day")
            except:
                continue
        else:
            continue

def main ():
    for url in list_of_days:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # find all tags with event CSS class
        events = soup.find_all(class_="tribe-events-calendar-day__event")
        check_events(events)



if __name__ == "__main__":
    main()