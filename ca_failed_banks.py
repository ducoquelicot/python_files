import csv
import datetime
import os
import urllib.request

url = 'https://www.fdic.gov/bank/individual/failed/banklist.csv'
urllib.request.urlretrieve(url, os.path.expanduser('~/Desktop/failed_banks.csv'))

with open(os.path.expanduser('~/Desktop/failed_banks.csv'), 'r', encoding="ISO-8859-1") as failed_banks:
    reader = csv.reader(failed_banks)
    ca_failed_banks = []
    failed_banks.readline()
    for row in reader:
        row[5] = datetime.datetime.strptime(row[5], '%d-%b-%y').strftime('%Y-%m-%d')
        if row[2] == 'CA':
            ca_failed_banks.append(row)

with open(os.path.expanduser('~/Desktop/ca_failed_banks.csv'), 'w') as ca_banks:
    writer = csv.writer(ca_banks)
    writer.writerow(["bank_name", "city", "state", "cert", "acq_institution", "closing_date", "updated_date"])
    writer.writerows(ca_failed_banks)

print(len(ca_failed_banks))