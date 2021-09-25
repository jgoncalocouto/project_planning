# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import datetime
import warnings


class Task:
    name: str
    description: str
    cost: tuple
    start_date: datetime.datetime
    end_date: datetime.datetime
    duration: datetime.timedelta
    
    
    def __init__(self,description="",cost=(0,"EUR"), **kwargs):
        
        # ensure that the min quantity of user inputs is provided
        min_inputs=["name","start_date","duration"]
        if not all(attr in kwargs  for attr in min_inputs):
            raise AttributeError("Missing attributes. At least: " + str(min_inputs) + " must be defined.")
        else:
            for key in min_inputs:
                self.key=kwargs[key]
        
        self.description=description
        self.cost=cost
            

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
        
        
    def __getattr__(self, attr):
        if attr=="end_date":
            self.end_date=self.start_date+self.duration


    def check_end_date(self):
        if self.end_date < self.start_date+self.duration:
            self.end_date=self.start_date+self.duration
            warnings.warn("'end_date' chosen violates the condition: 'end_date'>'start_date' + 'duration'. 'end_date' set to minimum value: 'end_date'='start_date' + 'duration'")
            
  


    