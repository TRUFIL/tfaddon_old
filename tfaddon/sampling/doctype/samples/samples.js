// Copyright (c) 2017, DGSOL InfoTech and contributors
// For license information, please see license.txt

//frappe.provide("tfaddon");
frappe.ui.form.on('Samples', {
	on_load: function(frm) {
		//frm.events.loc_not_in_list(frm);
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
		frm.set_query("material", function(){
			return {
				"filters": {"material_type": doc.smp_type}
			}
		});
		frm.set_query("smp_equipment", function(){
			return {
				"filters": {"eq_owner": doc.eq_owner}
			}
		});
		frm.set_query("smp_location", function(){
			return {
				"filters": {"loc_owner": doc.eq_owner}
			}
		});
		frm.set_query("equipment", function(){
			return {
				"filters": {"eq_owner": doc.eq_owner}
			}
		});
		frm.set_query("location", function(){
			return {
				"filters": {"loc_owner": doc.eq_owner}
			}
		});
		$.each(frm.doc.containers || [], function(i, d) {
			d.status = frm.doc.status;
		});
		//refresh_field("status");
		if(doc.docstatus == 1) {
			/*if ((doc.collected_by == "Customer" && doc.status == 'Collected') || (doc.collected_by == "TRUFIL" && doc.status == 'Dispatched')) {
				cur_frm.add_custom_button(__('Receive'), cur_frm.cscript['Receive Samples']);
			}*/
			if ((doc.status == 'Collected') || (doc.status == 'Dispatched')) {
				cur_frm.add_custom_button(__('Receive'), cur_frm.cscript['Receive Samples']);
			}
			if (doc.status == 'Completed') {
				cur_frm.add_custom_button(__('Dispose'), cur_frm.cscript['Dispose Samples']);
			}
		} 
		frm.events.required_fields(frm);
	},
	validate: function(frm, cdt, cdn) {

	},
	collected_by: function(frm,cdt,cdn) {
		if(frm.doc.__islocal || frm.doc.docstatus == 0) {
			frm.toggle_reqd("bag_no", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
			frm.toggle_reqd("sampling_request", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
			frm.toggle_reqd("sampler_name", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
			frm.toggle_reqd("sales_order", true);
			if (collected_by == "Customer" && frm.doc.sampler_name) {
				frm.set_value("sampler_name","");
			} 
			if (collected_by == "Customer" && frm.doc.sampling_request) {
				frm.set_value("sampling_request","");
			}
		}
	},
	loc_not_in_list: function(frm) {
		if(frm.doc.__islocal || frm.doc.docstatus == 0) {
			frm.toggle_reqd("loc_area", frm.doc.loc_not_in_list? 1: 0)
			frm.toggle_reqd("loc_location", frm.doc.loc_not_in_list? 1: 0)
			frm.toggle_reqd("loc_cd", frm.doc.loc_not_in_list? 1: 0)
			frm.toggle_reqd("loc_cd", frm.doc.loc_not_in_list? 1: 0)
			frm.toggle_reqd("smp_location", frm.doc.loc_not_in_list? 0: 1);
			if (frm.doc.loc_not_in_list) {
				frm.set_value("smp_location", "");
			}
		}
	},
	smp_location: function(frm) {
		if (frm.doc.smp_location) {
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Locations",
					filters: {"name": frm.doc.smp_location},
				},
				callback: function(res) {
					if (res.message) {
						frm.set_value("loc_area", res.message.area);
						frm.set_value("loc_location", res.message.location);
						frm.set_value("loc_cd", res.message.cd);
						frm.set_value("loc_ccd", res.message.ccd);
						frm.set_value("loc_not_in_list", 0);
						//frm.toggle_enable("smp_location",true);
					} 
				}
			});
		}
	},
	eq_not_in_list: function(frm) {
		if(frm.doc.__islocal || frm.doc.docstatus == 0) {
			frm.toggle_reqd("eq_make", frm.doc.eq_not_in_list? 1: 0)
			frm.toggle_reqd("eq_serial", frm.doc.eq_not_in_list? 1: 0)
			frm.toggle_reqd("eq_rating", frm.doc.eq_not_in_list? 1: 0)
			frm.toggle_reqd("eq_vr", frm.doc.eq_not_in_list? 1: 0)
			frm.toggle_reqd("eq_cr", frm.doc.eq_not_in_list? 1: 0)
			frm.toggle_reqd("eq_no_of_phases", frm.doc.eq_not_in_list? 1: 0)
			frm.toggle_reqd("eq_oil_capacity", frm.doc.eq_not_in_list? 1: 0)
			frm.toggle_reqd("smp_equipment", frm.doc.eq_not_in_list? 0: 1);
			if (frm.doc.eq_not_in_list) {
				frm.set_value("smp_equipment", "");
			}
		}
	},
	smp_equipment: function(frm) {
		if (frm.doc.smp_equipment) {
			//alert("Inside smp_location trigger");
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Equipments",
					filters: {"name": frm.doc.smp_equipment},
				},
				callback: function(res) {
					if (res.message) {
						//console.log(res.message);
						frm.set_value("eq_make", res.message.manufacturer_full_name);
						frm.set_value("eq_serial", res.message.eq_sl_no);
						frm.set_value("eq_rating", res.message.capacity);
						frm.set_value("eq_vr", res.message.voltage);
						frm.set_value("eq_cr", res.message.current);
						frm.set_value("eq_no_of_phases", res.message.eq_phases);
						frm.set_value("eq_oil_capacity", res.message.eq_oil_qty);
						frm.set_value("eq_yom", res.message.eq_yom);
						frm.set_value("owner_eq_id", res.message.owner_eq_id);
						frm.set_value("eq_not_in_list", 0);
					}
				}
			});
		}
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
		$.each(frm.doc.containers || [], function(i, d) {
			//if(!d.sampling_request) d.sampling_request = frm.doc.sampling_request;
			d.sampling_request = frm.doc.sampling_request;
		});
		refresh_field("containers");
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
						frm.set_value("po_no_date", res.message.po_no + " dated " + frappe.datetime.str_to_user(res.message.po_date));
						frm.set_value("so_no_date", res.message.name + " dated " + frappe.datetime.str_to_user(res.message.transaction_date));
						frm.set_value("customer", res.message.customer);
						frm.set_value("eq_owner", res.message.customer);
					}
				}
			});			
		} else {
			frm.set_value("customer", "");
			frm.set_value("po_no_date", "");
			frm.set_value("so_no_date", "");
			frm.set_value("eq_owner", "");
		}
		$.each(frm.doc.containers || [], function(i, d) {
			//if(!d.sales_order) d.sales_order = frm.doc.sales_order;
			d.sales_order = frm.doc.sales_order;
		});
		refresh_field("containers");
	},
	smp_source: function(frm, cdt, cdn) {
		if (frm.doc.smp_source == "Storage") {
			frm.set_value("smp_type", "Transformer Oil");
			frm.set_value("eq_rating", "NA");
			frm.set_value("eq_vr", "NA");
			frm.set_value("eq_cr", "NA");
			frm.set_value("eq_no_of_phases", "NA");
			frm.set_value("eq_ott", "0.00");
			frm.set_value("eq_wtt", "0.00");
			frm.set_value("eq_oil_capacity", "0");
			frm.set_value("eq_load", "0.00");
		} else {
			frm.set_value("smp_type", "");
			frm.set_value("smp_point", "");
			frm.set_value("eq_rating", "");
			frm.set_value("eq_vr", "");
			frm.set_value("eq_cr", "");
			frm.set_value("eq_no_of_phases", "");
			frm.set_value("eq_ott", "");
			frm.set_value("eq_wtt", "");
			frm.set_value("eq_oil_capacity", "");
			frm.set_value("eq_load", "");
		}
		frm.set_value("smp_point", "");
	},
	smp_type: function(frm, cdt, cdn) {
		if (frm.doc.smp_point) {frm.set_value("smp_point", "");}
		if (frm.doc.material) {frm.set_value("material", "");}
	},
	equipment: function(frm, cdt, cdn) {
		if (frm.doc.equipment) {
			frappe.call ({
				'method': 'frappe.client.get',
				'args': {
					'doctype': 'Equipments',
					'name': frm.doc.equipment
				},
				'callback': function(res) {
					console.log(res.message);
					if (res.message) {
						var wrapper = $(frm.fields_dict['eq_details_html'].wrapper);
						wrapper.html(frappe.render(eq_template, {doc: res.message}));
					}
				}
			});
		} else {
			var wrapper = $(frm.fields_dict['eq_details_html'].wrapper);
			wrapper.html(frappe.render(blank_template, {doc: []}));
		}
		frm.refresh_field('eq_details_html');
	},
	location: function(frm, cdt, cdn) {
		if (frm.doc.location) {
			frappe.call ({
				'method': 'frappe.client.get',
				'args': {
					'doctype': 'Locations',
					'name': frm.doc.location
				},
				'callback': function(res) {
					console.log(res.message);
					if (res.message) {
						var wrapper = $(frm.fields_dict['loc_details_html'].wrapper);
						wrapper.html(frappe.render(loc_template, {doc: res.message}));
					}
				}
			});			
		} else {
			var wrapper = $(frm.fields_dict['loc_details_html'].wrapper);
			wrapper.html(frappe.render(blank_template, {doc: []}));
		}
		frm.refresh_field('loc_details_html');
	},
	required_fields: function(frm, cdt, cdn) {
		var sf = ["collection_date","smp_source","smp_type","smp_point","smp_condition",
			"weather_condition","eq_owner","sampler_remarks"];
			
		if (frm.doc.__islocal || frm.doc.docstatus == 0) {
			for (i = 0; i < sf.length; i++) {
				frm.toggle_reqd(sf[i], frm.doc.status == "Draft"? 1: 0);
			}
		}
		frm.events.collected_by(frm);
		frm.events.loc_not_in_list(frm);
		frm.events.eq_not_in_list(frm);
		//frm.events.equipment(frm);
		//frm.events.location(frm);
	},
	bag_no: function(frm, cdt, cdn) {
		$.each(frm.doc.containers || [], function(i, d) {
			//if(!d.bag_no) d.bag_no = frm.doc.bag_no;
			d.bag_no = frm.doc.bag_no;
		});
		refresh_field("containers");
	},
	status: function(frm, cdt, cdn) {
		//$.each(frm.doc.containers || [], function(i, d) {
			//d.status = frm.doc.status;
		//});
		//refresh_field("status");
		frm.refresh();
	},
	eq_owner: function (frm, cdt, cdn) {
		if (frm.doc.smp_location) { frm.set_value("smp_location", ""); }
		if (frm.doc.smp_equipment) { frm.set_value("smp_equipment", ""); }
	}
});

