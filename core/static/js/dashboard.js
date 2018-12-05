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
        this.hriks = new Hriks()
        this.container = $('#newtasks')
        this.tasksContainer = $('#tasks')
    }

    getTasks() {
        this.new_tasks = Hriks.send_xml_request("GET", this.new_task_api)[0]
        this.tasks = Hriks.send_xml_request("GET", this.task_api)[0]
        this.renderNewTasks()
        this.renderTasks()
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
            console.log(e)
        } else if (response[1] != 200) {
            console.log(e)
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
                resp += '<tr>'
                resp += '<td style="text-align: left width: 15%">' + row.title.title() + '</td>'
                resp += '<td style="width: 15%">' + row.state.title() + '</td>'
                resp += '<td style="width: 15%">' + row.priority.title() + '</td>'
                resp += '<td style="width: 15%">' + row.creator.title() + '</td>'
                resp += '<td style="width: 15%">' + (
                    row.hasOwnProperty('acceptor') && row.acceptor != null ? row.acceptor.title() : '-') + '</td>'
                resp += '<td style="width: 25%">' + this.getActionButton(row, "all") + '</td>'
                resp += '</tr>'
            }
        }
        this.tasksContainer.html(resp)
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
        Hriks.send_xml_request("POST", this.update_task_api, JSON.stringify(data))        
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