from bs4 import BeautifulSoup as soup
import requests
from datetime import datetime
from datetime import timedelta
import re
import csv

def GetStations():
    StationList = "H:\\CrashWeatherData\\LISTOFSTATIONS.txt"
    f = open(StationList, "r")
    String = f.read()
    Stations = re.findall(r'\(\w+\)', String)
    Stations = [s.strip('(') for s in Stations]
    Stations = [s.strip(')') for s in Stations]

    StationsList = []
    for station in Stations:
        if station not in StationsList:
            StationsList.append(station)

    finallistUSED = []
    finallistTOTAL = []
    for item in StationsList:
        
        urlcreate = ('https://www.wunderground.com/weather/us/ga/atlanta/' + item)  
        url = requests.get(urlcreate)
        souptext = soup(url.content, 'html.parser')
        location = []
        i = 0
        for subheading in souptext.findAll('span', {'class':'subheading'}):
            for strong in subheading.findAll('strong'): 
                text = strong.text
                text = float(text)
                if i == 1 and ( 33.59 < text < 33.94):
                    if text*100 not in range(3373, 3388):
                        location.append(text)
                elif i == 2 and ( 84.53 < text < 84.28):
                    if text*100 not in range(8428, 8444):
                        location.append(text)
                elif i == 0:
                        location.append(text)
                        
        if len(location) == 3:
            finallistTOTAL.append(item + '-' + str(location[0]) + '-' + str(location[1]) + '-' + str(location[2]))
            finallistUSED.append(item)
 
    return finallistUSED , finallistTOTAL
     
def GetDeltaDays(Currentdate): 
    date_format = "%Y-%m-%d"
    d0 = datetime.strptime(Currentdate, date_format)
    d1 = datetime.strptime('2017-10-01', date_format)
    delta = d0 - d1
    delta = (delta.days)
    print(delta)
    return delta

# Generating table from https://www.wunderground.com/
def GetTable(errorSTAT, errorCOUNT, year, month, day, urlcreate): 
    i = 0
    try:
        testitem = souptext.find('div', {'class':'scrollable'})
        tester = testitem.text
        for scrollable in souptext.findAll('div', {'class':'scrollable'}):
            for TD in scrollable.findAll('tr', {'class':'ng-star-inserted'}):
                lister = [str(year) + str(month) + str(day)]
                for item in TD:
                    i += 1
                    text = str(item.text)
                    if text.find(':') != -1:
                        t = re.split(':| ', text)
                        if (t[2] == 'PM') and (t[0] != '12'):
                            h = (int(t[0]) + 12)
                        elif (t[0] == '12') and (t[2] == 'AM'):
                            h = ''
                        elif (t[2] == 'PM') and (t[0] == '12'):
                            h = int(12)
                        else:
                            h = (int(t[0]))
                        text = str(h) + str(t[1])
                        lister.append(text)
    
                    else:
                        t = text.translate(str.maketrans({'F': '', '%': '', '-': '0', 'n': '', ' ': '0', 'i': ''}))
                        x = t.strip()
                        lister.append(x)
                # Remove last element
                lister.pop()
                csvwriter.writerow(lister)
                csvwriter.writerow(lister)
                csvwriter.writerow(lister)
    except:
        print('miss')        
        errorSTAT = 1
        errorCOUNT += 1

    return errorSTAT, errorCOUNT


Currentdate = (datetime.now()).strftime('%Y-%m-%d')
delta = GetDeltaDays(Currentdate)
NewTime = (datetime.now() - timedelta(days=(delta)) ).strftime('%Y-%m-%d')
PATH = 'H:\\CrashWeatherData\\ALL\\'
PATH2 = 'H:\\CrashWeatherData\\DATA INFO\\'

finallistUSED , finallistTOTAL = GetStations()
print('CHECK')

with open(PATH2 + "Station-Latitude-Longitude" + '.csv', 'a', newline='') as csvINFO:
    f = csvINFO
    writer = csv.DictWriter(
           f, fieldnames=["Station", "Elevation ft", "Latitude", "Longitude" ])
    writer.writeheader()
    csvINFOMKR = csv.writer(csvINFO)
    print('check')
    for station in finallistTOTAL:
        newS = station.split('-')
        newS[3] = '-' + str(newS[3])       
        csvINFOMKR.writerow(newS)
    print('final')

