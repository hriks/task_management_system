class Dashboard {
	constructor() {
		this.task_api = '/task/all'
		this.new_task_api = '/task/new'
		this.create_task_api = '/task/create/'
		this.update_task_api = '/task/update/'
	}

	static close(id) {
		$('#' + id).hide()
		$('input').val('')
		$('select').val('')
	}

	static openModal(id) {
		$('#' + id).show()
	}
}