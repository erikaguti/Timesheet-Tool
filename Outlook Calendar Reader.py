import pandas as pd
from datetime import datetime
from datetime import date
import os
import argparse


def process_data(calendar_data):
    time = calendar_data[['Subject', 'Start Date','Start Time', 'End Time', 'Description']]

    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    days = []
    for index, row in time['Start Date'].items():
        days.append(weekDays[datetime.strptime(time['Start Date'][index], "%m/%d/%Y").weekday()])
    time['Weekday'] = days

    Hours = []
    for index, row in time.iterrows():
        delta = datetime.strptime(time['End Time'][index], "%I:%M:%S %p") - datetime.strptime(time['Start Time'][index], "%I:%M:%S %p")
        Hours.append(delta.seconds/3600)
    time['Hours Worked'] = Hours

    clean = time[['Start Date', 'Weekday','Subject','Hours Worked', 'Description']]
    clean.Description = clean.Description.astype(str)
    final = clean.groupby(['Start Date','Weekday','Subject']).sum()
    final['Notes'] = clean.groupby(['Start Date', 'Weekday','Subject'])['Description'].apply(';'.join)
    final.drop('Description', axis=1, inplace = True)
    return final


def main(input_file, output_file='output.xlsx'):
    calendar_data = pd.read_csv(input_file)
    df = process_data(calendar_data)
    df.to_excel(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert multiband images to RGB format using rasterio.')
    parser.add_argument('--input_file', type=str, required=True, help='Path to raw calendar data')
    parser.add_argument('--output_file', type=str, required=False, help='Name you want to give final file')

    args = parser.parse_args()
    main(args.input_file, args.output_file)