# Total list of relevant weather stations
finallistUSED =  [ 
    'KGAATLAN330', 'KGAATLAN474', 'KGAATLAN432', 'KGAATLAN562', 'KGAATLAN420', 
    'KGAATLAN94', 'KGADECAT57', 'KGAATLAN276', 'KGAATLAN606', 'KGAAVOND3', 'KGADECAT68', 
    'KGADECAT7', 'KGAATLAN467', 'KGAATLAN431', 'KGAATLAN552', 'KGAATLAN557', 'KGANORTH4', 
    'KGAFORES2', 'KGAATLAN586', 'KGAATLAN487', 'KGAATLAN378', 'KGAATLAN578', 'KGAATLAN46', 
    'KGASMYRN23', 'KGATUCKE23', 'KGASMYRN21', 'KGAATLAN528', 'KGAATLAN331', 'KGAATLAN25', 
    'KGALAKEC4', 'KGAMABLE2', 'KGAATLAN585', 'KGAATLAN536', 'KGASMYRN53', 'KGADUNWO9', 
    'KGAMOUNT7', 'KGASIBLE2', 'KGAATLAN85', 'KGASMYRN34', 'KGASTOCK15', 'KGAATLAN16', 
    'KGAATLAN525', 'KGAATLAN573', 'KGAATLAN444', 'KGAATLAN80', 'KGAATLAN449', 'KGADECAT59',
     'KGAATLAN473', 'KGAATLAN489', 'KGAATLAN393', 'KGAATLAN427', 'KGAATLAN405', 'KGAATLAN351',
      'KGADECAT47', 'KGAATLAN326', 'KGAAVOND8', 'KGAATLAN195', 'KGAATLAN495', 'KGAATLAN338',
       'KGAATLAN501', 'KGATUCKE26', 'KGAATLAN537', 'KGAOAKSO2', 'KGASMYRN57', 'KGAATLAN441',
        'KGAATLAN340', 'KGAATLAN607', 'KGAATLAN460', 'KGAATLAN361', 'KGATUCKE14', 'KGAATLAN379',
         'KGADECAT15', 'KGAATLAN592', 'KGAATLAN390', 'KGATUCKE28', 'KGADECAT72', 'KGAATLAN529',
          'KGATUCKE4', 'KGAATLAN115', 'KGAATLAN125', 'KGAATLAN497', 'KGAATLAN448']

FIN = 0

for Station in finallistUSED:
   errorCOUNT = 0
   errorSTAT = 0        
   with open(PATH + Station + 'WeatherScraper' + '.csv', 'w', newline='') as csvfile:
       csvwriter = csv.writer(csvfile)
   
       while NewTime != '2018-06-20':        
           
           NewTime = (datetime.now() - timedelta(days=(delta)) ).strftime('%Y-%m-%d')
           print(NewTime)
           NewTimeSP = NewTime.split('-')
           year = NewTimeSP[0]
           month = NewTimeSP[1]
           day = NewTimeSP[2]
           
           urlcreate = ('https://www.wunderground.com/dashboard/pws/' + Station + '/table/' + NewTime + '/' + NewTime + '/daily')  
           delta -= 1

           url = requests.get(urlcreate)
           souptext = soup(url.content, 'html.parser')
           lib = 'lib-display-unit'
           
           errorSTAT, errorCOUNT = GetTable(errorSTAT, errorCOUNT, year, month, day, urlcreate)
           
           if errorSTAT == 1:
               with open(PATH + Station + 'ErrorReport' + '.csv', 'a', newline='') as csvError:
                       csvErrorReport = csv.writer(csvError)
                       csvErrorReport.writerow([finallistUSED[FIN]])
                       csvErrorReport.writerow(['URL: ', urlcreate])
                       csvErrorReport.writerow(['Missing Day!: ',  str(year) + str(month) + str(day)])
                       errorSTAT = 0
               
           if errorCOUNT >= 25:
               with open(PATH + Station + 'ErrorReport' + '.csv', 'a', newline='') as csvError:
                   csvErrorReport = csv.writer(csvError)
                   csvErrorReport.writerow(['ERROR LIMIT EXCEEDED'])
               NewTime = '2018-06-20'
 
   delta = GetDeltaDays(Currentdate)
   NewTime = (datetime.now() - timedelta(days=(delta)) ).strftime('%Y-%m-%d')
   FIN += 1
   
   csvfile.close()
   csvError.close()  