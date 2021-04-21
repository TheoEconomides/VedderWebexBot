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
                                        # "id": "OrganizerLabel2",
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
                                        # "id": "DateLabel",
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
                                        # "id": "TimeLabel",
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
                                        # "id": "number",
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
                                        # "id": "protocolLabel",
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
                            },
                            {
                                "type": "Column",
                                "width": "200px",
                                "items": [
                                    {
                                        "type": "Input.Toggle",
                                        "id": "mutebeforedial",
                                        "title": "mute before dialing",
                                        "value": "true",
                                        "valueOn": "true",
                                        "valueOff": "false"
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
            },
            {
                "type": "Action.Submit",
                "title": "Mute",
                "data": {
                    "buttonaction": "setmute",
                    "deviceId": devicetodial
                }
            },
            {
                "type": "Action.Submit",
                "title": "Unmute",
                "data": {
                    "buttonaction": "setunmute",
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
                "buttonaction": "showcallstatus",
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


# Display call statistics
def build_stats_card(stats_json, devicename, device_id, parent_msgid):
    card_body = []
    stats_array = []
    body_call_header = {
            "type": "TextBlock",
            "text": "Call statistics for {}".format(devicename),
            "weight": "Bolder",
            "color": "Dark",
            "size": "Default"
        }
    card_body.append(body_call_header)
    for calljson in stats_json['result']['MediaChannels']['Call']:
        callid = calljson['id']
        # Create a row with the call ID, and column labels "Bit rate," "Jitter," "%loss"
        column_list = [
            {
                "type": "Column",
                "width": "150px",
                "style": "Default",
                "spacing": "None",
                "items": [{
                    "type": "TextBlock",
                    "text": "Call ID: " + str(callid),
                    "weight": "Bolder",
                    "color": "Dark",
                    "size": "Default"
                }]
            },
            {
                "type": "Column",
                "width": "80px",
                "style": "Default",
                "spacing": "None",
                "items": [{
                    "type": "TextBlock",
                    "text": "Bit rate",
                    "weight": "Bolder",
                    "color": "Dark",
                    "size": "Default"
                }]
            },
            {
                "type": "Column",
                "width": "50px",
                "style": "Default",
                "spacing": "None",
                "items": [{
                    "type": "TextBlock",
                    "text": "Jitter",
                    "weight": "Bolder",
                    "color": "Dark",
                    "size": "Default"
                }]
            },
            {
                "type": "Column",
                "width": "50px",
                "style": "Default",
                "spacing": "None",
                "items": [{
                    "type": "TextBlock",
                    "text":" % loss",
                    "weight": "Bolder",
                    "color": "Dark",
                    "size": "Default"
                }]
            }
        ]
        # Now enclose the columns list into a columnset object, then append to the card
        columnset_dict = {
            "type": "ColumnSet",
            "style": "Default",
            "spacing": "None",
            "columns": column_list
        }
        card_body.append(columnset_dict)

        # Gather the channel stats info into a dict using the channel id as the 'key'
        channelstatsarray = []
        channelidarray = []
        channelstatsdict = {}
        for channeljson in calljson['Channel']:
            channelid = channeljson['id']
            channeldir = channeljson['Direction']
            channeltype = channeljson['Type']
            channelnetloss = channeljson['Netstat']['Loss']
            channelnetrate = channeljson['Netstat']['ChannelRate']
            channelnetbytes = channeljson['Netstat']['Bytes']
            channelnetjitter = channeljson['Netstat']['Jitter']
            channelnetmaxjitter = channeljson['Netstat']['MaxJitter']
            channeldict = {
                "dir": channeldir,
                "type": channeltype,
                "netloss": channelnetloss,
                "netrate": channelnetrate,
                "netjitter": channelnetjitter,
                "netbytes": channelnetbytes,
                "netmaxjitter": channelnetmaxjitter
            }
            # channelstatsarray.append(channeldict)
            channelstatsdict[channelid] = channeldict
            channelidarray.append(channelid)

        channelidarray.sort()
        # print("channelstatsdict: {}".format(channelstatsdict))
        # print("channelIDarray: {}".format(channelidarray))

        # Get the details for this call channel and add a line of data to the card
        for channelid in channelidarray:
            channeldir = channelstatsdict[channelid]['dir']
            channeltype = channelstatsdict[channelid]['type']
            channelnetloss = channelstatsdict[channelid]['netloss']
            channelnetrate = channelstatsdict[channelid]['netrate']
            channelnetbytes = channelstatsdict[channelid]['netbytes']
            channelnetjitter = channelstatsdict[channelid]['netjitter']
            channelnetmaxjitter = channelstatsdict[channelid]['netmaxjitter']
            print("callid: {}, dir: {}, type: {}, rate: {}, loss: {}, jitter: {}".
                  format(callid, channeldir, channeltype, channelnetrate, channelnetloss, channelnetjitter))

            # Now add one set of columns, four wide and one deep
            column_list = [
                {
                    "type": "Column",
                    "width": "150px",
                    "style": "Default",
                    "spacing": "None",
                    "items": [{
                        "type": "TextBlock",
                        "text": "{}: {}".format(channeltype, channeldir),
                        "weight": "Regular",
                        "color": "Dark",
                        "size": "Default"
                    }]
                },
                {
                    "type": "Column",
                    "width": "80px",
                    "style": "Default",
                    "spacing": "None",
                    "items": [{
                        "type": "TextBlock",
                        "text": "{} k".format(str(channelnetrate/1000)),
                        "weight": "Bolder",
                        "color": "Dark",
                        "size": "Default"
                    }]
                },
                {
                    "type": "Column",
                    "width": "50px",
                    "style": "Default",
                    "spacing": "None",
                    "items": [{
                        "type": "TextBlock",
                        "text": str(channelnetloss),
                        "weight": "Bolder",
                        "color": "Dark",
                        "size": "Default"
                    }]
                },
                {
                    "type": "Column",
                    "width": "50px",
                    "style": "Default",
                    "spacing": "None",
                    "items": [{
                        "type": "TextBlock",
                        "text": str(channelnetjitter),
                        "weight": "Bolder",
                        "color": "Dark",
                        "size": "Default"
                    }]
                }
            ]

            # Now enclose the columns list into a columnset object, then append to the card
            columnset_dict = {
                "type": "ColumnSet",
                "style": "Default",
                "spacing": "None",
                "columns": column_list
            }
            card_body.append(columnset_dict)

    # Finally, put the card_body into a container and set the style to "Emphasis" to make it more
    # visible.
    # Set the "selectAction" to "deleteself" so that a click in the colored/emphasis container area will
    # cause the card to be deleted.
    card_container = [
        {
            "type": "Container",
            "style": "Default",
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

    card_code = {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2",
        "body": card_container,
        "actions": [{
            "type": "Action.Submit",
            "title": "Refresh",
            "data": {
                "buttonaction": "callstats",
                "parentmsgid": parent_msgid,
                "deviceId": device_id
            }
        },
             {
            "type": "Action.Submit",
            "title": "Call Status",
            "data": {
                "buttonaction": "showcallstatus",
                "parentmsgid": parent_msgid,
                "deviceId": device_id
            }
        }
    ]
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

def build_reboot_card(roomid, dlist):
    return()