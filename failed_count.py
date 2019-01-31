import csv
import operator
import os
import urllib.request

url = "https://www.fdic.gov/bank/individual/failed/banklist.csv"
local_file = os.path.expanduser("~/Desktop/failed_banks.csv")
urllib.request.urlretrieve(url, local_file)

state_count = {}
with open(local_file, "r", encoding="latin-1") as failed_banks:
    reader = csv.DictReader(failed_banks)
    for row in reader:
        state_count.setdefault(row["ST"].strip(), 0)
        state_count[row["ST"].strip()] += 1

state_counts_unpacked = state_count.items()
top_ten = sorted(
    state_counts_unpacked,
    key=operator.itemgetter(1),
    reverse=True
)[:10]

print("Failed Bank States - Top 10")
for state, count in top_ten:
    print("{}: {}".format(state, count))