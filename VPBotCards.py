#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "Theo Economides"
__author_email__ = "teconomides@vedderprice.com"
__copyright__ = "Copyright (c) 2020 Vedder Price PC"

import json

def build_booking_card(roomname, devicetodial, organizeremail, confdate, conftime, numbertodial, protocoltodial):
    card_code = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "Container",
                "style": "Emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": roomname,
                        "id": "RoomName",
                        "weight": "Bolder",
                        "size": "Default",
                        "color": "Accent"
                    },
                    # TODO: once the API includes the meeting name parameter, it should be added to the parameters passed
                    #   into this function and displayed with this next snippet of code
                    # {
                    #     "type": "TextBlock",
                    #     "text": "meetingname",
                    #     "id": "MeetingName",
                    #     "wrap": True,
                    #     "color": "Accent"
                    # },
                    # TODO: put a container around all elements above the number "dial" button and then add the "deleteself"
                    #   feature to the container.
                    # TODO: generally make the card look prettier with some color amd emphases
                    {
                        "type": "ColumnSet",
                        "horizontalAlignment": "Left",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "95px",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "Organizer:",
                                        "id": "OrganizerLabel2",
                                        "horizontalAlignment": "Left",
                                        "weight": "Bolder",
                                        "size": "Default"
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": 75,
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": organizeremail,
                                        "id": "Organizer2"
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        "type": "ColumnSet",
                        "horizontalAlignment": "Left",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "75px",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "Date:",
                                        "id": "DateLabel",
                                        "size": "Default",
                                        "weight": "Bolder"
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": "100px",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": confdate,
                                        "id": "date"
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": "70px",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "Start Time:",
                                        "id": "TimeLabel",
                                        "size": "Default",
                                        "weight": "Bolder"
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": conftime
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "ColumnSet",
                        "horizontalAlignment": "Left",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "75px",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "Number:",
                                        "id": "number",
                                        "horizontalAlignment": "Left",
                                        "weight": "Bolder",
                                        "size": "Default"
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": 80,
                                "items": [
                                    {
                                        "type": "Input.Text",
                                        "value": numbertodial,
                                        "id": "numberToDial",
                                        "isMultiline": False,
                                        "inlineAction": {
                                            "type": "Action.Submit",
                                            "title": "Dial",
                                            "data": {
                                                "buttonaction": "dial",
                                                "deviceToDial": devicetodial
                                            }
                                        }
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        "type": "ColumnSet",
                        "horizontalAlignment": "Left",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "60px",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "Protocol:",
                                        "id": "protocolLabel",
                                        "horizontalAlignment": "Left",
                                        "weight": "Bolder",
                                        "size": "Default"
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": "120px",
                                "items": [
                                    {
                                        "type": "Input.ChoiceSet",
                                        "value": protocoltodial,
                                        "id": "protocol",
                                        "style": "Compact",
                                        "choices": [
                                            {
                                                "title": "SIP",
                                                "value": "SIP"
                                            },
                                            {
                                                "title": "Spark",
                                                "value": "Spark"
                                            },
                                            {
                                                "title": "H320",
                                                "value": "H320"
                                            },
                                            {
                                                "title": "H323",
                                                "value": "H323"
                                            },
                                            {
                                                "title": "Unknown",
                                                "value": "Unknown"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Call Status",
                "data": {
                    "buttonaction": "showcallstatus",
                    "deviceId": devicetodial
                }
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }
    return(card_code)


def build_call_status_card(device_name, device_id, call_statuses, parent_msgid):
    # call_statuses is a list of dicts which looks like:
    # [{'id': callid, 'status': callstatus, 'callbacknumber': callbacknumber, 'type': calltype,'duration': callduration}]
    # and may have up to two dicts (one for each possible call on the codec)

    # start building the "body" part of the card_code
    # This puts the name of the system at the top of the card
    card_body = [
        {
            "type": "TextBlock",
            "text": str(device_name),
            "weight": "Bolder",
            "color": "Dark",
            "id": "roomname",
            "size": "Default"
        }
    ]
    # Next, iterate through the 1 or 2 call entries and append their info as:
    # One line with the callbacknumber followed by one line with three columns of
    # 'type' 'status' and 'callduration'
    for call in call_statuses:
        callbacknumber_item = {
            "type": "TextBlock",
            "text": str(call['callbacknumber']),
            "weight": "Bolder",
            "color": "Dark",
            "id": "callbacknumber{}".format(call['id']),
            "size": "Default"
        }
        card_body.append(callbacknumber_item)
        # convert the duration from sec to min and append the text " min"
        call_duration = "{0:.1f} min".format(call['duration']/60)
        # Now build the "columnset" body which is a list, three columns wide
        column_list = [
            {
                "type": "Column",
                "width": "80px",
                "items": [
                    {
                        "type": "Container",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": str(call['status']),
                                "weight": "Bolder",
                                "color": "Dark",
                                "id": "status{}".format(call['id']),
                                "size": "Default"
                            }
                        ],
                        "selectAction": {
                            "type": "Action.Submit",
                            "data": {
                                "buttonaction": "hangup",
                                "callid": call['id'],
                                "deviceId": device_id
                            }
                        }
                    }
                ]
            },
            {
                "type": "Column",
                "width": "50px",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": str(call['type']),
                        "id": "type{}".format(call['id']),
                        "weight": "Bolder",
                        "size": "Default",
                        "color": "Dark"
                    }
                ]
            },
            {
                "type": "Column",
                "width": "95px",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": call_duration,
                        "id": "duration{}".format(call['id']),
                        "weight": "Bolder",
                        "size": "Default",
                        "color": "Dark"
                    }
                ]
            }
        ]
        # Now enclose the three column list into a columnset object, then append to the card
        columnset_dict = {
            "type": "ColumnSet",
            "style": "Default",
            "spacing": "none",
            "columns": column_list
        }
        card_body.append(columnset_dict)

    # Finally, put the card_body into a container and set the style to "Emphasis" to make it more
    # visible.
    # Set the "selectAction" to "deleteself" so that a click in the colored/emphasis container area will
    # cause the card to be deleted.  Multiple status cards aren't needed, so this makes it easy to remove
    # the ones the user doesn't want any longer.
    card_container = [
        {
            "type": "Container",
            "style": "Emphasis",
            "items": card_body,
            "selectAction": {
                "type": "Action.Submit",
                "title": "Remove",
                "data": {
                    "buttonaction": "deleteself"
                }
            }
        }
    ]

    # Add button for refresh
    card_actions = [
        {
            "type": "Action.Submit",
            "title": "Refresh",
            "data": {
                "buttonaction": "refreshself",
                "parentmsgid": parent_msgid,
                "deviceId": device_id
            }
        },
        {
            "type": "Action.Submit",
            "title": "Call Stats",
            "data": {
                "buttonaction": "callstats",
                "parentmsgid": parent_msgid,
                "deviceId": device_id
            }
        },
        {
            "type": "Action.Submit",
            "title": "Hang up...",
            "style": "Destructive",
            "data": {
                "buttonaction": "hangup",
                "parentmsgid": parent_msgid,
                "deviceId": device_id
            }
        }
    ]

    card_code = {
        "type": "AdaptiveCard",
        "body": card_container,
        "actions": card_actions,
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }

    print('card code: ', json.dumps(card_code, indent=4))
    return card_code


