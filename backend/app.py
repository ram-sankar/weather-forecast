from flask import Flask
from flask import request
import requests, json ,random
import sqlite3
from datetime import datetime
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)


#127.0.0.1/auth/login?username=111&password=111
@app.route('/auth/signup',methods=['GET','POST'])
def signup():
	try:
		jsonfile=request.data
		js=jsonfile.decode("utf-8")
		jsonval=json.loads(js)
		email=jsonval["email"]
		password=jsonval["password"]
		username=jsonval["username"]
		phoneno=jsonval["phoneno"]
		conn = sqlite3.connect('auth.db')
		conn.execute("create table if not exists auth(username varchar(100),password varchar(100), phoneno varchar(100), email varchar(100))")
		conn.execute("insert into auth values('"+username+"','"+password+"','"+phoneno+"','"+email+"')")
		conn.commit()
		conn.close()
		tempvar='{"status":"SUCCESS"}'
		return json.loads(tempvar)
	except:
		tempvar='{"status":"FAIL"}'
		return json.loads(tempvar)
	

@app.route('/auth/login',methods=['GET','POST'])
def authenticate():
	jsonfile=request.data
	js=jsonfile.decode("utf-8")
	jsonval=json.loads(js)
	email=jsonval["email"]
	password=jsonval["password"]
	conn = sqlite3.connect('auth.db')
	val=conn.execute("select count (*) from auth where email='"+email+"' and password='"+password+"'")
	for row in val:
		ans=str(row[0])
	conn.close();
	if(ans=="1"):
		tempvar='{"status":"SUCCESS"}'
		return json.loads(tempvar)
	else:
		tempvar='{"status":"FAIL"}'
		return json.loads(tempvar)

@app.route('/crop',methods=['GET','POST'])
def crop():
	try:
		jsonfile=request.data
		js=jsonfile.decode("utf-8")
		jsonval=json.loads(js)
		city=jsonval["city"]
		ans='{"list":['
		conn=sqlite3.connect('crop.db')
		val=conn.execute("select * from place where place='"+city+"'")
		for row in val:
			cropslist=row[1].split(',')
			for icrop in cropslist:
				valcrop=conn.execute("select * from crop where name='"+icrop+"'")
				for rowcrop in valcrop:
					ans=ans+'{"name":"'+rowcrop[0]+'","weather":"'+rowcrop[1]+'","description":"'+rowcrop[2]+'"},'
		ans=ans[:-1]+']}'
		return json.loads(ans,strict=False)
	except:
		ans='{"status":"fail"}'
		return json.loads(ans)
#http://api.openweathermap.org/data/2.5/forecast?q=chennai&APPID=119c0a67018275a7fd42646e414a97bc&cnt=7
#base_url = "http://api.openweathermap.org/data/2.5/weather?"
#city_name = input("Enter city name : ")
#complete_url = base_url + "appid=" + api_key + "&q=" + city_name
@app.route('/',methods=['GET','POST'])
def home():
	jsonfile=request.data
	js=jsonfile.decode("utf-8")
	jsonval=json.loads(js)
	city=jsonval["city"]
	api_key = "119c0a67018275a7fd42646e414a97bc"
	complete_url = 'http://api.openweathermap.org/data/2.5/forecast?q='+city+'&APPID=119c0a67018275a7fd42646e414a97bc&cnt=6'
	response = requests.get(complete_url)
	x = response.json()
	pos=0
	ans='{'
	if x["cod"] != "404": 
		y = x["list"]
		for subs in y:
			if(pos==0):
				sub=subs["main"]
				current_temperature = sub["temp"] 
				min_temp = sub["temp_min"]
				max_temp = sub["temp_max"] 
				humidity = sub["humidity"]
				AirPol = random.randrange(50,100) 
				pressure = sub["pressure"]
				subwind = subs["wind"]
				speed = subwind["speed"]
				z = subs["weather"] 
				weather_main = z[0]["main"]
				weather_description = z[0]["description"]
				date=subs["dt_txt"]
				ans=ans+'"city":"'+city+'","api":"'+str(AirPol)+'","temp":"'+str(current_temperature)+'","min_temp":"'+str(min_temp)+'","max_temp":"'+str(max_temp)+'","humidity":"'+str(humidity)+'","pressure":"'+str(pressure)+'","speed":"'+str(speed)+'","weather_main":"'+str(weather_main)+'","description":"'+str(weather_description)+'","date":"'+str(date)+'","next":['
			else:
				sub=subs["main"]
				current_temperature=sub["temp"]
				z = subs["weather"] 
				weather_main = z[0]["main"]
				date=subs["dt_txt"].split(" ")
				actDate=date[0]
				time=date[1][:-3]
				time = datetime.strptime(time, "%H:%M")
				time = time.strftime("%I %p")
				Celsius = (current_temperature - 273)
				Celsius=int(Celsius)
				ans=ans+'{"time":"'+str(time)+'","temp":"'+str(Celsius)+'","description":"'+str(weather_main)+'"},'
			pos=pos+1
		ans=ans[:-1]+"]}"
		return json.loads(ans)

	else: 
		tempvar='{"status":"FAIL"}'
		return json.loads(ans)

