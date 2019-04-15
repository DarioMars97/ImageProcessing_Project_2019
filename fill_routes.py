import requests
import json

bus = 0 # 7ot rkm ll bus

zones = ["","",""] # 3behom w kaml 3lehom wlo zh2t mmkn t7ot 7aba w t run w trg3 tkml
                   # bs ely ht7to 8lt m4 hyt4al for now so please take care 

server = "https://image-processing-bus-services.herokuapp.com/"

for zone in zones:
    api = "bus_service/bus/"
    bus_str = str(bus)+"/"
    request = server+api+bus_str+"zones"
    response = requests.post(request,data={"zone_text":zone})
    json_data = json.loads(response.text)
    print(json_data)
