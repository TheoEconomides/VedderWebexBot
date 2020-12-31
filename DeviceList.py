import requests
import urllib3
import pytz
import json
#import ujson
from datetime import datetime
from requests.utils import requote_uri
from webexteamsbot import TeamsBot
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Device API class

class DeviceAPI:
    def __init__(self, auth):
        self._authHeader = self.genHeader(auth)
        self._apiUrls = {'status': 'https://webexapis.com/v1/device/xapi/status',
                         'command': 'https://webexapis.com/v1/device/xapi/command',
                         'devices': 'https://webexapis.com/v1/devices'
                         }

    # Create authorization header
    def genHeader(self, auth):
        return {'Authorization': 'Bearer ' + auth, 'Content-type': 'application/json'}

    # Return the header
    def getHeader(self):
        return self._authHeader

    # Create device list
    def getDevicesList(self):
        url = self._apiUrls['devices']
        return self.get(url)

    def getDevicesSubsetList(self, filter):
        url = self._apiUrls['devices']
        return self.get("{}?displayName={}".format(url, filter))

    def showDevices(self):
        devices = self.getDevicesList()
        for i in devices['items']:
            print("{}:{}".format(i['id'], i['displayName']))

    def getDeviceName(self, deviceID):
        url = self._apiUrls['devices']+'/'+ requote_uri(deviceID)
        device_deets = self.get(url)
        return(device_deets['displayName'])

    # Returns the xStatus of a specific device
    def getStatus(self, deviceId, keyPath):
        url = self._apiUrls['status']
        return self.get("{}?name={}&deviceId={}".format(url, keyPath, deviceId))

    def getCallStatus(self, deviceId):
        # Gather all relevant call info to return as a dict
        # There should be, at most, two calls in a device, but usually just one or none
        call_status = self.getStatus(deviceId, requote_uri("Call[*].Status"))
        # print('Full call status:',call_status)
        # Iterate through the call(s) and assemble the response dict
        response = []
        for call in call_status['result']['Call']:
            callid = str(call['id'])
            callstatus = call['Status']
            callbacknumber = self.getStatus(deviceId,requote_uri("Call["+callid+"].CallbackNumber"))['result']['Call'][0]['CallbackNumber']
            calltype = self.getStatus(deviceId,requote_uri("Call["+callid+"].Calltype"))['result']['Call'][0]['CallType']
            callduration = self.getStatus(deviceId,requote_uri("Call["+callid+"].Duration"))['result']['Call'][0]['Duration']

            response.append({'id': callid, 'status': callstatus, 'callbacknumber': callbacknumber, 'type': calltype,
                             'duration': callduration})
        return(response)

    def getCallStats(self, deviceid):
        stats_result = self.getStatus(deviceid, requote_uri("MediaChannels.Call[*].channel[*].*"))
        for callnumber in stats_result['result']['MediaChannels']['Call']:
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
        return stats_result

    def sendCommand(self, keyPath, payload):
        url = self._apiUrls['command']
        print("{}/{} - {}".format(url, keyPath,payload))
        return self.post("{}/{}".format(url, keyPath), payload)

    def get(self, url):
        return requests.get(url, headers=self._authHeader, verify=False).json()

    def post(self, url, payload):
        return requests.post(url, headers=self._authHeader, data=payload, verify=False).json()


if __name__ == '__main__':
    bot_token = 'NTdjNjgxODktMDdjYS00ODgwLTg4NjgtNWNhZDRkMDIwYTRhZWI4OTY3MDMtNzgy_PF84_9b4b0d2c-c77b-40fa-9a49-338196f70056'
    CT = pytz.timezone('US/Central')
    Zulu = pytz.timezone('UTC')
    bot_email = 'vp-tsiraki@webex.bot'
    bot_url = "http://8199e06d0973.ngrok.io/FirstProject/DeviceList.py"
    bot_app_name = "Vedder Tsiraki"

    # Create a Bot Object
#    bot = TeamsBot(
#        bot_app_name,
#        teams_bot_token=bot_token,
#        teams_bot_url=bot_url,
#        teams_bot_email=bot_email,
#    )

    devices = DeviceAPI(bot_token)
    # deviceList is type 'dict' with one keypair: "items" and then all the data stored in a list of dicts
    devices_dict = devices.getDevicesList()
    # dlist is a list of dicts. One dict per device.
    dlist = devices_dict['items']

    for device in dlist:
        # device is a dict with a bunch of keypairs
        print(device['displayName'],device['id'])
        # do a POST to get the bookings list
        payload_json = json.dumps({'deviceId':device['id'],'arguments':{'Days':7}})
        sched=requests.post('https://webexapis.com/v1/xapi/command/bookings.list',headers=devices._authHeader, json=payload_json).json()

        try:
            if sched['result']['ResultInfo']['TotalRows'] > 0:
                print(device['displayName'])
                for bookings in sched['result']['Booking']:
                    starttime_utc=Zulu.localize(datetime.strptime(bookings['Time']['StartTime'],'%Y-%m-%dT%H:%M:%SZ'))
                    starttime_local=starttime_utc.astimezone(CT)
                    print ("{} {}\n\t{}".format(bookings['Id'],bookings['Organizer']['Email'], starttime_local))
                    for call in bookings['DialInfo']['Calls']['Call']:
                        print ("\t-->",call['Number'], bookings['DialInfo']['ConnectMode'])
 #                print (json.dumps(sched['result'],indent=4))
        except KeyError:
                print ("ERROR: ",json.dumps(sched,indent=4))

