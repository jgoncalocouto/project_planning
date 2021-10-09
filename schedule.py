# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 19:39:19 2021

@author: JOGNC
"""

from datetime import *

class Schedule():
    
    WeekdayOff={5,6}
    startHour=9
    endHour=18
    LunchTime=timedelta(hours=1)
    WorkingHours=timedelta(hours=(startHour-endHour))-LunchTime
    NationalHolidays={
        (1,1), #New year
        (4,2), # Holy Friday
        (4,4), # Easter
        (4,25),  # Freedom day
        (5,1), # Labour day
        (5,3), # Body of God (?)
        (5,10),  # Portugal Day (?)
        (8,15), #Assumption of Our Lady (?)
        (10,5), #Replubic's creation day (?)
        (11,1), #All saints day (?)
        (12,1), #Independence day (?)
        (12,8), #Day of the holy Conceição (?)
        (12,25),  #Christmas Day (?)
        }

    
    def __init__(self,VacationDays=set()):
        self.VacationDays=VacationDays
    
    @property
    def VacationDays(self):
        return self._VacationDays
    @VacationDays.setter
    def VacationDays(self,VacationDays):
        for dayi in VacationDays:
            if dayi.weekday() in self.WeekdayOff:
                VacationDays.remove(dayi)
            elif (dayi.month,dayi.day) in self.NationalHolidays:
                VacationDays.remove(dayi)
        self._VacationDays=VacationDays

    def get_workdays(self,startDate,endDate):
        # populate a set with the available working days between start and end date
        ndays=endDate-startDate
        ndays=ndays.days
        dates=set([])
        for i in range(ndays+1):
            dayi=startDate+timedelta(days=i)
            if (dayi.weekday() not in self.WeekdayOff) and (dayi not in self.VacationDays) and ((dayi.month, dayi.day)  not in self.NationalHolidays):
                dates.add(dayi)
        # Calculate the (hour,minute,second,...) having into account the scheduled start and end hour
        expectedStartDate=datetime(startDate.year,startDate.month,startDate.day,self.startHour,0,0)
        expectedEndDate=datetime(endDate.year,endDate.month,endDate.day,self.endHour,0,0)
        hours2add=(expectedStartDate-startDate)-(expectedEndDate-endDate)
        # Total duration is given by:
        duration=timedelta(days=len(dates))+hours2add-self.LunchTime
        return duration
    
    def end_workdate(self,startDate,duration):
        ndays=duration//(self.WorkingHours) #number of working days
        remainder=duration-ndays*self.WorkingHours # hours that remain and not complete a full working day
        #Compute endDate
        dates=set([])
        for i in range(ndays+1):
            dayi=startDate+timedelta(days=i)
            if (dayi.weekday() not in self.WeekdayOff) and (dayi not in self.VacationDays) and ((dayi.month,dayi.day) not in self.NationalHolidays):
                dates.add(dayi)
        endDate=max(dates)+remainder
        return endDate
        
    
    def get_startdate(self,endDate,duration):
        pass
                

if __name__=="__main__":
    s=Schedule()
    print(s.get_workdays(datetime(2020,1,1),datetime(2025,1,1)))
    
    
    
    
