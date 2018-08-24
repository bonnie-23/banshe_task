//
//const {app, BrowserWindow, Menu} = require('electron')
//const path = require('path')
//const url = require('url')
//const shell = require('electron').shell
//const $ = require('jquery')
//
//
//
//let mainWindow
//function createWindow () {
//  mainWindow = new BrowserWindow({width: 450, height: 700})
//  mainWindow.setMenu(null)
//  mainWindow.loadURL('http://127.0.0.1:5000/getallgoals/start')
//  mainWindow.on('closed', function () {
//    mainWindow = null
//  })
//
//mainWindow.loadURL('/index.html')
//mainWindow.webContents.openDevTools()
//}




function addNew() {
    location.href = '/newgoal'
}


function newGoal() {

    $("#editdiag").dialog({
        autoOpen: true,
        resizable: false,
        title: "Add New Goal",
        modal: true,
        width: 400,
        height:350,
        open: function () {
            var insform = document.getElementById("editdiag");
            insform.style.visibility = "visible";
            insform.style.display = "block";

            var tomoro = moment().add(1,'days')
            $("#edit_eventdeadline").val(tomoro.toJSON().slice(0,16))
//            console.log(tom.toString().slice(0,21))

        },
        buttons: {
                    "save": function () {
                        var events = $("#events").data("events");
                        var temp =JSON.parse(events.replace(/\'/g,'\"'))
                        var active_events = temp['active']

                        for (i in active_events){
                            if (active_events[i]['event_name'] ==  $("#edit_eventname").val()){
                                alert("That event already exists")
                            }

                        }
                        saveGoal("save");
                    },
                    "cancel": function () {
                        $(this).dialog("close");
                        getAll()
                    },
                    "clear": function () {
                        clearForm("goal");
                    }

        }
    });
}



function newTodo(){
    var todo = document.getElementById("todoentry");
    todo.style.visibility = "visible";

    var addbtn = document.getElementById("addtodo");
    addbtn.style.visibility = "hidden";
}

function saveTodo() {
    var todolist = []

    if ($("#todo").val()!=''){
        todolist.push($("#todo").val())
        $("#todolist").append(
            $('<li value =' +$("#todo").val()+' >').html($("#todo").val())
        )

        $("#todo").val('')
    }

}

//Select an event in active or completed lists
function markComp(event) {
    //mark selected goal as complete
    $("input.check").change( function() {
        if($(this).is(':checked')){
            event['event_status'] = JSON.stringify($(this).is(':checked'));
            checkGoal(event);
        }
    });
}

function editGoal(event) {
    //edit active selected goal
    deadline = new Date(event['event_deadline'] + " UTC")


    var fmt = 'YYYY-MM-DDTHH:mm'
    var editdeadline = event['event_deadline']
    var dead = moment.utc(event['event_deadline'],fmt)

    var create = moment.utc(event['event_createdate'],fmt)
    var date = new Date()

    $("#editdiag").dialog({
        autoOpen: true,
        resizable: false,
        modal: true,
        width: 400,
        height:350,
        open: function () {
             var form = document.getElementById("editdiag");
             form.style.visibility = "visible";
             $('#edit_eventname').val(event['event_name']);
             $('#edit_eventdeadline').val(dead.format(fmt));
             $('#edit_eventpriority').val(event['event_priority']);
             $('#edit_eventreminder').val(event['event_reminder']);
             $('#eventcreate').val(create.format(fmt));
             $('#mongid').val(event['mongo_id']);

        },
        close: getAll,
        buttons: {
            "save": function () {
                saveGoal("edit");
                getAll();
            },
            "cancel": function () {
                $(this).dialog("close");
            }
        }
    });
}





function deleteGoal(event) {
    //confirm delete dialog
    $(function() {
        $( '<div>' ).dialog({
            autoOpen: true,
            resizable: false,
            height: "auto",
            title: 'Confirm Delete',
            modal: true,
            buttons: {
                        "Delete": function() {
                          location.href = "/deletegoal?dict=" + JSON.stringify(event['mongo_id']);
                        },
                        Cancel: function() {
                          $( this ).dialog( "close" );
                        }
            }

        });
    });
}


//commit changes to goal
function saveGoal(action,todolist) {
    var name = document.getElementById("edit_eventname").value
    var deadline = document.getElementById("edit_eventdeadline").value
    var todolist = getTodolist()
    var priority = document.getElementById("edit_eventpriority").value
    var reminder = document.getElementById("edit_eventreminder").value
    var create = document.getElementById("eventcreate").value
    var monid = document.getElementById("mongid").value

    var dict = {}
    var currentdate = new Date().setSeconds(0,0)


    console.log(todolist[0])
    if(name == "" || deadline == ""){
            alert("blank values")
        }
    else if (new Date(deadline) <= new Date(currentdate)){
        alert("select future date and time")
    }
    else {
        if (action=="edit") {
            dict['event_name'] = name
            dict['event_deadline'] = deadline
            dict['event_priority'] = priority
            dict['event_reminder'] = reminder
            dict['mongo_id'] = monid
            dict['event_createdate'] = create

            $.ajax({
                url: "/updategoal",
                type: "POST",
                contentType: "application/json;charset=UTF-8",
                dataType: "JSON",
                data: JSON.stringify(dict)
            });
        }
        else if (action=="save") {

            dict['event_name'] = name
            dict['event_deadline'] = deadline
//            dict['event_todolist'] = todolist
            dict['event_priority'] = priority
            dict['event_reminder'] = reminder

            $.ajax({
                  url: "/insertgoal",
                  type: "POST",
                  contentType: "application/json;charset=UTF-8",
                  dataType: "JSON",
                  data: JSON.stringify(dict),
                  success: function(data){
                    alert(data);
                  }
            });

        }
        getAll();
    }

    function getTodolist() {

        var todolist = [];
        $('#todolist li').each(function(){
            todolist.push($(this).attr('value'));
        });
        return todolist
    }
}



//Mark a goal as complete
function checkGoal(dict){

    chck = document.getElementById("chckHead")
    dict["event_status"]= JSON.stringify(true)

    $.ajax({
          url: "/togglegoal",
          type: "POST",
          contentType: "application/json;charset=UTF-8",
          dataType: "JSON",
          data: JSON.stringify(dict),
          success: function() {

          }
        });
    window.location.reload();
}

//filter displayed goals by period
function filterGoals () {
    var period = $("input:radio[name='filter']:checked").val()
    if (period == "tomorrow"){
        location.href = "/getgoalstomorrow";
        }
    else if (period == "this week"){
        location.href = "/getgoalsweek";
    }
    else if (period == "this month"){
        location.href = "/getgoalsmonth";
    }
}

function getAll() {
    location.href = "/getallgoals/start";
}



//clear form contents
function clearForm(formname) {

    if (formname == "goal"){
        try {
            document.getElementById('edit_eventname').value = ''
            document.getElementById('edit_eventdeadline').value =  ''
            document.getElementById('edit_eventpriority').value = 'Priority'
            document.getElementById('edit_eventreminder').value = 'Remind Me'
        }
        catch(err) {

        }

    }
}



//check every 60 seconds if deadline for goals have arrived
function loadPage() {

    //Hide Edit Form
    var editform = document.getElementById("editdiag");
    editform.style.visibility = "hidden";
    editform.style.display ="none";


    //Hide today list
    var todaylist = document.getElementById("duetodaydiag")
    todaylist.style.visibility = "hidden";
    todaylist.style.display ="none";


    //Hide todoentry
    var todoentry = document.getElementById("todoentry");
    todoentry.style.visibility = "hidden";


    //Get events from MongoDB
    var events = $("#basepage").data("events");
    var temp =JSON.parse(events.replace(/\'/g,'\"'))
    var today_events = temp['duetoday']
    var active_events = temp['active']

    //check for reminders
//    remFrequency();

    //call countdown dialog only once
    $("#events").one('click', function () {
        countToday();
    });


    //Display dialog for goals countdown
    function countToday(){
        if (today_events.length>0){
            $('<ul id="newDialogText"></ul>').dialog({
                autoOpen: true,
                resizable: false,
                height: "auto",
                title: 'due today',
                modal: true,
                open: function () {

                   for(i=0; i < today_events.length; i++) {
                        $("#newDialogText").append(
                            countdownTimer(today_events[i]['event_name'],today_events[i]['event_deadline'])
                        )
                    }
                }
            });
        }
    }


    //countdown timer to deadline W3Schools
    function countdownTimer(eventname,deadline){
        var countDownDate = new Date(deadline).getTime();
        var new_id = Math.floor((Math.random() * 999) + 1)
        return $('<li id=_' +new_id+'>').append (
            count()
        )


        function count() {
            var x = setInterval(function() {
                var now = new Date().getTime();
                var distance = countDownDate - now;

                    if (distance > 0) {
                        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

                        $('#_' + new_id).html(eventname + ": " + hours + "h " + minutes + "m " + seconds + "s ")

                    }
                    else {
                        $('#_' + new_id).html(eventname + ": EXPIRED")
                    }
            }, 1000);
        };
    }



    //Check each goal every 60s to see if deadline has arrived
    var intervalID = setInterval(getDue,60000);
    function getDue() {

        //check for events with deadline today
        var i;
        for(i=0; i < today_events.length; i++){
            var deadline = today_events[i]["event_deadline"]

            if ( deadline == getToday()){
                goal=today_events[i]

                name= goal["event_name"]
                mongo_id= goal["mongo_id"]
                showNotification(name,'Expired Deadline')


            }
        }

    }

    //Build string of todays date time YYYY-MM-DD HH:SS
    function getToday() {
        var currentdate = new Date()
        var today = currentdate.getFullYear() + "-" +
        (pad(currentdate.getMonth()+1)) + "-" +
        pad(currentdate.getDate()) + " " +
        pad(currentdate.getHours()) + ":" +
        pad(currentdate.getMinutes()) + ":" +
        "00"


        function pad(n, width=2, z=0) {
          z = z || '0';
          n = n + '';
          while(n.length<width) n = '' + z + n;
          return n
        }
        return  today
    };


    function stopCheck() {
        clearInterval(intervalID)
    };



    //show notification based on reminder frequency
    function remFrequency() {

        function freq(period) {
            return 1000 * 60 * 60 * period;
        }

        for(i=0; i < active_events.length; i++){
            name = active_events[i]['event_name']
            deadline = active_events[i]['event_deadline']

            this.$description = $( '<p></p>' );
            message = '<strong>' +name+ '</strong>' + ' is due on: <br/>' + deadline

            while (deadline!=getToday()){
                if (active_events[i]['event_reminder']=='daily') {
                    clearIntervals()
                    trackIntervals(setInterval(function () {
                        stopCheck()
                        showNotification( message,'Reminder')

                    },freq(24)))

                }
                else if (active_events[i]['event_reminder']=='weekly') {
//                    setInterval(function () {
//                        showNotification( message,'Reminder')
//
//                    },freq(24*7))
                }
                else if (active_events[i]['event_reminder']=='monthly') {
//                    setInterval(function () {
//                        showNotification( message,'Reminder')
//
//                    },freq(24*30))
                }

            }
        }
    }
}


//display notification
function showNotification(name,message) {

    clone = $('<div>').clone(true);

    $(clone).dialog({
        autoOpen: true,
        resizable: false,
        height: "auto",
        title: message,
        modal: true,
        open: function () {
            $(this).html(name);
        },
        buttons: {

                    "Delete": function() {
                        deleteGoal(mongo_id);
                    },
                    "Mark Complete": function() {
                        checkGoal(goal);

                    }

        }
    });
}




//app.on('ready', createWindow)
//app.on('activate', function () {
//  if (mainWindow === null) {
//    createWindow()
//  }
//})