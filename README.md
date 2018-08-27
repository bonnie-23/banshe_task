# banshe_task
Banshe Task Manager is a task management application written in Python using a Flask API and storage with Mongo DB. 
Its front end is written in Javascript using freelance template from Start Bootstrap.

------------------------------------------------------------------------------------------------------------------------------------------
With Banshe you can:
------------------------------------------------------------------------------------------------------------------------------------------

See all active and completed goals created in Banshe. 
see a countdown timer of your tasks due today. 
Filter goals due tomorrow, next week or next month.
Create a goal, select its deadline, priority and reminder frequency.
Alert dialogue pops up when deadline arrives where you can delete the goal or mark it as complete, or close to keep the goal and edit deadline later.
Add a todolist for each goal.
Click on a goal to see the todolist needed for achieving it.
Edit each goal and its todolist.
Once goal is done mark as complete. 
Mark completed goal as incomplete and edit.

------------------------------------------------------------------------------------------------------------------------------------------
To install Banshe Task Manager:
------------------------------------------------------------------------------------------------------------------------------------------
Banshe requires an installation of Python and an instance of MongoDB server to run.

1. Install Flask and pymongo modules using pip
2. Start local MongoDB server
3. Start Banshe server by running run.py from python environment
   "py run.py"
4. Launch application from browser on
    "http://127.0.0.1:5000/getallgoals/start"
------------------------------------------------------------------------------------------------------------------------------------------
Features still in development:
------------------------------------------------------------------------------------------------------------------------------------------
Delete todo item
Set reminder frequency and get reminders at specified intervals daily, weekly, monthly until deadline arrives

