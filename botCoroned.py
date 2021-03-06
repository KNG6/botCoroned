import requests, os, tweepy, datetime
from bs4 import BeautifulSoup
from time import sleep

#Just logs the script's processing.
def logs(content):
    Date=str(datetime.datetime.now().date())
    hour=str(datetime.datetime.now().time().hour)
    minute=str(datetime.datetime.now().time().minute)
    second=str(datetime.datetime.now().time().second)
    if len(hour)<2:
        hour="0"+hour
    if len(minute)<2:
        minute="0"+minute
    if len(second)<2:
        second="0"+second
    Time="["+hour+":"+minute+":"+second+"]"
    f=open("/home/me/botCoroned/logs/"+Date+".txt","a")#the absolute path is required idk why
    formatted=Time+" "+content
    f.write(formatted+"\n")
    f.close()
    #print(Time+" ["+Date+"] "+content)

#Token for account connexion (view the twitter API).
auth = tweepy.OAuthHandler("key", "key")
auth.set_access_token("token", "token")

logs("[*] Authentification de 'CoronaVirused'...")
api = tweepy.API(auth)

#Get the total for 1 region (exemple: Asia, Europe).
def getRegionTotal(region):
	cases=0
	deaths=0
	casesLast=0
	for country in world[region]:
		cases=cases+int(world[region][country][0])
		deaths=deaths+int(world[region][country][1])
		casesLast=casesLast+int(world[region][country][2])
	return cases,deaths,casesLast

#Return the total of case newcase & death.
def getWorldTotal():
	lst=["Asia","Europe","America","Other","Oceania","Africa"]
	result1=0
	result2=0
	result3=0
	for region in lst:
		o1,o2,o3=getRegionTotal(region)
		result1=result1+int(o1)
		result2=result2+int(o2)
		result3=result3+int(o3)
	return result1,result2,result3

#Get the letality just basic percentage.
def getLetality(num0,num1):
	letality=(int(num0)/int(num1))*100
	return letality

#Format correctly the numbers for being more readable.
def formatNum(num):
	num=str(num)
	currentNum=len(num)
	finish=False
	while finish!=True:
		if currentNum-3 > 0:
			currentNum=currentNum-3
			num=num.replace(num,num[:currentNum]+" "+num[currentNum:])
		else:
			finish=True
			return(num)

def generateRapport():
	frCases,frDeaths,frCasesNew=world["Europe"]["France"]
	beCases,beDeaths,beCasesNew=world["Europe"]["Belgium"]
	caCases,caDeaths,caCasesNew=world["America"]["Canada"]
	frLetality=getLetality(frDeaths,frCases)
	beLetality=float(getLetality(beDeaths,beCases))
	caLetality=float(getLetality(caDeaths,caCases))
	ueCases,ueDeaths,ueCasesNew=getRegionTotal("Europe")
	ueLetality=getLetality(ueDeaths,ueCases)
	worldCases,worldDeaths,worldCasesNew=getWorldTotal()
	worldLetality=getLetality(worldDeaths,worldCases)
	f = open("/home/kng/botCoroned/cache/last.rap","w")
	f.write(str(frCases)+";"+str(frDeaths)+";"+str(frCasesNew)+";"+str(frLetality)+";"+str(ueCases)+";"+str(ueDeaths)+";"+str(ueCasesNew)+";"+str(ueLetality)+";"+str(worldCases)+";"+str(worldDeaths)+";"+str(worldCasesNew)+";"+str(worldLetality)+";"+str(beCases)+";"+str(beDeaths)+";"+str(beCasesNew)+";"+str(beLetality)+";"+str(caCases)+";"+str(caDeaths)+";"+str(caCasesNew)+";"+str(caLetality))
	f.close()

#read the rapport of the previous execution.
def readRapport():
	f = open("/home/kng/botCoroned/cache/last.rap","r")
	rapport = f.read()
	rapport = rapport.split(";")
	return int(rapport[0]), int(rapport[1]), int(rapport[2]), float(rapport[3]), int(rapport[4]), int(rapport[5]), int(rapport[6]), float(rapport[7]), int(rapport[8]), int(rapport[9]), int(rapport[10]), float(rapport[11]), int(rapport[12]), int(rapport[13]), int(rapport[14]), float(rapport[15]), int(rapport[16]), int(rapport[17]), int(rapport[18]), float(rapport[19])

