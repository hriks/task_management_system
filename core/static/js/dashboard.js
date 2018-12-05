String.prototype.title = function() {
    if (this == "None" || this == "") {
        return "-"
    }
    var string = this.toLowerCase()
    string = string.replace(/(^|\s)[a-z]/g,function(f){return f.toUpperCase();});
    return string.replace(/_/g, " ").replace(/-/g, " ")
}

class Dashboard {
    constructor() {
        this.task_api = '/task/all'
        this.new_task_api = '/task/new'
        this.create_task_api = '/task/create/'
        this.update_task_api = '/task/update/'
        this.notification_api = '/notifications'
        this.update_notifications_api = '/update/notification?id='
        this.hriks = new Hriks()
        this.container = $('#newtasks')
        this.tasksContainer = $('#tasks')
        this.notificationsContainer = $('#notifications')
    }

    getTasks() {
        this.new_tasks = Hriks.send_xml_request("GET", this.new_task_api)[0]
        this.tasks = Hriks.send_xml_request("GET", this.task_api)[0]
        this.notifications = Hriks.send_xml_request("GET", this.notification_api)[0]
        this.renderNewTasks()
        this.renderTasks()
        this.renderNotifications()
    }

    static socketTasks() {
        return _dash.getTasks()
    }

    static close(id) {
        $('#' + id).hide()
        $('input').val('')
    }

    static openModal(id) {
        $('#' + id).show()
    }

    create() {
        var data = {
            "title": $('#title').val(),
            "description": $('#description').val(),
            "priority": $('#priority').val()
        }
        $('#create').html('<i class="fa fa-circle-o-notch fa-spin"></i> Creating')
        var response = Hriks.send_xml_request("POST", this.create_task_api, JSON.stringify(data))
        if (response == undefined) {
            alert("Something went wrong")
        } else if (![200, 201].includes(response[1])) {
            alert(response[0].message)
        }
        Dashboard.close('id01')
        $('#create').html('Create')
        $('#priority').val("low")
        return false
    }

    renderNewTasks() {
        var resp = ''
        if (this.new_tasks.length == 0) {
            resp += '<tr>'
            resp += '<td colspan="5" class="nr">No New Tasks</td>'
            resp += '</tr>'
        } else {
            for (let index=0; index < this.new_tasks.length; index++) {
                let row = this.new_tasks[index]
                resp += '<tr>'
                resp += '<td style="text-align: left">' + row.title.title() + '</td>'
                resp += '<td>' + row.state.title() + '</td>'
                resp += '<td>' + row.priority.title() + '</td>'
                resp += '<td>' + row.creator.title() + '</td>'
                resp += '<td>' + this.getActionButton(row, "new") + '</td>'
                resp += '</tr>'
            }
        }
        this.container.html(resp)
    }

    renderTasks() {
        var resp = ''
        if (this.tasks.length == 0) {
            resp += '<tr>'
            resp += '<td colspan="6" class="nr">No Tasks Pending</td>'
            resp += '</tr>'
        } else {
            for (let index=0; index < this.tasks.length; index++) {
                let row = this.tasks[index]
                let onclick = OPERATOR_TYPE == 'manager' ? 'onclick=Dashboard.showCaseTask(' + row.id + ')': ''
                resp += '<tr>'
                resp += '<td style="text-align: left width: 15%; cursor:pointer;" ' + onclick + '>' + row.title.title() + '</td>'
                resp += '<td style="width: 15%">' + row.state.title() + '</td>'
                resp += '<td style="width: 15%">' + row.priority.title() + '</td>'
                resp += '<td style="width: 15%">' + row.creator.title() + '</td>'
                resp += '<td style="width: 15%">' + (
                    row.hasOwnProperty('acceptor') && row.acceptor != null ? row.acceptor.title() : '-') + '</td>'
                resp += '<td style="width: 25%">' + this.getActionButton(row, "all") + '</td>'
                resp += '</tr>'
                if (OPERATOR_TYPE === 'manager') {
                    resp += '<tr id="task_info_' + row.id + '" class="task_infos">'
                    resp += '<td colspan="6">'
                    resp == '<div>' + row.description + '</div>'
                    resp += '<div><table class="table standardTable">'
                    resp += '<thead><tr><th>State</th><th>Accepted by</th>'
                    resp += '<th>Created by</th><th>Time</th>'
                    resp += '</tr><tbody>'
                    for (let index=0; index<row.timeline.length; index++) {
                        let timeline = row.timeline[index]
                        resp += '<tr>'
                        resp += '<td>' + timeline.state.title() + '</td>'
                        resp += '<td>' + timeline.accepted_by.title() + '</td>'
                        resp += '<td>' + timeline.created_by.title() + '</td>'
                        resp += '<td>' + timeline.time.title() + '</td>'
                        resp += '</tr>'
                    }
                    resp += '</tbody></table></div></td>'
                    resp += '</tr>'
                }

            }
        }
        this.tasksContainer.html(resp)
    }

    static showCaseTask(row_id) {
        $('.task_infos').not('#task_info_' + row_id).hide()
        $('#task_info_' + row_id).toggle()
    }

    renderNotifications() {
        var resp = ''
        for (let index=0; index < this.notifications.length; index++){
            resp += '<p class="notificationsp">' + (this.notifications[index].message)
            resp += '<span class="readnotifi" onclick="_dash.read('+this.notifications[index].id
            resp += ')"><i class="fa fa-close"></i></span></p>'
        }
        this.notificationsContainer.html(resp)

    }

    getActionButton(row, task_type) {
        if (OPERATOR_TYPE === 'manager') {
            return '<button type="submit" id="cancel" onclick=_dash.cancel(' + row.id + ')>Cancel</button>'
        } else {
            if (task_type === 'new') {
                return '<button type="submit" id="accept" onclick=_dash.accept(' + row.id + ')>Accept</button>'
            } else {
                var resp = '<button type="submit" id="complete" onclick=_dash.complete(' + row.id + ')>Complete</button>'
                resp += '<button type="submit" id="decline" onclick=_dash.decline(' + row.id + ')>Decline</button>'
                return resp
            }
        }
    }

    read(id) {
        Hriks.send_xml_request("POST", this.update_notifications_api + id)
    }

    accept(id) {
        this.update(id, 'accepted')
    }

    complete(id) {
        this.update(id, 'completed')
    }

    decline(id) {
        this.update(id, 'declined')
    }

    cancel(id) {
        this.update(id, 'cancelled')
    }

    update(id, state) {
        var data = {"id": id, "state": state}
        var response = Hriks.send_xml_request("POST", this.update_task_api, JSON.stringify(data))
        if (response[1] == 400) {
            return alert(response[0].message)
        }

    }
}

class Hriks {
    constructor () {
        this.csrftoken = this.getCookie('csrftoken')
        this.set_cookie_ajax()
    }

    csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    set_cookie_ajax() {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!_dash.hriks.csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", _dash.hriks.getCookie('csrftoken'));
                }
            }
        });
    }

    getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    static send_xml_request(method, api, data={}, sync=false, callback=null) {
        try {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( method, api, sync );
            if (callback != null && sync === true) {
                xmlHttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        callback()
                    }
                };
            }
            xmlHttp.setRequestHeader('X-CSRFToken', _dash.hriks.csrftoken)
            xmlHttp.setRequestHeader('Accept', 'application/json')
            xmlHttp.setRequestHeader('Content-Type', 'application/json')
            xmlHttp.send( data );
            return [JSON.parse(xmlHttp.responseText), xmlHttp.status]
        } catch(e) {
            alert('Something went wrong! Please Try Again')
            console.log(e)
        }
    }

}