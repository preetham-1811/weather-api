import json
from flask import Flask,render_template,request
import requests
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
app = Flask(__name__)


#Get HomePage
@app.route('/')
def man():
    return render_template('home.html')



#POST ResultPage
@app.route('/getCurrentWeather', methods=['POST'])

def home():

    city = request.args.get('city')
    output_format = request.args.get('output_format')

    city = request.form['city']
    output_format = request.form['output_format']


    #API
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring = {"q": city}

    headers = {
        "X-RapidAPI-Key": "31371bc5c3msh34f399b07961d46p192883jsn2ba7562e3194",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())

    respjson = json.dumps(response.json())

    #extract weather, location
    respdata = json.loads(respjson)
    locvalue = respdata.get("location")
    wvalue = respdata.get("current")

    #extract name, country, latitute, longitute, temp
    locjson = json.dumps(locvalue)
    wjson = json.dumps(wvalue)
    l_data = json.loads(locjson)
    w_data = json.loads(wjson)
    l_valueName = l_data.get("name")
    l_valueCountry = l_data.get("country")
    l_valueLat = l_data.get("lat")
    l_valueLong = l_data.get("lon")
    w_temp = w_data.get("temp_c")


    ResultJsonData = {
    "Weather": str(w_temp)+ " " + "C",
    "Latitute": l_valueLat,
    "Longitute": l_valueLong,
    "City": l_valueName + " " + l_valueCountry
    }

    ResultXMLData = {
        "Temperature": w_temp,
        "City": l_valueName,
        "Latitute": l_valueLat,
        "Longitute": l_valueLong,
    }


    if(output_format == "json"):
        Resultjson = json.dumps(ResultJsonData)
        return render_template('result.html', data= Resultjson)
    else:
        ResultX = dicttoxml(ResultXMLData)
        XMLData = parseString(ResultX) 
        Resultxml = XMLData.toprettyxml()
        return render_template('result.html', data= Resultxml)
    

if __name__ == "__main__":
    app.run(debug=True)