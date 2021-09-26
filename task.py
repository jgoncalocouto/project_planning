# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import datetime
import warnings
from enum import Enum
import numpy as np

class Scenario(Enum):
    NOMINAL=0
    UPPER=1
    LOWER=-1
    
    


class Task:
    name: str
    description: str
    cost: tuple
    start_date: datetime.datetime
    end_date: datetime.datetime
    duration: datetime.timedelta
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
        self.duration_db={"NOMINAL":datetime.timedelta(seconds=0),"UPPER":datetime.timedelta(seconds=0),"LOWER": datetime.timedelta(seconds=0)}
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
            if not (type(value) is datetime.datetime):
                raise TypeError("Attribute in " + str(datetime_attributes) + " not a datetime")
        if key in timedelta_attributes:
            if not isinstance(value, datetime.timedelta):
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


    
if __name__ == "__main__":
    s=Task(
        name="Sim",
        start_date=datetime.datetime(2021,1,1),
        duration=datetime.timedelta(hours=25))
    s.description="really boring test task"
    
    print(["end_date:",s.end_date])
    s.duration=datetime.timedelta(days=25)
    print(["duration: ",s.duration])
    print(["end_date:",s.end_date])
    s.duration=datetime.timedelta(days=1)
    print(["duration: ",s.duration])
    print(["end_date:",s.end_date])
    #method to minimize end_date
    #method to assign responsible?
    #method to promote/demote task level (relation with parent)
    #method to check if added dependencies are in agreement with the level/parent
  


    