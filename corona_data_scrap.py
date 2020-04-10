import pandas as pd
import numpy as np
import re
import lxml

from bs4 import BeautifulSoup
from requests import get
%matplotlib inline
from datetime import datetime,date


url = 'http://corona.gov.bd/'
page = get(url)
soup = BeautifulSoup(page.content, 'lxml') 

## Update CSV file for todays update
match_daily = soup.find('ul', class_="statistic__efected-new")
d_count=[]
for num in match_daily.find_all('li'):
    count = num.text
    d_count.append(count)
del d_count[0]
daily_count=[]
for i in range(len(d_count)):
    dc=d_count[i].replace('(','')
    dc=dc.replace('+','')
    dc=dc.replace(')','')
    dc=int(dc)
    daily_count.append(dc)

l_update = datetime.now()
daily_count.append(l_update)
df_d = pd.DataFrame(daily_count,index=['Confirmed','Recovered','Death','Last_Update'])
DF_d = df_d.T
file_name=date.today()
DF_d.to_csv('/Todays_Count/{}.csv'.format(file_name),  encoding='utf-8')

## Create CSV file for total count
t_count=[]
for num in soup.find_all('span', class_='statistic__efected-value'):
    count = int(num.text)
    t_count.append(count)
ac =t_count[0]-(t_count[1]+t_count[2])
t_count.append(ac)
t_count.append(l_update)
dt = pd.DataFrame(t_count,index=['Confirmed','Recovered','Death','Active','Last_Update'])
df = dt.T
df.to_csv('/Total_Count/{}.csv'.format(file_name),  encoding='utf-8')
