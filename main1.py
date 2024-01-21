# modules that i need

from jugaad_data import nse
from dateutil.relativedelta import relativedelta
from datetime import date
from os import path
import time
from matplotlib import pyplot as plt
import sys

stock_name = sys.argv[1]
year = int(sys.argv[2])

today_date = date.today()
start_date = today_date - relativedelta(years = year)

df = nse.stock_df(stock_name,start_date,today_date)

header = ['DATE','OPEN','CLOSE','HIGH','LOW','LTP','VOLUME','VALUE','NO OF TRADES']
times = []
sizes = []

df = df.loc[:,header]

#csv file
stime = time.time()
df.to_csv("SBIN.csv", index=False)
etime = time.time()
times.append((etime-stime)*10000)
sizes.append(path.getsize("SBIN.csv"))

#txt file
stime = time.time()
df.to_csv("SBIN.txt", sep='\t', index=False)
etime = time.time()
times.append((etime-stime)*10000)
sizes.append(path.getsize("SBIN.txt"))

#json file
stime = time.time()
df.to_json("SBIN.json")
etime = time.time()
times.append((etime-stime)*10000)
sizes.append(path.getsize("SBIN.json"))



plt.scatter(times,sizes)
plt.tight_layout()
plt.show()

