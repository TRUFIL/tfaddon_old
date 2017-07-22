// Copyright (c) 2017, DGSOL InfoTech and contributors
// For license information, please see license.txt

var assignment_fields = ['assigned_to','req_remarks']
var response_fields = ['act_samples','act_bottles','response_remarks'];

frappe.ui.form.on('Sampling Request', {
	refresh: function(frm) {
		//cur_frm.cscript.show_hide_fields(frm.doc)
	},
	req_status: function(frm) {
		/*
		if (frm.doc.req_status == 'New') {
			hide_field(assignment_fields);
			hide_field(response_fields);
		} 

		if (frm.doc.req_status == 'Assigned') {
			unhide_field(assignment_fields);
			hide_field(response_fields);
		} 

		if (frm.doc.req_status == 'Closed') {
			unhide_field(assignment_fields);
			unhide_field(response_fields);
		}
		*/
	}
});


