from flask import Flask,request,make_response
import os,json
import pyowm
import os

app = Flask(__name__)
owmapikey='180aefc3fc3f2e65cb6f727f23b64f0d' #or provide your key here
owm = pyowm.OWM(owmapikey)

#geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("result")
    print(result)
    parameters = result.get("parameters")
    print(parameters)
    city = parameters.get("geo-city")
    print(city)
    observation = owm.weather_at_place(city)
    print(observation)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    lat=str(latlon_res.get_lat())
    lon=str(latlon_res.get_lon())
     
    wind_res=w.get_wind()
    wind_speed=str(wind_res.get('speed'))
    
    humidity=str(w.get_humidity())
    
    celsius_result=w.get_temperature('celsius')
    temp_min_celsius=str(celsius_result.get('temp_min'))
    temp_max_celsius=str(celsius_result.get('temp_max'))
    
    fahrenheit_result=w.get_temperature('fahrenheit')
    temp_min_fahrenheit=str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit=str(fahrenheit_result.get('temp_max'))
    speech = "Today the weather in " + city + ": \n" + "Temperature in Celsius:\nMax temp :"+temp_max_celsius+".\nMin Temp :"+temp_min_celsius+".\nTemperature in Fahrenheit:\nMax temp :"+temp_max_fahrenheit+".\nMin Temp :"+temp_min_fahrenheit+".\nHumidity :"+humidity+".\nWind Speed :"+wind_speed+"\nLatitude :"+lat+".\n  Longitude :"+lon
    
    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather"
        }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
