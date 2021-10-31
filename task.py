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
    _dependencies: list
    task_id:int
    
    
    def __init__(self,name,start_date,duration,description="",cost=(0,"EUR"),structure_level=0,parent=[],childs=[],dependencies=[]):
        self.childs=childs
        self.dependencies=dependencies
        self.name=name
        self.start_date=start_date
        self.duration=duration
        self.description=description
        self.cost=cost
        self.task_id=id(self)
        self.parent=parent

        print("init")
        self.structure_level=structure_level
        
    
    @property
    def end_date(self):
        #analyze start_date dependency:
        if self._end_date < self.start_date+self.duration:
            self._end_date=self.start_date+self.duration
        #analyze subtasks:
        if self.childs:
            self.end_date=self.childs[0].end_date
            for child in self.childs:
                if child.end_date>self.end_date:
                    self.end_date=child.end_date
        return self._end_date
    
    @end_date.setter
    def end_date(self,end_date):
        self._end_date=end_date
    
    @property
    def duration(self):
        return self._duration
    @duration.setter
    def duration(self,duration):
        self._duration=duration
    
    @property
    def start_date(self):
        #analyze dependencies:
        for dependency in self.dependencies:
            if dependency.end_date>self._start_date:
                self.start_date=dependency.end_date
        #analyze subtasks:
        if self.childs:
            self.start_date=self.childs[0].start_date
            for child in self.childs:
                if child.start_date<self.start_date:
                    self.start_date=child.start_date
        return self._start_date
    
    @start_date.setter
    def start_date(self,start_date):
        self._start_date=start_date

    @property
    def dependencies(self):
        print("getter")
        return self._dependencies
    @dependencies.setter
    def dependencies(self,dependencies):
        if any(task in dependencies for task in self.childs):
            raise AttributeError("A subtask of a task cannot be a dependency of the same task")
        if self.parent in dependencies:
            raise AttributeError("The parent of a task cannot be a dependency of the that task")
        print("setter")
        self._dependencies=dependencies
    
    def addDependencies(self,Tasks):
        for task in Tasks:
            if task not in self.dependencies:
                self.dependencies.append(task)

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
        self.childs=[]
        self.duration=timedelta()
        for task in Subtasks:
            task.parent=self
            task.structure_level=self.structure_level-1
            eSubtasks.append(task)
            self.childs.append(task)
            self.duration+=childs.duration
        return eSubtasks

    def __str__(self):
        msg2output="Task: "
        msg2output+="lvl= {var}, ".format(var=self.structure_level)
        msg2output+="{var}, ".format(var=self.name)
        msg2output+="'{var}', ".format(var=self.description)
        msg2output+="from: {var} ".format(var=self.start_date)
        msg2output+="to: {var} |".format(var=self.end_date)
        msg2output+="working time: {var}, ".format(var=self.duration)
        msg2output+="Cost={var}".format(varname="cost",var=self.cost)
        msg2output+=")"
        return msg2output
    
    def __repr__(self):
        msg2output="Task("
        msg2output+="'{var}',".format(var=self.name)
        msg2output+="{var},".format(var=self.start_date)
        msg2output+="{var},".format(var=self.duration)
        msg2output+="{varname}='{var}',".format(varname="description",var=self.description)
        msg2output+="{varname}={var},".format(varname="cost",var=self.cost)
        msg2output+="{varname}={var},".format(varname="structure_level",var=self.structure_level)
        msg2output+="{varname}={var},".format(varname="parent",var=self.parent)
        msg2output+="{varname}={var},".format(varname="childs",var=self.childs)
        msg2output+="{varname}={var},".format(varname="dependencies",var=self.dependencies)
        msg2output+="{varname}={var}".format(varname="end_date",var=self.end_date)   
        msg2output+=")"
        return msg2output
            
    
    # if there are dependencies, the class is automatically changing the start_date if it is smaller than the max(end_date) of the dependencies -> does it make sense?
    #method to promote/demote task level (relation with parent) -> Missing validation
    #method to check if added dependencies are in agreement with the level/parent -> Checked
    #method to validate currency
    # dunder methods missing:
        # __eq__ and similar
        # __lt__ __gt__ and similar
        # __repr__
        # __str__
    


    
if __name__ == "__main__":
    s=Task(
        name="Sim",
        start_date=datetime(2021,1,1),
        duration=timedelta(hours=25))
    s.description="really boring test task"
    
    s2=Task(
        name="Child_Sim_1",
        start_date=datetime(2021,1,1),
        duration=timedelta(hours=50))
    
    
    s3=Task(
        name="Child_Sim_2",
        start_date=datetime(2021,1,1),
        duration=timedelta(hours=50))
    s3.dependencies=[s2]
    s.dependencies=[s2,s3]

    

#     s.duration=timedelta(days=25)
#     print(["duration: ",s.duration])
#     print(["end_date:",s.end_date])
#     s.duration=timedelta(days=1)
#     print(["duration: ",s.duration])
#     print(["end_date:",s.end_date])

  


    
