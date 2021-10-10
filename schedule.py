# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 19:39:19 2021

@author: JOGNC
"""

from datetime import *

class Schedule():
    
    WeekdayOff={5,6}
    _startHour=9
    _endHour=18
    _lunchTime=timedelta(hours=1)
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
            if (dayi.weekday() in self.WeekdayOff) or ((dayi.month,dayi.day) in self.NationalHolidays) :
                VacationDays.remove(dayi)
        self._VacationDays=VacationDays
    
    @property
    def startHour(self):
        return self._startHour
    @startHour.setter
    def startHour(self,startHour):
        self._startHour=startHour
        self.calculate_workingHours()
        
    @property
    def endHour(self):
        return self._endHour
    @endHour.setter
    def endHour(self,endHour):
        self._endHour=endHour
        self.calculate_workingHours()
        
    @property
    def lunchTime(self):
        return self._lunchTime
    @lunchTime.setter
    def lunchTime(self,lunchTime):
        self._lunchTime=lunchTime
        self.calculate_workingHours()
    
    def calculate_workingHours(self):
        self.WorkingHours=timedelta(hours=(self.startHour-self.endHour))-self.lunchTime

    def get_workdays(self,startDate,endDate,effortLevel=1):
        """
        Parameters
        ----------
        startDate : datetime
            Task Start Date.
        endDate : datetime
            Task End Date.
        effortLevel : float, optional
            Represents the percentage of the responsible's working time will be dedicated to the task. The default is 1.

        Returns
        -------
        duration : timedelta
            working time available between the two dates (Start and End) that can be devoted to the task, having into account the effort level.
        """ 
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
        duration=(timedelta(days=len(dates))+hours2add-self.lunchTime)*effortLevel
        return duration
    
    def get_enddate(self,startDate,duration,effortLevel=1):
        """
        Parameters
        ----------
        startDate : datetime
            Task Start Date.
        duration : timedelta
            amount of useful time required to complete the task.
        effortLevel : float, optional
            Represents the percentage of the responsible's working time will be dedicated to the task. The default is 1.

        Returns
        -------
        endDate : datetime
            Task End Date.
        """
        ndays=duration//(self.WorkingHours*effortLevel) #number of working days
        remainder=duration-ndays*(self.WorkingHours*effortLevel) # hours that remain and not complete a full working day
        #Compute endDate
        dates=set([])
        for i in range(ndays+1):
            dayi=startDate+timedelta(days=i)
            if (dayi.weekday() not in self.WeekdayOff) and (dayi not in self.VacationDays) and ((dayi.month,dayi.day) not in self.NationalHolidays):
                dates.add(dayi)
        endDate=max(dates)+(remainder*(1/effortLevel))
        return endDate
        
    
    def get_startdate(self,endDate,duration,effortLevel=1):
        """
        Parameters
        ----------
        endDate : datetime
            Task End Date.
        duration : timedelta
            amount of useful time required to complete the task.
        effortLevel : float, optional
            Represents the percentage of the responsible's working time will be dedicated to the task. The default is 1.

        Returns
        -------
        startDate : datetime
            Task Start Date.
        """
        ndays=duration//(self.WorkingHours*effortLevel) #number of working days
        remainder=duration-ndays*(self.WorkingHours*effortLevel) # hours that remain and not complete a full working day
        #Compute startDate
        dates=set([])
        for i in range(ndays+1):
            dayi=endDate-timedelta(days=i)
            if (dayi.weekday() not in self.WeekdayOff) and (dayi not in self.VacationDays) and ((dayi.month,dayi.day) not in self.NationalHolidays):
                dates.add(dayi)
        startDate=min(dates)-(remainder*1/(effortLevel))
        return startDate

# Missing: effort level. It should be accounted for when calculating: duration | startDate | endDate           

if __name__=="__main__":
    s=Schedule()
    print(s.get_workdays(datetime(2020,1,1),datetime(2025,1,1)))
    
    
    
    
