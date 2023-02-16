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

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

current_time = datetime.datetime.now()

date = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day)

weekno = datetime.datetime.today().weekday()


#debug tools
# date = '2023-01-21'
# weekno = 5

response = requests.get("https://api.dineoncampus.com/v1/location/5b10d972f3eeb60909e01489/periods/?platform=1&date="+date)

lunchID = response.json()['periods'][1]['id']
dinnerID = response.json()['periods'][2]['id']

responseL = requests.get("https://api.dineoncampus.com/v1/location/5b10d972f3eeb60909e01489/periods/"+lunchID+"?platform=1&date="+date)
responseD = requests.get("https://api.dineoncampus.com/v1/location/5b10d972f3eeb60909e01489/periods/"+dinnerID+"?platform=1&date="+date)

#get 'desc' 'name'

# Weekdays:
'''                     #weekend lunch has no rooted, dinner does??
0: Homestyle -> 0       | 0
1: Create -> delete     | delete
2: Rooted -> 1          | delete
3: Global Halal -> delete | delete
4: Salad Bar -> 2       | 1
5: Pasta -> delete      | delete
6: Pizza -> 3           | 2
7: Grill -> 4           | 3
8: Soup -> 5            | 4
9: Deli -> 6            | 5
10: Bakery-Dessert -> 7 | 6
'''

#Weekends:
'''
0: Homestyle
1: Rooted
2: Salad Bar
3: Pizza
4: Grill
5: Daily Chef Soups
6: Deli
7: Bakery-Dessert
'''

def weekendFix(stations,is_dinner):
    retlist = []
    if is_dinner:
        for x in stations:
            if x == 0:
                retlist.append(0)
            elif x == 1:
                pass
            elif x == 2:
                retlist.append(1)
            elif x == 3:
                pass
            elif x == 4:
                retlist.append(2)
            elif x == 5:
                pass
            elif x == 6:
                retlist.append(3)
            elif x == 7:
                retlist.append(4)
            elif x == 8:
                retlist.append(5)
            elif x == 9:
                retlist.append(6)
            elif x == 10:
                retlist.append(7)
    else:
        for x in stations:
            if x == 0:
                retlist.append(0)
            elif x == 1:
                pass
            elif x == 2:
                pass
            elif x == 3:
                pass
            elif x == 4:
                retlist.append(1)
            elif x == 5:
                pass
            elif x == 6:
                retlist.append(2)
            elif x == 7:
                retlist.append(3)
            elif x == 8:
                retlist.append(4)
            elif x == 9:
                retlist.append(5)
            elif x == 10:
                retlist.append(6)
    return retlist

def createResponseLunch(stations):
    lunch = '--Lunch--\n'
    if weekno >= 5:
        stations = weekendFix(stations,0)
    for x in stations:
        lunch += str(responseL.json()['menu']['periods']['categories'][x]['name']) + ":\n"
        for i in responseL.json()['menu']['periods']['categories'][x]['items']:
            lunch += str(i['name']) + "\n"
        lunch += "\n"
    return lunch.encode('utf-8')


def createResponseDinner(stations):
    dinner = '--Dinner--\n'
    if weekno >= 5:
        stations = weekendFix(stations,1)
    for x in stations:
        dinner += str(responseD.json()['menu']['periods']['categories'][x]['name']) + ":\n"
        for i in responseD.json()['menu']['periods']['categories'][x]['items']:
            dinner += str(i['name']) + "\n"
        dinner += "\n"
    return dinner.encode('utf-8')


#debug tools
# print(createResponseLunch([0,1,3,7,8]))
# print(createResponseDinner([0,1,3,7,8]))

# print(createResponseLunch([0,1,2,3,4,5,6,7,8,9]))
# print(createResponseDinner([0,1,2,3,4,5,6,7,8,9]))


#user
send_message('[phone number removed]', '[carrier]',createResponseLunch([0,1,3,7]))
send_message('[phone number removed]', '[carrier]',createResponseDinner([0,1,3,7]))
