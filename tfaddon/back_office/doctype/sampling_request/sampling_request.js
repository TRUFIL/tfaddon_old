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


cur_frm.cscript.show_hide_fields = function(doc) {
	main_fields = ['transaction_date','sales_order','assigned_to','contact_name','contact_no'];
	request_fields = ['est_samples','est_container','req_remarks'];
	response_fields = ['act_samples','act_bottles','response_remarks'];
	if (doc.req_status == 'NEW') {
		hide_field(response_fields);
		toggle_reqd(['assigned_to','contact_name','contact_no','est_samples','est_container'],true);
		toggle_enable(main_fields,false);
		toggle_enable(request_fields,false);
	} else if (doc.req_status == 'ASSIGNED') {
		unhide_field(response_fields);
		toggle_reqd(['act_samples','act_bottles'],true);
		toggle_reqd(['assigned_to','contact_name','contact_no','est_samples','est_container'],false);
		toggle_enable(main_fields,true);
		toggle_enable(request_fields,true);
	} else {
		unhide_field(response_fields);

	}
}