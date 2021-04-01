#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""A simple bot script, built on Flask.
This sample script leverages the Flask web service micro-framework
(see http://flask.pocoo.org/).  By default the web server will be reachable at
port 5000 you can change this default if desired (see `flask_app.run(...)`).
ngrok (https://ngrok.com/) can be used to tunnel traffic back to your server
if your machine sits behind a firewall.
You must create a Webex Teams webhook that points to the URL where this script
is hosted.  You can do this via the WebexTeamsAPI.webhooks.create() method.
Additional Webex Teams webhook details can be found here:
https://developer.webex.com/webhooks-explained.html
A bot must be created and pointed to this server in the My Apps section of
https://developer.webex.com.  The bot's Access Token should be added as a
'WEBEX_TEAMS_ACCESS_TOKEN' environment variable on the web server hosting this
script.
This script supports Python versions 2 and 3.
Copyright (c) 2016-2020 Cisco and/or its affiliates.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
from DeviceList import DeviceAPI
import pytz
import json
from datetime import datetime
from time import sleep
import VPBotCards
import os

__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__contributors__ = ["Brad Bester <brbester@cisco.com>"]
__copyright__ = "Copyright (c) 2016-2020 Cisco and/or its affiliates."
__license__ = "MIT"


from flask import Flask, request
import requests

from webexteamssdk import WebexTeamsAPI, Webhook


# Module constants
CAT_FACTS_URL = 'https://catfact.ninja/fact'


# Initialize the environment
# Create the web application instance
flask_app = Flask(__name__)

# Detect whether the connection is in the development environment or production.  
# Production implies:
#   1) URL for the bot is at "vpython.azurewebsites.com"
#   2) the 'createdBy' attribute in the inbound JSON is: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MzljNmIwMC04NzBiLTRiZTMtOTM4ZC1jOTM3YzAwMDdjMjI
# Development implies:
#   1) URL for the bot is at "*.ngrok.io"
#   2) the 'createdBy' attribute in the inbound JSON is: Y2lzY29zcGFyazovL3VzL1BFT1BMRS81Y2JlMjc1Zi1kODAyLTQ5NTMtYWFhOC0wZjYwYmEzNzQ4MTY

# Create the Webex Teams API connection object
#botToken = 'NTdjNjgxODktMDdjYS00ODgwLTg4NjgtNWNhZDRkMDIwYTRhZWI4OTY3MDMtNzgy_PF84_9b4b0d2c-c77b-40fa-9a49-338196f70056'
botToken = os.environ.get('VP_BOT_TOKEN')
api = WebexTeamsAPI(botToken)
devices = DeviceAPI(botToken)

# time-related variables
CT = pytz.timezone('US/Central')
Zulu = pytz.timezone('UTC')
localTZ = CT

# webhook-related variables
MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"


# Core bot functionality
# Your Webex Teams webhook should point to http://<serverip>:5000/events
@flask_app.route('/events', methods=['GET', 'POST'])
def webex_teams_webhook_events():
    """Processes incoming requests to the '/events' URI."""
    if request.method == 'GET':
        return ("""<!DOCTYPE html>
                   <html lang="en">
                       <head>
                           <meta charset="UTF-8">
                           <title>Webex Teams Bot served via Flask</title>
                       </head>
                   <body>
                   <p>
                   <strong>Your Flask web server is up and running!</strong>
                   </p>
                   <p>
                   Here is a nice Cat Fact for you:
                   </p>
                   <blockquote>{}</blockquote>
                   </body>
                   </html>
                """.format(get_catfact()))
    elif request.method == 'POST':
        """Respond to inbound webhook JSON HTTP POST from Webex Teams."""
        # Get the POST data sent from Webex Teams
        json_data = request.json
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")

        # Create a Webhook object from the JSON data
        webhook_obj = Webhook(json_data)
        # Get the room details
#        room = api.rooms.get(webhook_obj.data.roomId)
        # Get the message details
#        message = api.messages.get(webhook_obj.data.id)
        # Get the sender's details
#        person = api.people.get(message.personId)

        # Handle a new message event
        if (webhook_obj.resource == MESSAGE_WEBHOOK_RESOURCE
                and webhook_obj.event == MESSAGE_WEBHOOK_EVENT):
            respond_to_message(webhook_obj)

        # Handle an Action.Submit button press event
        elif (webhook_obj.resource == CARDS_WEBHOOK_RESOURCE
              and webhook_obj.event == CARDS_WEBHOOK_EVENT):
            respond_to_button_press(webhook_obj)

        # Ignore anything else (which should never happen
        else:
            print(f"IGNORING UNEXPECTED WEBHOOK:\n{webhook_obj}")

        return "OK"


# Helper functions
def get_catfact():
    """Get a cat fact from catfact.ninja and return it as a string.
    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.
    """
    response = requests.get(CAT_FACTS_URL, verify=False)
    response.raise_for_status()
    json_data = response.json()
    return json_data['fact']


def respond_to_message(webhook):
    # Get the room details
    room = api.rooms.get(webhook.data.roomId)
    # Get the message details
    message = api.messages.get(webhook.data.id)
    # split the message list into two pieces, separated by whitespace. The first item is the command and the rest
    # are any arguments for the command
    message_list = message.text.split(" ", 1)
    # Get the sender's details
    person = api.people.get(message.personId)

    print("NEW MESSAGE IN ROOM '{}'".format(room.title))
    print("FROM '{}'".format(person.displayName))
    print("MESSAGE '{}'\n".format(message.text))

    # This is a VERY IMPORTANT loop prevention control step.
    # If you respond to all messages...  You will respond to the messages
    # that the bot posts and thereby create a loop condition.
    me = api.people.me()
    if message.personId == me.id:
        # Message was sent by me (bot); do not respond.
        return 'OK'
    else:
        if "/CAT" in message_list[0]:
            print("FOUND '/CAT'")
            # Get a cat fact
            cat_fact = get_catfact()
            print("SENDING CAT FACT '{}'".format(cat_fact))
            # Post the fact to the room where the request was received
            api.messages.create(room.id, text=cat_fact)
        if "/b" in message_list[0]:
            print("FOUND '/bookings'")
            filter_str = ""
            if len(message_list) > 1:
                filter_str = message_list[1]
                print ("Filtering on: " + filter_str)
            get_bookings(room.id, filter_str)
        if "/stat" in message_list[0]:
            deviceid = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL0RFVklDRS82ZDE3MDA4Mi1lODI0LTQyMGQtYmRiNS1kODk2OGUzNmI5NWI='
            statii = devices.getCallStatus(deviceid)
            print("statii:")
            print(json.dumps(statii, indent=4))
#           api.messages.create(room.id, text=statii)
#         if "/demo" in message_list[0]:
#             msg_result = api.messages.create(
#                 room.id,
#                 text="If you see this your client cannot render cards\n",
#                 attachments=[{
#                     "contentType": "application/vnd.microsoft.card.adaptive",
#                     "content": VPBotCards.CiscoDefaultCard
#                 }],
#             )
#             print("message result:")
#             print(msg_result)
    return ()


def respond_to_button_press(webhook):
    print("FOUND: Button Press")
    # Get the room details
    room = api.rooms.get(webhook.data.roomId)
    attachment_action = api.attachment_actions.get(webhook.data.id)
    person = api.people.get(attachment_action.personId)
    message_id = attachment_action.messageId
    # api.messages.create(
    #     room.id,
    #     parentId=message_id,
    #     markdown=f"This is the data sent from the button press.  A more "
    #              f"robust app would do something cool with this:\n"
    #              f"```\n{attachment_action.to_json(indent=2)}\n```"
    # )
    print("button action: ", attachment_action.to_json())
    if attachment_action.inputs["buttonaction"] == "dial":
        # If the "mutebeforedial" var is set to "true" mute the video system before calling
        if attachment_action.inputs["mutebeforedial"] == "true":
            deviceid = attachment_action.inputs["deviceToDial"]
            devices.setMuteOn(deviceid)
        # Now dial the call
        dial_result = dial_calls(attachment_action.to_json())
        print("dial_result: {}".format(json.dumps(dial_result, indent=4)))
        # allow some time to pass before checking the status of the call
        sleep(5)
        show_connection_status(dial_result, room.id, message_id)
        return

    elif attachment_action.inputs["buttonaction"] == "showcallstatus":
        # A display of a device call status has been requested.
        # The first argument to "show_connection_status" is a dict with the required fields of a call_result:
        # {"deviceId": deviceId, "message": message, "parentmsgid": parent_msgid}
        try:
            parent_msgid = attachment_action.inputs["parentmsgid"]
        except:
            parent_msgid = message_id
        show_connection_status({"deviceId": attachment_action.inputs["deviceId"], "message": "Showing Call Status"},
                               room.id, parent_msgid)
        return

    # elif attachment_action.inputs["buttonaction"] == "refreshself":
    #     # A refresh of a device call status has been requested.
    #     # The first argument to "show_connection_status" is a dict with the required fields of a call_result:
    #     # {"deviceId": deviceId, "message": message}  In this case the "message" is not used
    #     parent_msgid = attachment_action.inputs["parentmsgid"]
    #     show_connection_status({"deviceId": attachment_action.inputs["deviceId"], "message": "Refreshing"},
    #                            room.id, parent_msgid)
    #     return

    elif attachment_action.inputs["buttonaction"] == "setmute":
        # mute the microphones of the device
        # parent_msgid = attachment_action.inputs["parentmsgid"]
        deviceid = attachment_action.inputs["deviceId"]
        devices.setMuteOn(deviceid)
        return

    elif attachment_action.inputs["buttonaction"] == "setunmute":
        # unmute the microphones of the device
        # parent_msgid = attachment_action.inputs["parentmsgid"]
        deviceid = attachment_action.inputs["deviceId"]
        devices.setMuteOff(deviceid)
        return

    elif attachment_action.inputs["buttonaction"] == "hangup":
        # A hangup card is requested.
        # The first argument to "hangup_calls" is a dict with the required fields of a call_result:
        # {"deviceId": deviceId, "message": message}
        parent_msgid = attachment_action.inputs["parentmsgid"]
        show_hangup_call_card({"deviceId": attachment_action.inputs["deviceId"], "message": "Hangup card"},
                              room.id, parent_msgid)
        return

    elif attachment_action.inputs["buttonaction"] == "hangupACall":
        # Hang up a specific call on a device
        # The first argument to "hangup_calls" is a dict with the required fields of a call_result:
        # {"deviceId": deviceId, "message": message}
        parent_msgid = attachment_action.inputs["parentmsgid"]
        hangup_result = hangup_call(attachment_action.inputs["deviceId"], attachment_action.inputs["callidToHang"],
                                    room.id, parent_msgid)
        print("hangup result: ", hangup_result)
        return

    elif attachment_action.inputs["buttonaction"] == "callstats":
        # Display the call stats: jitter, bandwidth, etc.
        # The only parameter passed is the deviceId. This will display stats of all current calls on the device
        parent_msgid = attachment_action.inputs["parentmsgid"]
        show_call_stats(attachment_action.inputs["deviceId"], room.id, parent_msgid)
        return

    elif attachment_action.inputs["buttonaction"] == "deleteself":
        # When a call stats card is clicked anywhere, delete the card
        result = api.messages.delete(attachment_action.messageId)
        print("Delete card result:", result)
        return


def get_bookings(roomid, filter):
    # TODO: figure out how to limit the time frame of the bookings returned.
    bookings_text = ""
    # deviceList is type 'dict' with one keypair: "items" and then all the data stored in a list of dicts
    devices_dict = devices.getDevicesSubsetList(filter)
    # dlist is a list of dicts. One dict per device.
    dlist = devices_dict['items']
    for device in dlist:
        # device is a dict with a bunch of keypairs
        #        print(device['displayName'],device['id'])
        # do a POST to get the bookings list
        payload_json = json.dumps({'deviceId': device['id'], 'arguments': {'Days': 7}})
        sched = requests.post('https://webexapis.com/v1/xapi/command/bookings.list', headers=devices.getHeader(),
                              json=payload_json).json()
        try:
            # api.messages.create(roomid, text=device['displayName'])
            if sched['result']['ResultInfo']['TotalRows'] > 0:
                dialinfo = ""
                # print(device['displayName'])
                bookings_text += device['displayName']+'\n'
                for bookings in sched['result']['Booking']:
                    startdatetime_utc = Zulu.localize(datetime.strptime(bookings['Time']['StartTime'],
                                                                        '%Y-%m-%dT%H:%M:%SZ'))
                    startdatetime_local = startdatetime_utc.astimezone(localTZ)
                    startdate_local = startdatetime_local.strftime('%Y-%m-%d')
                    starttime_local = startdatetime_local.strftime('%H:%M')+" "+str(localTZ)

                    print("{}\n\t{}\n".format(bookings['Organizer']['Email'], startdatetime_local))
                    bookings_text += "{}\n\t{}\n".format(bookings['Organizer']['Email'], starttime_local)
                    dialinfo = bookings['DialInfo']['Calls']['Call']

                    send_booking_card(bookings, roomid, device['displayName'],
                                      bookings['Organizer']['Email'], dialinfo, device['id'])
        except Exception:
            print("ERROR: ", json.dumps(sched['message'], indent=4))
            bookings_text += "ERROR: Room {}:(id:{})\n{}\n".format(device['displayName'], device['id'],
                                                                   json.dumps(sched['message'], indent=4))
            api.messages.create(roomid, text="ERROR: Room {}: {}".format(device['displayName'],sched['message']))
            print("Response: ", bookings_text)
    return()


def dial_calls(callinfo_json):
    # do a POST to get the bookings list
    # print ("Callinfo:")
    callinfo = json.loads(callinfo_json)

    # Had to use the 'capitalize()' function on the protocol string because the bookings listing returns "SIP" but
    # the API requires capitalization of first letter.  Specifically, "H320, H323, Sip, Spark".  This inconsistency
    # is, perhaps, understandable, but it's also terribly jaw-dropping.
    payload_json = json.dumps({'deviceId': callinfo['inputs']['deviceToDial'],
                               'arguments': {'Number': callinfo['inputs']['numberToDial'],
                               'Protocol': callinfo['inputs']['protocol'].capitalize()}})

    # print ('payload_json: '+payload_json)
    dial_status = requests.post('https://webexapis.com/v1/xapi/command/dial', headers=devices.getHeader(), json=payload_json).json()
    return dial_status


def hangup_call(device_id, callid, roomid, parent_msgid):
    payload_json = json.dumps({'deviceId': device_id, 'arguments': {'CallId': int(callid)}})
    hangup_status = requests.post('https://webexapis.com/v1/xapi/command/call.disconnect', headers=devices.getHeader(),
                                  json=payload_json).json()
    return(hangup_status)


def show_connection_status(dial_result, teamsroomid, parent_msgid):
    # parent_msgid is the "parent" message ID - namely the bookings card from which the "dial" button was pressed
    # all responses to the teams room should have this message id as their parent
    try:
        # first, just see if we can access the deviceId. An error condition would mean that "dial_result" has a
        # dict with "message" and "error" keys, but not "deviceId".  So throw an error if deviceId doesn't exist
        deviceid = dial_result['deviceId']
        # retrieve the call status using the info returned in 'dial_result'
        call_status = devices.getCallStatus(dial_result['deviceId'])
        # display the basic dial results in a card
        device_name = devices.getDeviceName(deviceid)
        call_status_card = VPBotCards.build_call_status_card(device_name, deviceid, call_status, parent_msgid)
    except Exception:
        # TODO: add code to check the system for number of active calls.  If it is zero, just make this message say
        #   something like, "No calls, dude"  otherwise, show the error message.
        call_status_card = {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "ERROR: {}".format(dial_result['message']),
                    "color": "Attention",
                    "weight": "Bolder",
                    "wrap": True,
                    "size": "Default"
                }
            ],
            "selectAction": {
                "type": "Action.Submit",
                "title": "Remove",
                "data": {
                    "buttonaction": "deleteself"
                }
            },
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.2"
        }
        print('ERROR')
        print(dial_result)
    # try:
    msg_result = api.messages.create(
        teamsroomid,
        text="If you see this your client cannot render cards\n",
        parentId=parent_msgid,
        attachments=[{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": call_status_card
        }]
    )
    print("call_status_card_msg result:")
    print(msg_result)
    return msg_result