frappe.ui.form.on("Sampling Containers", {
	containers_add: function(frm, cdt, cdn) {
		var row = frappe.get_doc(cdt, cdn);
		if(frm.doc.bag_no) {
			row.bag_no = frm.doc.bag_no;
			refresh_field("bag_no", cdn, "containers");
		}
		if(frm.doc.sampling_request) {
			row.sampling_request = frm.doc.sampling_request;
			refresh_field("sampling_request", cdn, "containers");
		}
		if(frm.doc.sales_order) {
			row.sales_order = frm.doc.sales_order;
			refresh_field("sales_order", cdn, "containers");
		}
		if(frm.doc.status) {
			row.status = frm.doc.status;
			refresh_field("status", cdn, "containers");
		}
	},
	containers_remove: function(frm, cdt, cdn) {
		// Update sample_id
		var bottles = frm.doc.containers;
		sample_id = "";
		for (var i in bottles) {
			if (sample_id != "") {sample_id += "-";}
			sample_id += bottles[i].container_no;
		}
		if (sample_id != "") {
			frm.set_value("sample_id", sample_id);
		}		
	},
	bag_no: function(frm, cdt, cdn) {
		if(!frm.doc.bag_no) {
			erpnext.utils.copy_value_in_all_row(frm.doc, cdt, cdn, "containers", "bag_no");
		}
	},	
	sampling_request: function(frm, cdt, cdn) {
		if(!frm.doc.sampling_request) {
			erpnext.utils.copy_value_in_all_row(frm.doc, cdt, cdn, "containers", "sampling_request");
		}
	},	
	sales_order: function(frm, cdt, cdn) {
		if(!frm.doc.sales_order) {
			erpnext.utils.copy_value_in_all_row(frm.doc, cdt, cdn, "containers", "sales_order");
		}
	},
	status: function(frm, cdt, cdn) {
		if (!frm.doc.status) {
			erpnext.utils.copy_value_in_all_row(frm.doc, cdt, cdn, "containers", "status");
		}
	},
	container_no: function(frm, cdt, cdn) {
		var bottles = frm.doc.containers;
		sample_id = "";
		for (var i in bottles) {
			if (sample_id != "") {sample_id += "-";}
			sample_id += bottles[i].container_no;
		}
		if (sample_id != "") {
			frm.set_value("sample_id", sample_id);
		}		
	}
});

