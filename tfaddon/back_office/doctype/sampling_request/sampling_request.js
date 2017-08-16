// Copyright (c) 2017, DGSOL InfoTech and contributors
// For license information, please see license.txt

//var doc=frm.doc;
var assignment_fields = ['assigned_to','req_remarks']
var response_fields = ['act_samples','act_bottles','response_remarks'];

frappe.ui.form.on('Sampling Request', {
	onload: function(frm) {
		frm.events.required_fields(frm);
	},
	refresh: function(frm) {
		frm.events.required_fields(frm);
		//cur_frm.cscript.show_hide_fields(frm.doc)
	},
	validate: function(frm, cdt, cdn) {
		if (frm.doc.docstatus == 1 && frm.doc.workflow_state == "In Process") {
			if (frm.doc.act_duration == 0) {
				alert("Activity Duration cannot be 0");
				frappe.validated = false;
			} 
		}
	},
	required_fields: function(frm, cdt, cdn) {
		var doc=frm.doc;
		var before_save = ((doc.__islocal) && (doc.workflow_state == "Draft")) ? 1 : 0;
		var before_assign = ((doc.docstatus === 0) && (doc.workflow_state == "To Assign")) ? 1 : 0;
		var doc_assigned = ((doc.docstatus === 1) && (doc.workflow_state == "In Process")) ? 1 : 0;
		var doc_closed = ((doc.docstatus === 1) && (doc.workflow_state == "Closed")) ? 1 : 0;
		var doc_cancelled = ((doc.docstatus === 2) && (doc.workflow_state == "Cancelled")) ? 1 : 0;
		alert("before_save: " + before_save + "\n" + "before_assign: " + before_assign + "\n" + "doc_assigned: " + doc_assigned + "\n" + "doc_closed: " + doc_closed + "\n" + "doc_cancelled: " + doc_cancelled + "\n");

		if (doc_closed || doc_cancelled) {
			frm.toggle_enable("closer_date", false);
			frm.toggle_enable("act_start_date", false);
			frm.toggle_enable("act_duration", false);
			frm.toggle_enable("act_samples", false);
			frm.toggle_enable("act_containers", false);
			frm.toggle_enable("response_remarks", false);
		} else {
			frm.toggle_reqd("est_start_date", before_save);
			frm.toggle_reqd("est_duration", before_save);
			frm.toggle_reqd("site_location", before_save);
			frm.toggle_reqd("est_samples", before_save);
			frm.toggle_reqd("est_containers", before_save);
			frm.toggle_reqd("contact_name", before_assign);
			frm.toggle_reqd("contact_no", before_assign);
			frm.toggle_reqd("assigned_to", before_assign);
			frm.toggle_reqd("req_remarks", before_assign);
			frm.toggle_reqd("closer_date", doc_assigned);
			frm.toggle_reqd("act_start_date", doc_assigned);
			frm.toggle_reqd("act_duration", doc_assigned);
			frm.toggle_reqd("act_samples", doc_assigned);
			frm.toggle_reqd("act_containers", doc_assigned);
			frm.toggle_reqd("response_remarks", doc_assigned);
		}
	},
	update_status: function(frm) {
		var doc = frm.doc;
		if (doc.__islocal) {frm.set_value("document_state", "Draft");}

		if (doc.docstatus === 0) {
			if(doc.est_start_date && doc.est_duration > 0 && doc.site_location && doc.est_samples >0 && doc.est_containers >= doc.est_samples) {frm.set_value("document_state", "To Assign");}
		}
		if (doc.docstatus === 1) {
			if(doc.assigned_to && doc.contact_name && doc.contact_no && doc.req_remarks && ) {frm.set_value("document_state", "In Process");}
		}
	}
});


