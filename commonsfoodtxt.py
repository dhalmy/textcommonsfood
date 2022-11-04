import requests
import json
import smtplib
import datetime

# Set up to send texts
import response as response

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = ("[username removed]", "[password removed]")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
    server.sendmail(auth[0], recipient, message)
# end of texting

# Pulling Food data
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

current_time = datetime.datetime.now()

date = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day)

weekno = datetime.datetime.today().weekday()


response = requests.get("https://api.dineoncampus.com/v1/location/5b10d972f3eeb60909e01489/periods/?platform=1&date="+date)

lunchID = response.json()['periods'][1]['id']
dinnerID = response.json()['periods'][2]['id']

responseL = requests.get("https://api.dineoncampus.com/v1/location/5b10d972f3eeb60909e01489/periods/"+lunchID+"?platform=1&date="+date)
responseD = requests.get("https://api.dineoncampus.com/v1/location/5b10d972f3eeb60909e01489/periods/"+dinnerID+"?platform=1&date="+date)

#get 'desc' 'name'

# Weekdays:
'''
0: Homestyle -> 0
1: Create -> 1
2: Rooted -> 2
3: Global Halal -> delete
4: Pizza -> 3
5: Grill LTO ->4
6: Pasta Station -> delete
7: Daily Chef Soups -> 5
8: Bakery-Dessert -> 6
'''

#Weekends:
'''
0: Homestyle
1: Create
2: Rooted
3: Pizza
4: Grill LTO
5: Daily Chef Soups
6: Bakery-Dessert
'''

def weekendFix(stations): #python 3.9 doesn't support switch cases
    retlist = []
    for x in stations:
        if x == 0:
            retlist.append(0)
        elif x == 1:
            retlist.append(1)
        elif x == 2:
            retlist.append(2)
        elif x == 3:
            pass
        elif x == 4:
            retlist.append(3)
        elif x == 5:
            retlist.append(4)
        elif x == 6:
            pass
        elif x == 7:
            retlist.append(5)
        elif x == 8:
            retlist.append(6)
    return retlist

def createResponseLunch(stations):
    lunch = '--Lunch--\n'
    if weekno > 5:
        stations = weekendFix(stations)
    for x in stations:
        lunch += str(responseL.json()['menu']['periods']['categories'][x]['name']) + ":\n"
        for i in responseL.json()['menu']['periods']['categories'][x]['items']:
            lunch += str(i['name']) + "\n"
        lunch += "\n"
    return lunch


def createResponseDinner(stations):
    dinner = '--Dinner--\n'
    if weekno > 5:
        stations = weekendFix(stations)
    for x in stations:
        dinner += str(responseD.json()['menu']['periods']['categories'][x]['name']) + ":\n"
        for i in responseD.json()['menu']['periods']['categories'][x]['items']:
            dinner += str(i['name']) + "\n"
        dinner += "\n"
    return dinner


#user
send_message('[phone number removed]', '[carrier]',createResponseLunch([0,1,3,7]))
send_message('[phone number removed]', '[carrier]',createResponseDinner([0,1,3,7]))
