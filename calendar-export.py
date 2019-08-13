import pandas as pd
import numpy as np
from datetime import timedelta
from dateparser import parse
from pandas._libs.tslibs.nattype import NaTType
import math

calendar_file = pd.read_csv('as3m19-it-innovation.CSV')

print(calendar_file.head())
#                                              Subject  ...         Categories
# 0                   MJB, PM - FLAME Project Briefing  ...                NaN
# 1  MJB, NS, HW - FLAME CLMC Technical Handover Me...  ...                NaN
# 2                            MJB - Working from Home  ...  working from home
# 3                                      MJB - Holiday  ...            holiday
# 4            MJB - Working from Garage (In By 11:00)  ...  working from home
# [5 rows x 8 columns]

print(calendar_file.columns)
# Out[4]:
# Index(['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time',
#        'All day event', 'Meeting Organizer', 'Categories'],
#       dtype='object')

print(calendar_file.loc[0,:])
# Subject                        Subject
# Start Date                         NaT
# Start Time                         NaT
# End Date                           NaT
# End Time                           NaT
# All day event            All day event
# Meeting Organizer    Meeting Organizer
# Categories                  Categories
# Time                               NaT
# Name: 0, dtype: object

##################################################################################################
headers = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time',
           'All day event', 'Meeting Organizer', 'Categories']
parse_dates = ['Start Date', 'Start Time', 'End Date', 'End Time']
calendar_file = pd.read_csv('as3m19-it-innovation.CSV', names=headers,
                            parse_dates=parse_dates, date_parser=parse)

# remove titles row
calendar_file = calendar_file.loc[1:,:]

calendar_file['End Time'].head()
calendar_file['Time'] = calendar_file['End Time'] - calendar_file['Start Time']

# calendar_file.loc[calendar_file['All day event'] == 'True', 'Time'] = timedelta(hours=0)

# check times are correct
calendar_file['StrTime'] = calendar_file['Time'].map(str)

# check for any invalid dates
print(calendar_file.loc[calendar_file['Start Date'].apply(isinstance, args=(NaTType,)) == True])
print(calendar_file.loc[calendar_file['End Date'].apply(isinstance, args=(NaTType,)) == True])

calendar_file['DateTime'] = calendar_file['Time'] + (calendar_file['End Date'] - calendar_file['Start Date'])

# check date times are correct
calendar_file['StrTime'] = calendar_file['DateTime'].map(str)

# check for negative times
calendar_file['StrTime'].loc[calendar_file['StrTime'].apply(lambda x: x.startswith("-"))]
#### date parsing has gone wrong here as can be see some dates are parsing in american style
##################################################################################################

## try again with specific parsing rules:
headers = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time',
           'All day event', 'Meeting Organizer', 'Categories']
parse_dates = ['Start Date', 'Start Time', 'End Date', 'End Time']
calendar_file = pd.read_csv('as3m19-it-innovation.CSV', names=headers)

# remove titles row
calendar_file = calendar_file.loc[1:,:]

calendar_file['End Time'].head()
et = calendar_file['End Time'].apply(lambda x: parse(str(x), date_formats=['%H:%M:%S']))
st = calendar_file['Start Time'].apply(lambda x: parse(str(x), date_formats=['%H:%M:%S']))

time = et - st
calendar_file['Time'] = time.apply(lambda x: x.total_seconds() / 3600)

calendar_file['End Date'].head()
# ed = calendar_file['End Date'].apply(lambda x: parse(str(x), date_formats=['%d/%m/%Y']))
# sd = calendar_file['Start Date'].apply(lambda x: parse(str(x), date_formats=['%d/%m/%Y']))

def calc_date(row):
    fromdate = parse(str(row['Start Date']), date_formats=['%d/%m/%Y'])
    todate = parse(str(row['End Date']), date_formats=['%d/%m/%Y'])
    daygenerator = (fromdate + timedelta(x + 1)
                    for x in range((todate - fromdate).days))
    day_sum = sum(1 for day in daygenerator if day.weekday() < 5)
    new_date = day_sum * 8.0
    return new_date


calendar_file['DateTime'] = calendar_file.apply(calc_date, axis=1)

calendar_file['DateTime'] = calendar_file['DateTime'] + calendar_file['Time']

# check date times are correct
calendar_file['StrTime'] = calendar_file['DateTime'].map(str)

# check for negative times
calendar_file['StrTime'].loc[calendar_file['StrTime'].apply(lambda x: x.startswith("-"))]

# example row of data: calendar_file.loc[1, ('Subject',)]
# filter by only items with holiday or annual leave in the subject or categories
holiday_only = calendar_file.loc[
    calendar_file['Subject'].str.contains('annual leave|holiday|hol$', na=False, case=False, regex=True) |
    calendar_file['Categories'].str.contains('holiday', na=False, case=False, regex=False)]

# sum it up!
holiday_only[['Meeting Organizer', 'DateTime']].groupby('Meeting Organizer').sum()
