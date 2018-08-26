from datetime import datetime, timedelta
from .mongo import MongoDB
from bson.objectid import ObjectId




mongo = MongoDB()

''' 
base object for banshe events
'''
class Event(object):
    def __init__(self, event_name,
                    event_priority,
                    event_status,
                    event_deadline,
                    event_todo,
                    event_reminder,
                    event_createdate):

        self.name = event_name
        self.priority = event_priority
        self.todolist = event_todo
        self.status = event_status
        self.reminder = event_reminder
        try:
            self.deadline = datetime.strptime(event_deadline,'%Y-%m-%d').date()
            self.createdate = datetime.strptime(event_createdate, '%Y-%m-%d').date()
        except:
            self.deadline = event_deadline
            self.createdate = event_createdate


    '''
    update event status with stat from server
    '''
    def toggle_event(self, goalid, check):
        self.status = check
        #Toggle().toggle(self.status)
        self.update(goalid,self)
        #return self.status

    '''
    insert new event to MongoDB
    '''
    def insert_event(self):

        if self.name == "":
            return "Please enter Event Name"
        elif self.deadline < datetime.now() or self.deadline == "" :
            return "Please select a future deadline"
        else:
            doc = {
                'event_name': self.name,
                'event_priority': self.priority,
                'event_todolist': self.todolist,
                'event_status': self.status,
                'event_reminder': self.reminder,
                'event_deadline': str(self.deadline),
                'event_createdate': str(self.createdate)
            }
            mongo.insertrecord(doc,'event')
        return "Event was inserted"

    '''
    get a date slice object to manipulate date parts
    '''
    def getslice(self):
        return DateSlice(self)


    '''
    replaces event in MongoDB with modified event 
    '''
    def update(self,goalid, newgoal):
        try:
            modgoal ={
                'event_name': newgoal.name,
                'event_priority': newgoal.priority,
                'event_status': newgoal.status,
                'event_todolist': self.todolist,
                'event_reminder': newgoal.reminder,
                'event_deadline': str(newgoal.deadline)}
            mongo.update(goalid,modgoal,'event')
            return 'Record updated'
        except:
            return 'Something went wrong'

    '''
    attaches a todo item to event todolist
    '''
    def add_todo(self, goalid, name, status):
        todo = Todo(goalid, name, status)
        todo.save_todo()
        self.attach_todo(goalid)

    def get_todolist(self,goalid):
        todolist = []
        mongo_todolist = mongo.getonerecord({'goal_id': ObjectId(goalid)}, 'todo')
        for i in mongo_todolist:
            todolist.append({'todo_id': str(i['_id']),
                             'goal_id': str(i['goal_id']),
                             'todo_name': i['todo_name'],
                             'todo_status': i['todo_status']
                             })
        return todolist

    def attach_todo(self,goalid):
        self.todolist = self.get_todolist(goalid)
        self.update(goalid,self)



class Timer(object):
    def __init__(self, event):
        self. created_time = event.createdate
        self.deadline = datetime.strptime(event.deadline,'%Y-%m-%d %H:%M:%S')
        self.now = datetime.now()

    def get_elapsed_time(self):
        elap_time = self.now - self.created_time
        return elap_time.days
    def get_rem_time(self):
        remtime = self.deadline - self.now
        return remtime.days


class DateSlice(Timer):
    def __init__(self,event):
        Timer.__init__(self,event)
        self.day = self.now + timedelta(days = 1)
        self.week = [self.now,self.now + timedelta(days = 7)]
        self.month = [self.now,self.now + timedelta(days= 30)]


class Toggle(object):
    def toggle(self, event):
        return True if event == False else False





'''
Todo Objects
---------------------------------------------------------------------------------------
'''

'''todo object'''
class Todo(object):
    def __init__(self, goalid, name, status):
        self.goalid = goalid
        self.name = name
        self.status = status

        self.todorecord = {
            'goal_id': self.goalid,
            'todo_name': self.name,
            'todo_status': self.status
        }

    def save_todo(self):
       return mongo.insertrecord(self.todorecord, 'todo')

    def update(self, todoid):
        return mongo.update(todoid,self.todorecord,'todo')
    def update_record(self):
        self.todorecord['goal_id'] = self.goalid
        self.todorecord['todo_name'] = self.name
        self.todorecord['todo_status'] = self.status

    def toggle_todo(self,todoid):
        self.status = Toggle().toggle(self.status)
        self.update_record()
        self.update(todoid)
        return self.status

class Task(object):
    def __init__(self, name):
        self.name = name
        self.status = False

    def toggle_task(self):
        self.status = Toggle().toggle(self.status)


class Reminder(object):
    reminder_registry = []

    def __init__(self, timer, rem_type):
        self.timer = timer
        self.rem_type = rem_type
        #Reminder.reminder_registry.append(self)#[self.timer,self.rem_type])
        #print(Reminder.reminder_registry)

    def nextreminder(self, date):
        if self.rem_type == 'Daily':
            nextrem = date + timedelta(days=1)
            return nextrem
        if self.rem_type == 'Weekly':
            nextrem = date + timedelta(weeks=1)
            return nextrem
        if self.rem_type == 'Monthly':
            nextrem = datetime(date.year, date.month+1,date.day)
            return nextrem


    def attach_rem(self):
        Reminder.reminder_registry.append(self)



    def check_rem_registry(self):
        pass
    def notify(self):
        pass




class EventPriority(object):
    def __init__(self, name):
        self.priority_name = name
        







if __name__== '__main__':
    a=Reminder(Timer(Event()), 'Daily')