#Get the difference from yesterday's report.
def diffRapport():
	frCasesOld, frDeathsOld, frCasesNewOld, frLetalityOld, ueCasesOld, ueDeathsOld, ueCasesNewOld, ueLetalityOld, worldCasesOld, worldDeathsOld ,worldCasesNewOld, worldLetalityOld, beCasesOld, beDeathsOld, beCasesNewOld, beLetalityOld, caCasesOld, caDeathsOld, caCasesNewOld, caLetalityOld = readRapport()
	frCases,frDeaths,frCasesNew=world["Europe"]["France"]
	beCases,beDeaths,beCasesNew=world["Europe"]["Belgium"]
	caCases,caDeaths,caCasesNew=world["America"]["Canada"]
	frCases,frDeaths,frCasesNew=int(frCases),int(frDeaths),int(frCasesNew)
	beCases,beDeaths,beCasesNew=int(beCases),int(beDeaths),int(beCasesNew)
	caCases,caDeaths,caCasesNew=int(caCases),int(caDeaths),int(caCasesNew)
	frLetality=float(getLetality(frDeaths,frCases))
	beLetality=float(getLetality(beDeaths,beCases))
	caLetality=float(getLetality(caDeaths,caCases))
	ueCases,ueDeaths,ueCasesNew=getRegionTotal("Europe")
	ueLetality=float(getLetality(ueDeaths,ueCases))
	worldCases,worldDeaths,worldCasesNew=getWorldTotal()
	worldLetality=float(getLetality(worldDeaths,worldCases))
	return frCases-frCasesOld, frDeaths-frDeathsOld, frCasesNew-frCasesNewOld, frLetality-frLetalityOld, ueCases-ueCasesOld, ueDeaths-ueDeathsOld, ueCasesNew-ueCasesNewOld, ueLetality-ueLetalityOld, worldCases-worldCasesOld, worldDeaths-worldDeathsOld ,worldCasesNew-worldCasesNewOld, worldLetality-worldLetalityOld, beCases-beCasesOld, beDeaths-beDeathsOld, beCasesNew-beCasesNewOld, beLetality-beLetalityOld, caCases-caCasesOld, caDeaths-caDeathsOld, caCasesNew-caCasesNewOld, caLetality-caLetalityOld

#
def finalDiffRapport():
	Rapport = {}
	Rapport["frCasesDiff"], Rapport["frDeathsDiff"], Rapport["frCasesNewDiff"], Rapport["frLetalityDiff"], Rapport["ueCasesDiff"], Rapport["ueDeathsDiff"], Rapport["ueCasesNewDiff"], Rapport["ueLetalityDiff"], Rapport["worldCasesDiff"], Rapport["worldDeathsDiff"], Rapport["worldCasesNewDiff"], Rapport["worldLetalityDiff"], Rapport["beCasesDiff"], Rapport["beDeathsDiff"], Rapport["beCasesNewDiff"], Rapport["beLetalityDiff"], Rapport["caCasesDiff"], Rapport["caDeathsDiff"], Rapport["caCasesNewDiff"], Rapport["caLetalityDiff"] = diffRapport()

	for entry in Rapport:
		if Rapport[entry]>0:
			Rapport[entry]="+"+str(Rapport[entry])

	return Rapport["frCasesDiff"], Rapport["frDeathsDiff"], Rapport["frCasesNewDiff"], Rapport["frLetalityDiff"], Rapport["ueCasesDiff"], Rapport["ueDeathsDiff"], Rapport["ueCasesNewDiff"], Rapport["ueLetalityDiff"], Rapport["worldCasesDiff"], Rapport["worldDeathsDiff"], Rapport["worldCasesNewDiff"], Rapport["worldLetalityDiff"], Rapport["beCasesDiff"], Rapport["beDeathsDiff"], Rapport["beCasesNewDiff"], Rapport["beLetalityDiff"], Rapport["caCasesDiff"], Rapport["caDeathsDiff"], Rapport["caCasesNewDiff"], Rapport["caLetalityDiff"]

#Web scrapping part
logs("[*] Connexion au site...")
worldGet=requests.get("https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases")
worldSoup=BeautifulSoup(worldGet.content,"html.parser")
worldScrap=worldSoup.find_all("tr")
world={"Asia":{},"Europe":{},"America":{},"Other":{},"Oceania":{},"Africa":{},"Total":{}}
logs("[*] Ajoute des pays du monde dans la base de donnée...")
#Data organization part
oldRegionName="\xa0"
for region in worldScrap:
	listRegion=region.find_all("td")
	if listRegion!=[]:
		countryList=[]
		regionName=str(listRegion[0]).replace("<td>","").replace("</td>","").replace("<strong>","").replace("</strong>","")
		regionCountryName=str(listRegion[1]).replace("<td>","").replace("</td>","").replace("<strong>","").replace("</strong>","")
		regionCountryCases=str(listRegion[2]).replace("<td>","").replace("</td>","").replace("<strong>","").replace("</strong>","")
		regionCountryDeaths=str(listRegion[3]).replace("<td>","").replace("</td>","").replace("<strong>","").replace("</strong>","")
		regionCountryCasesLast=str(listRegion[4]).replace("<td>","").replace("</td>","").replace("<strong>","").replace("</strong>","")
		if str(regionName)=="\xa0":
			regionName=oldRegionName
			if str(oldRegionName)=="\xa0":
				regionName="Other"
		if str(regionCountryCasesLast)=="\xa0":
			regionCountryCasesLast=0
		if regionCountryCases=="\xa0":
			regionCountryCases=0
		if regionCountryDeaths=="\xa0":
			regionCountryDeaths=0
		if str(regionCountryName)=="\xa0":
			regionCountryName=0
		logs(f"[+] {regionName}:{regionCountryName}:{regionCountryCases},{regionCountryDeaths},{regionCountryCasesLast}...")
		world[regionName][regionCountryName]=[regionCountryCases,regionCountryDeaths,regionCountryCasesLast]
		oldRegionName=regionName

