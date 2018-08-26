# banshe_task
Banshe Task Manager is a task management application written in Python using a Flask API and storage with Mongo DB. 
Its fronteend is written in Javascript using freelance template from Start Bootstrap.

------------------------------------------------------------------------------------------------------------------------------------------
With Banshe you can:
------------------------------------------------------------------------------------------------------------------------------------------

See all active and completed goals created in Banshe. 
see a countdown timer of your tasks due today 
Filter goals due tomorrow, next week or next month
Create a goal, select its deadline, priority and reminder frequency.
Add a todolist for each goal
Click on a goal to see the todolist needed for achieving it
edit each goal and the 

------------------------------------------------------------------------------------------------------------------------------------------
To install Banshe Task Manager:
------------------------------------------------------------------------------------------------------------------------------------------
Banshe requires an installation of Python and an instance of MongoDB server to run.

1. Install Flask and pymongo modules using pip
2. Start local MongoDB server
3. Start Banshe server by running r.py from python environment
   "py run.py"
4. Launch application from browser on
    "http://127.0.0.1:5000/getallgoals/start"
------------------------------------------------------------------------------------------------------------------------------------------
Features still in development:
------------------------------------------------------------------------------------------------------------------------------------------
Delete todo item
mark completed goal as incomplete
Set reminder frequency and get reminders at specified intervals daily, weekly, monthly until deadline arrives
Display bage with count of todo items for each goal
