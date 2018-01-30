import os
import csv
import datetime
import json
import xlrd
import requests
import requests_cache
from operator import itemgetter
import re


requests_cache.install_cache('ris_cache', backend='sqlite') #, expire_after=180)

data =[]
workbook = xlrd.open_workbook('RIS%20adressen%20-%20te%20verrijken%20door%20DATALAB%2020170320.xlsx')
# Show sheets
sheet_names = workbook.sheet_names()
print(sheet_names)

# Load each sheet
#for i in range(0,1):
worksheet = workbook.sheet_by_index(0)

# Key names
first_row = [] 
for col in range(0,3):	
	first_row.append( worksheet.cell_value(0,col).title() )

print(first_row)

# loop all rows on every column (=Section)

for row in range(1, worksheet.nrows):
	#print(worksheet.cell_value(row,0))

	newItem ={}
	newItem["Zaaknummer"] = int(worksheet.cell_value(row,0))
	newItem["Adres"] = str(worksheet.cell_value(row,1)).strip()	
	postcodeCell = str(worksheet.cell_value(row,2)).strip()	
	if postcodeCell == '0000AA' or re.match(r'^[0-9.]+$',postcodeCell) or re.match(r'^[2-9]{1}',postcodeCell) :
		print('TRUE')
		postcodeCell = ''
	else:
		postcodeCell = str(worksheet.cell_value(row,2)).strip()			

	pc6 = re.match(r'(\d{4}\s*[A-Z]{2})', postcodeCell)
	if pc6:
		newItem["Postcode"] = pc6.group(1)
	else:
		newItem["Postcode"] = postcodeCell
	adresClean = re.sub(r'.*;','',newItem["Adres"])
	adresClean = re.sub(r'[+.]','',adresClean)
	adresClean = re.sub(r'[I]{1,3}$','',adresClean)
	adresClean = re.sub(r'[-/][A-Z0-9]*$','',adresClean)
	adresClean = re.sub(r'hs$','-H',adresClean,flags=re.IGNORECASE)
	adresClean = re.sub(r'huis$','-H',adresClean)
	adresClean = re.sub(r'hg$','',adresClean)
	newItem["Adres_opgeschoond"] = re.sub(r'  ',' ',adresClean)						
	data.append(newItem)
	#print(newItem)	

print('items: '+ str(len(data)))

for index, item in enumerate(data):
	print('item: '+ str(index)+' of '+str(len(data)))
	#if re.match(r'\d{4}\s*[A-Z]{2}',item["Postcode"]):	
	item["Straatnaam BAG"] = ''	
	item["Huisnummer BAG"] = ''
	item["Woonplaats BAG"] = ''
	item["Matching"] = 'Postcode reeds bekend'	
	#else:
	try:
		url = requests.get('http://geodata.nationaalgeoregister.nl/locatieserver/free?q='+item["Adres_opgeschoond"]+' '+'Amsterdam&rows=1')
		result = json.loads(url.text)
		resultBAG = result["response"]["docs"][0]	
		#print(resultBAG)
		try:
			if resultBAG["woonplaatsnaam"]=='Amsterdam':
				item["Postcode"] = resultBAG["postcode"]
				item["Straatnaam BAG"] = resultBAG["straatnaam"]
				item["Huisnummer BAG"] = resultBAG["huis_nlt"]
				item["Woonplaats BAG"] = resultBAG["woonplaatsnaam"]
				item["Matching"]= 'Match gevonden, mogelijk wel verkeerd adresmatch'
			else:
				item["Straatnaam BAG"] = resultBAG["straatnaam"]
				item["Huisnummer BAG"] = resultBAG["huis_nlt"]
				item["Woonplaats BAG"] = resultBAG["woonplaatsnaam"]
				item["Matching"]= 'Match gevonden, in andere woonplaats'
		except:
			item["Straatnaam BAG"] = resultBAG["straatnaam"]
			item["Huisnummer BAG"] = ''
			item["Woonplaats BAG"] = resultBAG["woonplaatsnaam"]
			item["Matching"] = 'Geen huisnummer bekend'
			continue
	except:
		item["Straatnaam BAG"] = ''	
		item["Huisnummer BAG"] = ''
		item["Woonplaats BAG"] = ''
		item["Matching"] = 'Geen match gevonden'

#print(data2)

with open('outputRIS.csv', 'w') as f:
    w = csv.DictWriter(f, data[0].keys())
    w.writeheader()
    for item in data:
    	#print(item)
    	w.writerow(item)