var eq_template = `
	<div class="form-group">
		<div class="col-xs-12">
			<table style="width: 100%; font-size:x-small"><tbody style="padding: 50px; vertical-align: top;">
				<tr><td style="width: 50%;">Owner </td><td>: {{ doc.eq_owner }}</td></tr>
				<tr><td>Owner's Equipment ID </td><td>: {{ doc.owner_eq_id }}</td></tr>
				<tr><td>Equipment Type </td><td>: {{ doc.eq_type }}</td></tr>
				<tr><td>Manufacturer </td><td>: {{ doc.manufacturer_full_name }}</td></tr>
				<tr><td>Manufacturer’s Serial No </td><td>: {{ doc.eq_sl_no }}</td></tr>
				<tr><td>Manufacturing Year </td><td>: {{ doc.eq_yom }}</td></tr>
				<tr><td>Cooling </td><td>: {{ doc.eq_cooling }}</td></tr>
				<tr><td>Voltage Class </td><td>: {{ doc.voltage_class }}</td></tr>
				<tr><td>Rating </td><td>: {{ doc.capacity }}</td></tr>
				<tr><td>Voltage Ratio </td><td>: {{ doc.voltage }}</td></tr>
				<tr><td>Current Ratio </td><td>: {{ doc.current }}</td></tr>
				<tr><td>Phases </td><td>: {{ doc.eq_phases }}</td></tr>
				<tr><td>Insulating Fluid </td><td>: {{ doc.eq_oil_type }} | {{ doc.eq_oil_qty }} kl</td></tr>
			</tbody></table>
		</div> 
	</div>`;