def show_call_stats(deviceid, teamsroomid, parent_msgid):
    stats_result = devices.getCallStats(deviceid)
    stats_card = VPBotCards.build_stats_card(stats_result, devices.getDeviceName(deviceid), deviceid, parent_msgid)
    print('Stats card:', json.dumps(stats_card, indent=4))
    msg_result = api.messages.create(
        teamsroomid,
        text="If you see this your client cannot render cards\n",
        parentId=parent_msgid,
        attachments=[{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": stats_card
        }]
    )
    return


def send_booking_card(bookings, roomid, roomname, organizer, dialinfo, deviceID):
    organizeremail = organizer
    numbertodial = ""
    devicetodial = deviceID
    protocoltodial = ""

    startdatetime_utc = Zulu.localize(datetime.strptime(bookings['Time']['StartTime'],
                                                        '%Y-%m-%dT%H:%M:%SZ'))
    startdatetime_local = startdatetime_utc.astimezone(localTZ)
    confdate = startdatetime_local.strftime('%Y-%m-%d')
    conftime = startdatetime_local.strftime('%H:%M') + " " + str(localTZ)

    numbertodial = bookings['DialInfo']['Calls']['Call'][0]['Number']
    try:
        protocoltodial = bookings['DialInfo']['Calls']['Call'][0]['Protocol']
    except:
        protocoltodial = "Unknown"

    booking_card = VPBotCards.build_booking_card(roomname, devicetodial, organizeremail, confdate, conftime, numbertodial, protocoltodial)
    try:
        card_result = api.messages.create(
            roomid,
            text="If you see this your client cannot render cards\n",
            attachments=[{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": booking_card
            }]
        )
        print("card result")
        print(card_result)
    except:
        print("card creation error: ", json.dumps(booking_card, indent=4))


