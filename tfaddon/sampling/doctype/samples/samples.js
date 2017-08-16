// Copyright (c) 2017, DGSOL InfoTech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Samples', {
	on_load: function(frm) {
		frm.events.required_fields(frm);
	},
	refresh: function(frm) {
		var doc = frm.doc;
		frm.set_query("sampling_request", function(){
			return {
				"filters": {"workflow_state": "In Process", "docstatus": 1, "assigned_to": doc.sampler_name}
			}
		});
		frm.set_query("smp_point", function(){
			return {
				"filters": {"sampling_source": doc.smp_source, "sample_type": doc.smp_type}
			}
		});
		frm.events.required_fields(frm);
	},
	validate: function(frm, cdt, cdn) {

	},
	collected_by: function(frm,cdt,cdn) {
		frm.toggle_reqd("bag_no", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
		frm.toggle_reqd("sampling_request", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
		frm.toggle_reqd("sampler_name", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
		frm.toggle_reqd("sales_order", (frm.doc.collected_by == "Customer") ? 1 : 0);
	},
	sampling_request: function(frm, cdt, cdn) {
		//frm.add_fetch('sampling_request', 'sales_order', 'sales_order');
		if (frm.doc.sampling_request) {
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Sampling Request",
					filters: {"name": frm.doc.sampling_request},
				},
				callback: function(res) {
					if (res.message) {
						frm.set_value("sales_order", res.message.sales_order);
						frm.toggle_enable("sales_order",false);
					}
				}
			});
		} else {
			frm.set_value("sales_order", "");
			frm.toggle_enable("sales_order",true);
		}
	},
	sales_order: function(frm, cdt, cdn) {
		//frm.add_fetch('sales_order', 'po_no', 'po_no');
		//frm.add_fetch('sales_order', 'po_date', 'po_date');
		//alert("Sales Order: "+frm.doc.sales_order+'\n'+"Po No: "+frm.doc.po_no+"\n"+"PO Date: 0"+frm.doc.po_date);
		if (frm.doc.sales_order) {
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Sales Order",
					name: frm.doc.sales_order,
				},
				callback: function(res) {
					if (res.message) {
						frm.set_value("po_no", res.message.po_no);
						frm.set_value("po_date", res.message.po_date);
					}
				}
			});			
		} else {
			frm.set_value("po_no", "");
			frm.set_value("po_date", "");
		}
	},
	smp_type: function(frm, cdt, cdn) {
		frm.set_value("smp_point", "");
	},
	smp_source: function(frm, cdt, cdn) {
		if (frm.doc.smp_source == "Storage") {
			frm.set_value("smp_type", "Transformer Oil");
			frm.set_value("voltage_class", "Not Applicable");
			frm.set_value("eq_rating", "Not Applicable");
			frm.set_value("eq_vr", "Not Applicable");
			frm.set_value("eq_cr", "Not Applicable");
			frm.set_value("eq_no_of_phases", "Not Applicable");
			frm.set_value("eq_ott", "0.00");
			frm.set_value("eq_wtt", "0.00");
			frm.set_value("eq_oil_capacity", "0");
			frm.set_value("eq_load", "Not Applicable");
		} else {
			frm.set_value("smp_type", "");
			frm.set_value("smp_point", "");
			frm.set_value("voltage_class", "");
			frm.set_value("eq_rating", "");
			frm.set_value("eq_vr", "");
			frm.set_value("eq_cr", "");
			frm.set_value("eq_no_of_phases", "");
			frm.set_value("eq_ott", "");
			frm.set_value("eq_wtt", "");
			frm.set_value("eq_oil_capacity", "");
			frm.set_value("eq_load", "");
		}
	},
	required_fields: function(frm, cdt, cdn) {
		if (frm.doc.__islocal) {
			frm.toggle_reqd("collected_by", true);
			frm.toggle_reqd("collection_date", true);
			frm.toggle_reqd("smp_source", true);
			frm.toggle_reqd("smp_type", true);
			frm.toggle_reqd("smp_point", true);
			frm.toggle_reqd("smp_condition", true);
			frm.toggle_reqd("weather_condition", true);
			frm.toggle_reqd("eq_owner", true);
		}
		frm.events.collected_by(frm);
	}

});

