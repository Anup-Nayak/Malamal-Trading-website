# modules that i need

from jugaad_data import nse
from dateutil.relativedelta import relativedelta
from datetime import date
from os import path
import time
from matplotlib import pyplot as plt
import sys
import pyarrow


stock_name = sys.argv[1]
year = int(sys.argv[2])

csv = stock_name + ".csv"
txt = stock_name + ".txt"
json = stock_name + ".json"
html = stock_name + ".html"
parquet = stock_name + ".parquet"

today_date = date.today()
start_date = today_date - relativedelta(years = year)

df = nse.stock_df(stock_name,start_date,today_date)

header = ['DATE','OPEN','CLOSE','HIGH','LOW','LTP','VOLUME','VALUE','NO OF TRADES']
times = []
sizes = []

df = df.loc[:,header]

#csv file
stime = time.time()
df.to_csv(csv, index=False)
etime = time.time()
times.append((etime-stime)*10000)
sizes.append(path.getsize(csv))

#txt file
stime = time.time()
df.to_csv(txt, sep='\t', index=False)
etime = time.time()
times.append((etime-stime)*10000)
sizes.append(path.getsize(txt))

#json file
stime = time.time()
df.to_json(json)
etime = time.time()
times.append((etime-stime)*10000)
sizes.append(path.getsize(json))

#to html
stime = time.time()
df.to_html(html,index=False)
etime = time.time()
times.append((etime-stime)*10000)
sizes.append(path.getsize(html))

#to parquet
stime = time.time()
df.to_parquet(parquet,index = False)
etime = time.time()
times.append((etime-stime)*10000)
sizes.append(path.getsize(parquet))


plt.scatter(times,sizes)
plt.tight_layout()
plt.show()