def show_hangup_call_card(calls, teamsroomid, parent_msgid):
    # parent_msgid is the "parent" message ID - namely the bookings card from which the "dial" button was pressed
    # all responses to the teams room should have this message id as their parent
    try:
        # first, just see if we can access the deviceId. An error condition would mean that "dial_result" has a
        # dict with "message" and "error" keys, but not "deviceId".  So throw an error if deviceId doesn't exist
        deviceid = calls['deviceId']
        # retrieve the call status using the info in 'calls'
        call_status = devices.getCallStatus(calls['deviceId'])
        # display the basic dial results in a card
        device_name = devices.getDeviceName(deviceid)
        hangup_card = VPBotCards.build_hangup_card(device_name, deviceid, call_status, parent_msgid)
    except Exception:
        hangup_card = {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "ERROR: {}".format(calls['message']),
                    "color": "Attention",
                    "weight": "Bolder",
                    "wrap": True,
                    "size": "Default"
                }
            ],
            "selectAction": {
                "type": "Action.Submit",
                "title": "Remove",
                "data": {
                    "buttonaction": "deleteself"
                }
            },
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.2"
        }
        print('ERROR')
    msg_result = api.messages.create(
        teamsroomid,
        text="If you see this your client cannot render cards\n",
        parentId=parent_msgid,
        attachments=[{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": hangup_card
        }],
    )
    print("hangup_card result:")
    print(msg_result)
    return msg_result


if __name__ == '__main__':
    # Start the Flask web server
    flask_app.run(host='0.0.0.0', port=5000, debug=True)