import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
import requests
import json
import sys
#from django.http import StreamingHttpResponse



#arguments = cgi.FieldStorage()
#These next lines work for an http GET
#for i in arguments.keys():
#    print (i, ' / ', arguments[i].value,)
#    print('<br>')

# This is for http POST
#print(cgi.print_form())



#def main_page(request):
    print("Content-Type: application/json")
    print("")
#    if request.method=='POST':
#        data = request.body.decode('utf-8')
#        received_json_data = json.loads(data)
#        return ('POST:'+str(received_json_data))


i