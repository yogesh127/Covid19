import requests
import csv
import json
url = 'https://api.covid19india.org/data.json'
r = requests.get(url)
#print (r.json())
data = r.json()
tested = data['tested']
csvFile = open('tested.csv', 'w') 
count = 0
csv_writer = csv.writer(csvFile) 
for row in tested:
	if count == 0:
		csv_writer.writerow(row.keys())
		count=1
 	csv_writer.writerow(row.values()) 
csvFile.close()