def getAPI():
	pass

scheduler=BackgroundScheduler()
scheduler.add_job(func=getAPI,trigger="interval",seconds=3)
scheduler.start()
atexit.register(lambda:scheduler.shutdown())



conn = sqlite3.connect('crop.db')
c=conn.cursor()
c.execute("select count(*) from sqlite_master where type='table' and name='crop'")
if c.fetchone()[0]!=1:
	conn.execute("create table if not exists crop(name varchar(100),weather varchar(20000), description varchar(20000))")
	crop="rice"

	weather="As per the district forecast issued by the IMO for Coimbatore district, sky will be mostly cloudy. Light rainfall is expected on next five days. Maximum temperature is to be around 31 to 32 C . Minimum temperature is to be around 22 *C to 23  C . Morning relative humidity is to be around 85 evening relative humidity is to be around 55 per cent Average wind speed is to be around 8 km per hour and the wind direction will be from East direction."
	description="Gal midge incidence in rice is being observed in some pockets hence farmers are requested to monitor the crop carefully and spray if require thiamethoxam @ 100 g ha or pihasalone 2m1/ litter of water."
	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")
	conn.commit()

	crop="cotton"

	weather="As per the district forecast issued by the IMO for Coimbatore district, sky will be mostly cloudy. Light rainfall is expected on next five days. Maximum temperature is to be around 31 to 32C . Minimum temperature is to be around 22 *C to 23C . Morning relative humidity is to be around 85 evening relative humidity is to be around 55 per cent Average wind speed is to be around 8 km per hour and the wind direction will be from East direction."

	description="Gal midge incidence in rice is being observed in some pockets hence farmers are requested to monitor the crop carefully and spray if require thiamethoxam @ 100 g ha or pihasalone 2m1/ litter of water."
	

	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")
	conn.commit()

	crop="banana"

	weather= "As per the district forecast issued by the IMD for Coimbatore district, sky will be mostly cloudy. Light rainfall is expected on next five days. Maximum temperature is to be around 31T to 32C . Minimum temperature is to be around 22 C to 23 C Morning relative humidity is to be around 85 evening relative humidity is to be around 55 per cent Average wind speed is to be around 8 km per hour and the wind direction will be from East direction."
	description="Garden land banana may be planted by utilizing the prevailing weather. A sucker must weigh 2 kg each and must be dipped in GA carbendazim solution before planting. Also again dip the sucker in clay water mixture and sprinkle 3 g of carbofuron per square feet."
	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")
	conn.commit()

	crop="coconut"

	weather="As per the district forecast issued by the INC for Coimbatore district, sky will be mostly cloudy. Light rainfall is expected on next five days. Maximum temperature is to be around 31 2C to 32*C . Minimum temperature is to be around 22C to 23 C. Morning relative humidity is to be around 8.5 evening relative humidity is to be around 55 per cent. Average wind speed is to be around 8 km per hour and the wind direction will he from East direction"

	description="This is best time for second does application of fertilizer to coconut at 650 g urea + 1kg super phosphate + 1 kg uriate of potash / tree."
	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")

	conn.commit()

	crop="sugarbeet"

	weather="As per the district forecast issued by the IMO for Coimbatore district, sky will be mostly cloudy. Light rainfall is expected on next five days. Maximum temperature is to be around 31 C to  32 C . Minimum temperature is to be around 22  C to 23 C . Morning relative humidity is to be around 8.5 evening relative humidity is to be around 55 per cent. Average wind speed is to be around 8 km per hour and the wind direction will be from East direction."

	description="Detrashing and double line propping must be done to the latest season crop."
	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")
	conn.commit()

	crop="brinjal"

	weather="mainly cloudy and no rainfall will occur."

	description="avoid touching of fruits with soil to prevent rotting. cleanliness to be maintained."

	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")
	conn.commit()

	crop="chilli"

	weather="mainly cloudy and no rainfall."

	description="for aphid ,hoppers,whileflies,apply imidaclorpid 17.8SL@1ml/5lit of water .For yellow mite apply 2.5ml/lt of water."

	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")
	conn.commit()

	crop="wheat"

	weather="Light rain likely at isolated places of Punjab during next 24 hours; VI/eater likely to be dry during subsequent 4 hours and light rain likely at isolated places thereafter. Shallow lo moderate fog likely at isolated places during next 48 hours in the state."

	description="It is optimum time to sow wheat varieties PBW 550r Unnat PB14 550. Farmers are advised to complete sowing of wheat varieties i.e. Iinnat P8W 34ar PBW 1 Zr, PEI 725, PEW 677, HD 3086) WH 1105, HD 2967, PBW 621 during the period. Prefer to use happy seeder for the sowing of wheat crop.Treat 40 Kg seed with Raxil easy/ onus 13 ml (dissolve in 400 ml of water) or Tebuseed or Seeded or Exzole @ 40 q or vitavax power @120 g or vilavax 80g.In termite infested fields, treat the seed with 1 g Cruiser 70 WS or 2 ml Neonix 20 FS or 4 ml Dursban/Ruban/Durmet 20 EC per kg seed and dry in shade. Seed treated with Neonix also controls smuts of wheat As dry weather is expected in coming 2.3 days, farmers can apply first irrigation to wheat crop sown during last week of October and start spraying of weEdicides."

	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")

	conn.commit()

	crop="mustard"

	weather="Light rain likely at isolated places of Punjab during next 24 hours; Weather likely to be dry during subsequent 48 hours and light rain likely at isolated places thereafter.Shallow to moderate fog likely at isolated places during next 48 hours in the state."

	description="Transplanting of gobhi sarson is more profitable during this period than direct sowing. Use 60 days old seedlings of gobhi sarson (G L-1) but for gobhi sarson hybrid hyola PAC 401 use 30-35 days old seedlings. To early sown rays, apply 45 kg urea per acre with first irrigation."

	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")

	conn.commit()

	crop="tomato"

	weather="Light rain likely at isolated places of Punjab during next 24 hours; Weather likely to be dry during subsequent 48 hours and light rain likely at isolated places thereafter.Shallow to moderate fog likely at isolated places during next 4S hours in the state."
	description="It is optimum time to sow root crops like radish, turnip and carrot. Use 2 kg seed for turnip and 4 kg seed for carrot and radish per acre. Before sowing, treat the seed with Captan or Thiram @ 3 g per kg of seed. It is the optimum time for transplanting of nursery of tomato, brinjal. Complete sowing of the nursery of onion during these days Complete sowing of peas and hand hoeing should be done to control weeds"

	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")

	conn.commit()

	crop="ginger"

	weather="Light rain likely at isolated places of Punjab during next 24 hours; Weather likely to be dry during subsequent 48 hours and light rain likely at isolated places thereafter.Shallow to moderate fog likely at isolated places during next 4S hours in the state."

	description="Stem borer -There is a chance of stem borer in ginger_ Spary 20 g of Beauveria per one litre of water to control stem borer"
	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")

	conn.commit()

	crop="pea"

	weather="Light rain likely at isolated places of Punjab during next 24 hours; Weather likely to be dry during subsequent 48 hours and light rain likely at isolated places thereafter.Shallow to moderate fog likely at isolated places during next 4S hours in the state."

	description="Sucking pests   - There is a chance of sucking pests in vegetables. Apply 2% emulsion once in a weak for the control."
	conn.execute("insert into crop values('"+crop+"','"+weather+"','"+description+"')")

	conn.commit()

c=conn.cursor()
c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='place'")
if c.fetchone()[0]!=1 :
	conn.execute("create table if not exists place(place varchar(100),crop varchar(500))")
	conn.execute("insert into place values('theni','rice,cotton,banana,coconut,sugarbeet')")
	conn.execute("insert into place values('tanjore','rice,cotton')")
	conn.execute("insert into place values('bengal','brinjal,chilli')")
	conn.execute("insert into place values('amritsar','wheat,mustard,tomato')")
	conn.execute("insert into place values('palakkad','ginger,rice')")
	conn.commit()


if __name__ == '__main__':
	app.run()