var loc_template = `
	<div class="form-group">
		<div class="col-xs-12">
			<table style="width: 100%; font-size:x-small"><tbody style="padding: 50px; vertical-align: top;">
				<tr><td style="width: 50%;">Owner </td><td>: {{ doc.loc_owner }}</td></tr>
				<tr><td>Owner's Location ID </td><td>: {{ doc.ccd }}</td></tr>
				<tr><td>Installation Location </td><td>: {{ doc.area }} | {{ doc.location }}</td></tr>
				<tr><td>Equipment Designation </td><td>: {{ doc.cd }}</td></tr>
				<tr><td>Installation </td><td>: {{ doc.installation }}</td></tr>
			</tbody></table>
		</div> 
	</div>`;

var blank_template = `
	<div></div>
	`;

cur_frm.cscript['Receive Samples'] = function() {
	var dialog = new frappe.ui.Dialog({
		title: "Receipt Details",
		fields: [
			{"fieldtype": "Date", "label": __("Received Date"), "fieldname": "receipt_date", "reqd": 1 },
			{"fieldtype": "Link", "label": __("Receiving Lab"), "fieldname": "laboratory", "reqd": 1, "options": "Laboratories" },
			{"fieldtype": "Link", "label": __("Material Tested"), "fieldname": "material", "reqd": 1, "options": "Materials" },
			{"fieldtype": "Select", "label": __("Condition on Receipt"), "fieldname": "receipt_condition", "reqd": 1, "options": "OK\nBROKEN\nDISPUTED"},
			{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
	});
	dialog.fields_dict.update.$input.click(function() {
		var args = dialog.get_values();
		//alert(args.act_start_date + " / " + args.act_duration);
		if(!args) return;
		return cur_frm.call({
			method: "declare_received",
			doc: cur_frm.doc,
			args: {receipt_date:args.receipt_date, laboratory:args.laboratory, 
				material:args.material, receipt_condition:args.receipt_condition},
			callback: function(r) {
				if(r.exc) {
					frappe.msgprint(__("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
}

cur_frm.cscript['Dispose Samples'] = function() {
	var dialog = new frappe.ui.Dialog({
		title: "Dispose Details",
		fields: [
			{"fieldtype": "Date", "label": __("Disposed Date"), "fieldname": "disposed_date", "reqd": 1 },
			{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
	});
	dialog.fields_dict.update.$input.click(function() {
		var args = dialog.get_values();
		//alert(args.act_start_date + " / " + args.act_duration);
		if(!args) return;
		return cur_frm.call({
			method: "declare_disposed",
			doc: cur_frm.doc,
			args: {disposed_date:args.disposed_date},
			callback: function(r) {
				if(r.exc) {
					frappe.msgprint(__("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
}