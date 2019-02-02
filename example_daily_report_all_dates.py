import os
from datetime import datetime
import calendar


def loadReportFor(date: datetime):
    if date.year == 2019 and date.mont > 1:
        # there wont be any data for this yet anyway
        return
    cmd = f"python3 mainNOW.py --year {date.year} --month {date.month} --day {date.day} --period daily"
    print("Loading report for date: "+str(date)+" with command: "+cmd)
    os.system(cmd)


for year in [2018, 2019]:
    for month in range(1, 13):
        _, daysinmonth = calendar.monthrange(year, month)
        for day in range(1, daysinmonth):
            loadReportFor(datetime(year=year, month=month, day=day))