def build_stats_card(stats_json):
    card_actions = []
    for callnumber in stats_json['result']['MediaChannels']['Call']:
        callid = callnumber['id']
        for channelnumber in callnumber['Channel']:
            channelid = channelnumber['id']
            channeldir = channelnumber['Direction']
            channeltype = channelnumber['Type']
            channelnetloss = channelnumber['Netstat']['Loss']
            channelnetrate = channelnumber['Netstat']['ChannelRate']
            channelnetbytes = channelnumber['Netstat']['Bytes']
            channelnetjitter = channelnumber['Netstat']['Jitter']
            channelnetmaxjitter = channelnumber['Netstat']['MaxJitter']
            print("callid: {}, dir: {}, type: {}, rate: {}, loss: {}, jitter: {}".
                  format(callid, channeldir, channeltype, channelnetrate, channelnetloss, channelnetjitter))
    card_code = {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }
    return card_code


def build_hangup_card(device_name, device_id, call_statuses, parent_msgid):
    card_actions = []
    # start building the "body" part of the card_code
    # This puts the name of the system at the top of the card
    card_body = [
        {
            "type": "TextBlock",
            "text": str(device_name),
            "weight": "Bolder",
            "color": "Dark",
            "id": "roomname",
            "size": "Default"
        }
    ]
    # Next, iterate through the 1 or 2 call entries and append their info as:
    # One line with the callbacknumber followed by one line with three columns of
    # 'type' 'status' and 'callduration'
    for call in call_statuses:
        callbacknumber_item = {
            "type": "TextBlock",
            "text": str(call['callbacknumber']),
            "weight": "Bolder",
            "color": "Dark",
            "id": "callbacknumber{}".format(call['id']),
            "size": "Default"
        }
        card_body.append(callbacknumber_item)
        # convert the duration from sec to min and append the text " min"
        call_duration = "{0:.1f} min".format(call['duration']/60)
        # Now build the "columnset" body which is a list, three columns wide
        column_list = [
            {
                "type": "Column",
                "width": "80px",
                "spacing": "None",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "Call ID: {}".format(str(call['id'])),
                        "weight": "Bolder",
                        "color": "Good",
                        "id": "callid{}".format(call['id']),
                        "spacing": "None",
                        "size": "Default"
                    }
                ]
            },
            {
                "type": "Column",
                "width": "80px",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": str(call['status']),
                        "weight": "Bolder",
                        "color": "Dark",
                        "id": "status{}".format(call['id']),
                        "spacing": "None",
                        "size": "Default"
                    }
                ]
            },
            {
                "type": "Column",
                "width": "50px",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": str(call['type']),
                        "id": "type{}".format(call['id']),
                        "weight": "Bolder",
                        "size": "Default",
                        "spacing": "None",
                        "color": "Dark"
                    }
                ]
            },
            {
                "type": "Column",
                "width": "95px",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": call_duration,
                        "id": "duration{}".format(call['id']),
                        "weight": "Bolder",
                        "size": "Default",
                        "spacing": "None",
                        "color": "Dark"
                    }
                ]
            }
        ]
        # Now enclose the three column list into a columnset object, then append to the card
        columnset = {
            "type": "ColumnSet",
            "style": "Default",
            "spacing": "none",
            "columns": column_list
        }
        card_body.append(columnset)

        # Create the hangup buttons as Action.Submit buttons for the card
        hup_action = {
            "type": "Action.Submit",
            "title": "HANG UP CALL ID {}".format(call['id']),
            "style": "Destructive",
            "data": {
                "buttonaction": "hangupACall",
                "callidToHang": call['id'],
                "parentmsgid": parent_msgid,
                "deviceId": device_id
            }

        }
        card_actions.append(hup_action)

    # Finally, put the card_body into a container and set the style to "warning" for emphasis
    card_container = [
        {
            "type": "Container",
            "style": "Warning",
            "selectAction": {
                "type": "Action.Submit",
                "title": "Remove",
                "data": {
                    "buttonaction": "deleteself"
                }
            },
            "items": card_body
        }
    ]

    card_code = {
        "type": "AdaptiveCard",
        "body": card_container,
        "actions": card_actions,
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }
    return(card_code)