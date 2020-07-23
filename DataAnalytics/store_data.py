import requests
import csv
url = 'https://api.covid19india.org/data.json'
resp = requests.get(url)
resp = resp.json()
tested = resp["tested"]
# keys = tested.keys()
# print(keys)
# print(tested)
keys = ['_ckd7g', 'source', 'testsconductedbyprivatelabs', 'totalindividualstested', 'totalpositivecases', 'totalsamplestested', 'updatetimestamp']
csvFile = open('tested.csv', 'w')
csv_writer = csv.writer(csvFile)
csv_writer.writerow(keys)
for dict_data in tested:
	to_append = []
	for key in keys:
		if not dict_data.get(key, None):
			to_append.append('nan')
		else:
			to_append.append(dict_data.get(key))
	csv_writer.writerow(to_append)
csvFile.close()