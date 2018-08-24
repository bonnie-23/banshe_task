from pymongo import MongoClient
from bson.objectid import ObjectId




class MongoDB:
    def __init__(self):
        client = MongoClient()
        db = client.db.banshe_events

        self.events = db['event']
        self.todo = db['todo']
        self.reminder = db['reminder']

    def getall(self, tabltype,cond):
        if tabltype == 'event':
            return self.events.find(cond)
        elif tabltype == 'todo':
            return self.todo.find(cond)

    def getrange(self,slice):
        print(slice)
        return slice #self.events.find({})+

    def getonerecord(self,record,rectype):
        if rectype == 'event':
            return self.events.find(record)
        elif rectype == 'todo':
            return self.todo.find(record)

    def update(self, id, modrec, rectype):
        if rectype == 'event':
            self.events.update({"_id": ObjectId(id)},
                               {"$set": modrec})
        elif rectype == 'todo':
            self.todo.update({"_id": ObjectId(id)},
                               {"$set": modrec})

    def deleteevent(self,goalid):
        self.events.remove(goalid)

    def insertrecord(self,rec,rectype):
        if rectype =='event':
            self.events.insert(rec)
        elif rectype == 'todo':
            self.todo.insert(rec)
        elif rectype == 'reminder':
            self.reminder.insert(rec)

    def removerecord(self, rec, rectype):
        if rectype == 'event':
            self.events.remove(rec)
        elif rectype == 'todo':
            self.todo.remove(rec)

    def remove_all_records(self):
        self.reminder.remove({})
        self.events.remove({})
        self.todo.remove({})



if __name__ == "__main__":
    MongoDB()





