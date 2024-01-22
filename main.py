# modules that i need

from jugaad_data import nse
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date
from os import path
import time
from matplotlib import pyplot as plt
import sys
import pyarrow


stock_name = sys.argv[1]
yearI = sys.argv[2]
try:
    global year
    year = int(yearI)
except ValueError:
    print("That's not a valid input for number of years, please input non-negative integer")
    quit()

file_extensions = [".csv", ".txt" , ".json", ".html",".parquet",".feather",".png"]
file_names = []

for i in range(0,len(file_extensions)):
    file_names.append(stock_name+file_extensions[i])

indx = 0

# csv = stock_name + ".csv"
# txt = stock_name + ".txt"
# json = stock_name + ".json"
# html = stock_name + ".html"
# parquet = stock_name + ".parquet"
# excel = stock_name + ".xlsx"

png = stock_name + ".png"

today_date = date.today()
start_date = today_date - relativedelta(years = year)

df = nse.stock_df(stock_name,start_date,today_date)

header = ['DATE','OPEN','CLOSE','HIGH','LOW','LTP','VOLUME','VALUE','NO OF TRADES']

times = []
sizes = []

df = df.loc[:,header]

#csv file
stime = time.time()
df.to_csv(file_names[indx], index=False)
etime = time.time()
times.append((etime-stime)*1000)
sizes.append((path.getsize(file_names[indx]))/1024)
indx += 1

#txt file
stime = time.time()
df.to_csv(file_names[indx], sep='\t', index=False)
etime = time.time()
times.append((etime-stime)*1000)
sizes.append((path.getsize(file_names[indx]))/1024)
indx += 1

#json file
stime = time.time()
df.to_json(file_names[indx])
etime = time.time()
times.append((etime-stime)*1000)
sizes.append((path.getsize(file_names[indx]))/1024)
indx += 1

#to html
stime = time.time()
df.to_html(file_names[indx],index=False)
etime = time.time()
times.append((etime-stime)*1000)
sizes.append((path.getsize(file_names[indx]))/1024)
indx += 1

#to parquet
stime = time.time()
df.to_parquet(file_names[indx],index = False)
etime = time.time()
times.append((etime-stime)*1000)
sizes.append((path.getsize(file_names[indx]))/1024)
indx += 1

#to excel
# stime = time.time()
# df.to_excel(file_names[indx], sheet_name=stock_name)
# etime = time.time()
# times.append((etime-stime)*1000)
# sizes.append((path.getsize(file_names[indx]))/1024)
# indx += 1

#to feather (binary)
stime = time.time()
df.to_feather(file_names[indx])
etime = time.time()
times.append((etime-stime)*1000)
sizes.append((path.getsize(file_names[indx]))/1024)
indx += 1

l=[]
for i in range(0,len(file_names)-1):
    l.append(file_extensions[i][1:])

# l = ['csv','txt','json','html','parquet','excel','feather']
    
color =['blue','orange','green','red','purple','black']


for i in range (0,len(l)):
    plt.scatter(times[i],sizes[i],c=color[i],label=l[i])
plt.legend()

# for i, j in zip(times, sizes):
#    plt.text(i, j+1, '({}, {})'.format(int(i), int(j)))

plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.tight_layout()
plt.title("Different file formats on the basis of file size and time taken to write the file")
plt.xlabel("Time taken (ms)")
plt.ylabel("Size used (mega-bytes)")
plt.savefig(png, bbox_inches='tight')
# plt.show()