frCases,frDeaths,frCasesNew=world["Europe"]["France"]
beCases,beDeaths,beCasesNew=world["Europe"]["Belgium"]
caCases,caDeaths,caCasesNew=world["America"]["Canada"]
frLetality=getLetality(frDeaths,frCases)
beLetality=float(getLetality(beDeaths,beCases))
caLetality=float(getLetality(caDeaths,caCases))
ueCases,ueDeaths,ueCasesNew=getRegionTotal("Europe")
ueLetality=getLetality(ueDeaths,ueCases)
worldCases,worldDeaths,worldCasesNew=getWorldTotal()
worldLetality=getLetality(worldDeaths,worldCases)
frCasesDiff, frDeathsDiff, frCasesNewDiff, frLetalityDiff, ueCasesDiff, ueDeathsDiff, ueCasesNewDiff, ueLetalityDiff, worldCasesDiff, worldDeathsDiff, worldCasesNewDiff, worldLetalityDiff, beCasesDiff, beDeathsDiff, beCasesNewDiff, beLetalityDiff, caCasesDiff, caDeathsDiff, caCasesNewDiff, caLetalityDiff= finalDiffRapport()

toSend1=(f"#Covid_19 #coronavirus #CoronaUpdate\n🇫🇷 Total:\nCas: {formatNum(frCases)} ({formatNum(frCasesDiff)}).\nMort(s): {formatNum(frDeaths)} ({formatNum(frDeathsDiff)}).\nNouveau cas (15 dernier jours): {formatNum(frCasesNew)}.\nLétalité: {str(frLetality)[:5]}% ({str(frLetalityDiff)[:5]}%).")
toSend2=(f"#Covid_19 #coronavirus #CoronaUpdate\n🇧🇪 Total:\nCas: {formatNum(beCases)} ({formatNum(beCasesDiff)}).\nMort(s): {formatNum(beDeaths)} ({formatNum(beDeathsDiff)}).\nNouveau cas (15 dernier jours): {formatNum(beCasesNew)}.\nLétalité: {str(beLetality)[:5]}% ({str(beLetalityDiff)[:5]}%).")
toSend3=(f"#Covid_19 #coronavirus #CoronaUpdate\n🇪🇺 Total:\nCas: {formatNum(ueCases)} ({formatNum(ueCasesDiff)}).\nMort(s): {formatNum(ueDeaths)} ({formatNum(ueDeathsDiff)}).\nNouveau cas (15 dernier jours): {formatNum(ueCasesNew)}.\nLétalité: {str(ueLetality)[:5]}% ({str(ueLetalityDiff)[:5]}%).")
toSend4=(f"#Covid_19 #coronavirus #CoronaUpdate\n🇨🇦 Total:\nCas: {formatNum(caCases)} ({formatNum(caCasesDiff)}).\nMort(s): {formatNum(caDeaths)} ({formatNum(caDeathsDiff)}).\nNouveau cas (15 dernier jours): {formatNum(caCasesNew)}.\nLétalité: {str(caLetality)[:5]}% ({str(caLetalityDiff)[:5]}%).")
toSend5=(f"#Covid_19 #coronavirus #CoronaUpdate\n🌍 Total:\nCas: {formatNum(worldCases)} ({formatNum(worldCasesDiff)}).\nMort(s): {formatNum(worldDeaths)} ({formatNum(worldDeathsDiff)}).\nNouveau cas (15 dernier jours): {formatNum(worldCasesNew)}.\nLétalité: {str(worldLetality)[:5]}% ({str(worldLetalityDiff)[:5]}%).")

logs("[*] Envoie des messages...")

if int(frCasesDiff) > 0 and int(frDeathsDiff) > 0:
	api.update_status(toSend1)
if int(beCasesDiff) > 0 and int(beDeathsDiff) > 0:
	api.update_status(toSend2)
if int(ueCasesDiff) > 0 and int(ueDeathsDiff) > 0:
	api.update_status(toSend3)
if int(caCasesDiff) > 0 and int(caDeathsDiff) > 0:
	api.update_status(toSend4)
if int(worldCasesDiff) > 0 and int(worldDeathsDiff) > 0:
	api.update_status(toSend5)

#Generate rapport for the next execution.
generateRapport()
