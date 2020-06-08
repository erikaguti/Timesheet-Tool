import pandas as pd
from datetime import datetime
from datetime import date
import os

modified = []
for file in os.listdir(os.getcwd()):
    if file.endswith('CSV'):
        modified.append(os.stat(file).st_mtime)
for file in os.listdir(os.getcwd()):    
    if os.stat(file).st_mtime == max(modified):
        raw = pd.read_csv(file, encoding = 'latin1')

time = raw[['Subject', 'Start Date','Start Time', 'End Time', 'Description']]

weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
days = []
for index, row in time['Start Date'].iteritems():
    days.append(weekDays[datetime.strptime(time['Start Date'][index], "%m/%d/%Y").weekday()])
time['Weekday'] = days

Hours = []
for index, row in time.iterrows():
    delta = datetime.strptime(time['End Time'][index], "%I:%M:%S %p") - datetime.strptime(time['Start Time'][index], "%I:%M:%S %p")
    Hours.append(delta.seconds/3600)
time['Hours Worked'] = Hours

clean = time[['Weekday','Subject','Hours Worked', 'Description']]
clean.Description = clean.Description.astype(str)
final = clean.groupby(['Weekday','Subject']).sum()
final['Notes'] = clean.groupby(['Weekday','Subject'])['Description'].apply(';'.join)
final.to_excel('done.xlsx')