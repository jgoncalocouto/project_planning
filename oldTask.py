# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:29:10 2021

@author: JOGNC
"""

from datetime import datetime,timedelta
import warnings
from enum import Enum
import numpy as np

class Scenario(Enum):
    NOMINAL=0
    UPPER=1
    LOWER=-1

class OldTask():
    name: str
    description: str
    cost: tuple
    start_date: datetime
    end_date: datetime
    duration: timedelta
    active_scenario: dict
    duration_db=dict
    cost_db: dict
    responsible: int
    parent: int
    structure_level:int
    dependencies: list
    task_id:int
    
    
    
    
    def __init__(
                 self,description="",
                 cost=(0,"EUR"),
                 active_scenario={"cost":Scenario.NOMINAL,"duration":Scenario.NOMINAL},
                 **kwargs
                 ):
        
        self.task_id=id(self)
         # Initialize dbs:
        self.duration_db={"NOMINAL":timedelta(seconds=0),"UPPER":timedelta(seconds=0),"LOWER": timedelta(seconds=0)}
        self.cost_db={"NOMINAL":(0,"EUR"),"UPPER":(0,"EUR"),"LOWER": (0,"EUR")}
    
        # ensure that the min quantity of user inputs is provided
        min_inputs1=["name","start_date"]
        if not all(attr in kwargs  for attr in min_inputs1):
            raise AttributeError("Missing attributes. At least: " + str(min_inputs1) + " must be defined.")
        else:
            for key in min_inputs1:
                setattr(self, key, kwargs[key])
        
        
        #set default attributes
        default_inputs=["active_scenario","description","cost"]
        self.active_scenario=active_scenario
        self.description=description
        self.cost=cost
        
        # ensure that the min quantity of user inputs is provided
        min_inputs2=["duration"]
        if not all(attr in kwargs  for attr in min_inputs2):
            raise AttributeError("Missing attributes. At least: " + str(min_inputs2) + " must be defined.")
        else:
            for key in min_inputs2:
                setattr(self, key, kwargs[key])
        
        min_inputs=min_inputs1+min_inputs2
                

        # ensure that only attributes not in min_inputs or default inputs are being looped here
        entries_to_remove=min_inputs+default_inputs
        for k in entries_to_remove:
            kwargs.pop(k, None)
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            


        
        

            
    
    def __setattr__(self, key, value):
        
        str_attributes=["name","description"]
        datetime_attributes=["start_date","end_date"]
        timedelta_attributes=["duration"]
        tuple_attributes=["cost"]
        
        if key in str_attributes:
            if not isinstance(value, str):
                raise TypeError("Attribute in " + str(str_attributes) + " not a string")
        if key in datetime_attributes:
            if not (type(value) is datetime):
                raise TypeError("Attribute in " + str(datetime_attributes) + " not a datetime")
        if key in timedelta_attributes:
            if not isinstance(value, timedelta):
                raise TypeError("Attribute in " + str(timedelta_attributes) + " not a timedelta")
        if key in tuple_attributes:
            if not isinstance(value, tuple):
                raise TypeError("Attribute in " + str(tuple_attributes) + " not a tuple")
        
        self.__dict__[key] = value
        if key == "end_date":
            self.check_end_date()
        elif key == "duration":
            self.duration_db[self.active_scenario["duration"].name]=self.duration
            self.check_end_date()
        elif key=="cost":
            self.cost_db[self.active_scenario["cost"].name]=self.cost
        elif key == "active_scenario":
            self.duration=self.duration_db[self.active_scenario["duration"].name]
            self.cost=self.cost_db[self.active_scenario["cost"].name]
        else:
            pass

        
            
        
        
    def __getattr__(self, attr):
        if attr=="end_date":
            self.end_date=self.start_date+self.duration
            return self.end_date
            


    def check_end_date(self):
        if self.end_date < self.start_date+self.duration:
            self.end_date=self.start_date+self.duration
            #warnings.warn("'end_date' chosen violates the condition: 'end_date'>'start_date' + 'duration'. 'end_date' set to minimum value: 'end_date'='start_date' + 'duration'")
    
    @staticmethod
    def get_workdays(from_date, to_date):
        # if the start date is on a weekend, forward the date to next Monday
        if from_date.weekday() > 4:
            from_date = from_date + timedelta(days=7 - from_date.weekday())
        # if the end date is on a weekend, rewind the date to the previous Friday
        if to_date.weekday() > 4:
            to_date = to_date - timedelta(days=to_date.weekday() - 4)
        if from_date > to_date:
            return 0
        # that makes the difference easy, no remainders etc
        diff_days = (to_date - from_date).days + 1
        weeks = int(diff_days / 7)
        return weeks * 5 + (to_date.weekday() - from_date.weekday()) + 1
    
    @staticmethod
    def determine_workdays(duration):
        durationInSecs=duration.total_seconds()
        durationInWorkingDays=durationInSecs//Task.WorkingHours.total_seconds()
        remainder=durationInSecs-durationInWorkingDays*Task.WorkingHours.total_seconds()
        duration=timedelta(days=durationInWorkingDays,seconds=remainder)
        return duration
    
    @staticmethod
    def get_endWorkdate(startDate,duration):
        days2add=duration.total_seconds()//(24*3600)
        endDate=startDate
        while days2add>0:
            if endDate.weekday()==1:
                endDate=endDate+timedelta(days=1)
            elif endDate.weekday()==7:
                endDate=endDate+timedelta(days=2)
            elif endDate.weekday()==6:
                endDate=endDate+timedelta(days=3)
                days2add=days2add-1
            else:
                endDate=endDate+timedelta(days=1)
                days2add=days2add-1
        return endDate
        
        
            
    
    
    
    def minimize_end_date(self,effort_level,work_hours,work_days):
        #effort level measures the percentage of the time the responsible can work on the task
        pass

    
    # Solve the issue with util days (use dtu: https://dateutil.readthedocs.io/en/stable/)
    #method to minimize end_date
    #method to promote/demote task level (relation with parent)
    #method to check if added dependencies are in agreement with the level/parent
    #method to validate currency