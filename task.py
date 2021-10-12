# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from datetime import *
import warnings
from enum import Enum
import numpy as np

    
    


class Task():
    name: str
    description: str
    cost: tuple
    _start_date: datetime
    _end_date: datetime
    _duration: timedelta
    responsible: int
    parent: int
    structure_level:int
    dependencies: list
    task_id:int
    
    
    def __init__(self,name,start_date,duration,description="",cost=(0,"EUR"),parent=[],childs=[]):
        self.name=name
        self.start_date=start_date
        self.duration=duration
        self.description=description
        self.cost=cost
        self.task_id=id(self)
        self.parent=parent
        self.childs=childs
    
    @property
    def end_date(self):
        return self._end_date
    @end_date.setter
    def end_date(self,end_date):
        if end_date < self.start_date+self.duration:
            self._end_date=self.start_date+self.duration
        else:
            self._end_date=end_date
    
    @property
    def duration(self):
        return self._duration
    @duration.setter
    def duration(self,duration):
        self._duration=duration
    
    @property
    def start_date(self):
        return self._start_date
    @start_date.setter
    def start_date(self,start_date):
        self._start_date=start_date

    def check_end_date(self):
        if self.end_date < self.start_date+self.duration:
            self.end_date=self.start_date+self.duration
            #warnings.warn("'end_date' chosen violates the condition: 'end_date'>'start_date' + 'duration'. 'end_date' set to minimum value: 'end_date'='start_date' + 'duration'")
    
    def __getattr__(self, attr):
        if attr=="_end_date":
            self._end_date=self.start_date+self.duration
            return self._end_date
    def isSubtask(self,TaskParent):
        self.parent=TaskParent
        self.structure_level=TaskParent.structure_level+1
        TaskParent.childs.append(self)
        return TaskParent
    
    def isGroup(self,Subtasks):
        eSubtasks=[]
        #Should we do: self.childs=[]?
        for task in Subtasks:
            task.parent=self
            task.structure_level=self.structure_level-1
            eSubtasks.append(task)
            self.childs.append(task)
        return eSubtasks
            
    


    #method to promote/demote task level (relation with parent)
    #method to check if added dependencies are in agreement with the level/parent
    #method to validate currency
    
    


    
if __name__ == "__main__":
    s=Task(
        name="Sim",
        start_date=datetime(2021,1,1),
        duration=timedelta(hours=25))
    s.description="really boring test task"
    print(["end_date:",s.end_date])
#     s.duration=timedelta(days=25)
#     print(["duration: ",s.duration])
#     print(["end_date:",s.end_date])
#     s.duration=timedelta(days=1)
#     print(["duration: ",s.duration])
#     print(["end_date:",s.end_date])

  


    
