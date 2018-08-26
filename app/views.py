import ast
from datetime import datetime

from app import mongo, app
from bson.objectid import ObjectId
from flask import jsonify, request, render_template, redirect, url_for

from .core import Event



def makeevent(event):
    eventrecord = \
        Event(
            event['event_name'],
            event['event_priority'],
            event['event_status'],
            event['event_deadline'],
            event['event_todolist'],
            event['event_reminder'],
            event['event_createdate'])
    return eventrecord

def makeeventlist(lst,item):
    # print(item['event_todolist'])
    lst.append({'event_name': item['event_name'],
                    'event_priority': item['event_priority'],
                    'event_status': item['event_status'],
                    'event_todolist': item['event_todolist'],
                    'event_reminder': item['event_reminder'],
                    'event_deadline': item['event_deadline'],
                    'event_createdate': item['event_createdate'],
                    'mongo_id': str(item['_id'])

                    })
    return lst

'''
takes html datetime-local and convert to python date
'''
def fixdate(dateval):
    d= dateval.replace('T', ' ')
    return datetime.strptime(d.replace('-','/'),'%Y/%m/%d %H:%M')

'''
converts Javascript bool to Py bool
'''
def getbool(check):
    if check == 'true':
        return True
    else:
        return False

'''
groups active and completed tasks into separate lists
'''
def splitstat(cursor):
    output, active, completed, duetoday = {}, [], [],[]
    today = datetime.today().date()
    for i in cursor:
        deadline = datetime.strptime(i['event_deadline'],'%Y-%m-%d %H:%M:%S')

        if i['event_status']=='False':
            active = makeeventlist(active,i)
            if deadline.date() == today:
                duetoday = makeeventlist(duetoday, i)

        elif i['event_status']=='True':
            completed = makeeventlist(completed, i)


    output['active']= active
    output['completed'] = completed
    output['duetoday'] = duetoday
    return output


'''
Get all events in MongoDb create a dictionary for each record and append to a list
'''
@app.route('/getallgoals/<page>', methods=['GET'])
def get_all_goals(page):

    if page == "start":
        return render_template('index.html', events = splitstat(mongo.getall('event',{})),title='Banshe')
    elif page == "edit":
        return render_template('editgoal.html')

'''
Get events within a range day, week, month using a slice object
'''
@app.route('/getgoalstomorrow', methods=['GET'])
def get_goals_tomorrow():
    output = []
    for i in mongo.getall('event',{}):
        event = makeevent(i)
        slice = event.getslice().day.date()
        deadline = datetime.strptime(i['event_deadline'],'%Y-%m-%d %H:%M:%S').date()

        if  deadline == slice:
            output.append(i)
    return render_template('index.html', events = splitstat(output),title='Banshe')


@app.route('/getgoalsweek', methods=['GET'])
def get_goals_week():
    output = []
    for i in mongo.getall('event',{}):
        event = makeevent(i)
        slice = event.getslice().week
        deadline = datetime.strptime(i['event_deadline'], '%Y-%m-%d %H:%M:%S').date()

        if slice[0].date() <= deadline <= slice[1].date():
            output.append(i)
    return render_template('index.html', events=splitstat(output), title='Banshe')

@app.route('/getgoalsmonth', methods=['GET'])
def get_goals_month():
    output = []
    for i in mongo.getall('event',{}):
        event = makeevent(i)
        slice = event.getslice().month
        deadline = datetime.strptime(i['event_deadline'], '%Y-%m-%d %H:%M:%S').date()

        if slice[0].date() <= deadline <= slice[1].date():
            output.append(i)

    # return jsonify(splitstat(output))
    return render_template('index.html', events=splitstat(output), title='Banshe')


'''
takes goal name and deadline retrieves event from mongoDb
'''
@app.route('/getonegoal', methods = ['POST'])
def get_one_goal():
    output = []
    goal = request.json
    record = mongo.getonerecord({'_id': ObjectId(goal['mongo_id'])},'event')
    for i in record:
        output.append({'event_name': i['event_name'],
                        'event_priority': i['event_priority'],
                        'event_status': i['event_status'],
                        'event_todolist': i['event_todolist'],
                        'event_reminder': i['event_reminder'],
                        'event_deadline': i['event_deadline'],
                        'event_createdate': i['event_createdate'],
                        'mongo_id' : str(i["_id"])
                        })
    return  jsonify(output)



@app.route('/newgoal', methods = ['GET'])
def new_goal():
    return render_template("creategoal.html", title = 'New Goal')
@app.route('/editgoal', methods = ['GET'])
def edit_goal():
    dict= request.args.get('dict')
    return render_template("editgoal.html", dict = ast.literal_eval(dict), title = 'Edit')



'''
gets event object and inserts into MongoDB
'''
@app.route('/insertgoal', methods=['GET','POST'])
def insert_goal():
    eventrecord = makeevent({ 'event_name': request.json['event_name'],
                                   'event_priority': request.json['event_priority'],
                                   'event_status': "False",
                                   'event_deadline': fixdate(request.json['event_deadline']),
                                   'event_todolist': request.json['event_todolist'],
                                   'event_reminder': request.json['event_reminder'],
                                   'event_createdate': datetime.now().replace(second=0,microsecond=0)
                              })
    eventrecord.insert_event()
    return redirect( url_for('get_all_goals',page='start') )



'''
replaces that event in mongodb with event passed from Javascript form
'''
@app.route('/updategoal', methods=['GET','POST'])
def update_goal():
    if request.method == 'POST':
        eventrecord = makeevent({
            'event_name': request.json['event_name'],
             'event_priority': request.json['event_priority'],
             'event_status': "False",
             'event_deadline': fixdate(request.json['event_deadline']),
             'event_todolist': request.json['event_todolist'],
             'event_reminder': request.json['event_reminder'],
             'event_createdate': fixdate(request.json['event_createdate'])
            })
        print( request.json['event_todolist'] )
        eventrecord.update(request.json['mongo_id'], eventrecord)
    return redirect(url_for('get_all_goals', page='start'))


'''
Remove single document from MongoDB
'''
@app.route('/deletegoal', methods=['GET'])
def delete_goal():
    monid = {'_id': ObjectId(ast.literal_eval(request.args.get('dict')))}
    goalrecord = mongo.getonerecord(monid,'event')
    for i in goalrecord:
        mongo.deleteevent(i["_id"])

    return redirect(url_for('get_all_goals', page='start'))
    # return render_template("response.html", insresult ="Goal Deleted!")

'''
Remove all documents
'''
@app.route('/removeall', methods=['GET'])
def remove_all():
    mongo.remove_all_records()
    return 'All Records Removed'


'''
updates status of goal with on provided from Javascript form
'''
@app.route('/togglegoal', methods=['POST'])
def toggle_goal():
    record = mongo.getonerecord({'_id': ObjectId(request.json['mongo_id'])},'event')
    for i in record:
        eventrecord = makeevent(i)
        eventrecord.toggle_event(i['_id'],str(getbool(request.json['event_status'])))
    return redirect(url_for('get_all_goals',page='start'))
