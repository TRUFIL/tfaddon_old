// Copyright (c) 2017, DGSOL InfoTech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sample Transport Details', {
	refresh: function(frm) {
		if (frm.doc.workflow_state == 'Draft' || frm.doc.__islocal) {
			frm.toggle_enable(["dispatch_date","destination_lab","dispatch_mode","sender_name","dispatch_ref","exp_delivery_date","customer_sender_name","sender_remark"], true);
			frm.toggle_reqd(["dispatch_date","destination_lab","dispatch_mode","sender_name"], true);
		} else if (frm.doc.workflow_state == 'Dispatched') {
			frm.toggle_enable(["dispatch_date","destination_lab","dispatch_mode","sender_name","dispatch_ref","exp_delivery_date","customer_sender_name","sender_remark"], false);
			frm.toggle_enable(["received_date","receiving_lab","receiver_name", "receiver_remarks"], true);
			frm.toggle_reqd(["received_date","receiving_lab"], true);
		} else if (frm.doc.workflow_state == 'Received') {
			frm.toggle_enable(["dispatch_date","destination_lab","dispatch_mode","sender_name","dispatch_ref","exp_delivery_date","customer_sender_name","sender_remark"], false);
			frm.toggle_enable(["received_date","receiving_lab","receiver_name", "receiver_remarks"], false);
		}
	},

	dispatch_mode: function(frm) {
		if (frm.doc.dispatch_mode == "By Courier" || frm.doc.dispatch_mode == "By Booking" ) {
			frm.toggle_reqd("dispatch_ref", true);
		} else {
			frm.toggle_reqd("dispatch_ref", false);			
		}
	},

	sender_name: function(frm) {
		if (frm.doc.sender_name == "Customer") {
			frm.toggle_reqd("customer_sender_name", true);
		} else {
			frm.toggle_reqd("customer_sender_name", false);
		} 
	},
	
});
