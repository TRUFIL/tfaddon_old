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
		frm.set_query("material", function(){
			return {
				"filters": {"material_type": doc.smp_type}
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
		frm.events.required_fields(frm);
	},
	validate: function(frm, cdt, cdn) {

	},
	collected_by: function(frm,cdt,cdn) {
		frm.toggle_enable("bag_no", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
		//frm.toggle_reqd("bag_no", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
		frm.toggle_reqd("sampling_request", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
		frm.toggle_reqd("sampler_name", (frm.doc.collected_by == "TRUFIL") ? 1 : 0);
		frm.toggle_reqd("sales_order", true);//(frm.doc.collected_by == "Customer") ? 1 : 0);
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
	},
	smp_source: function(frm, cdt, cdn) {
		/*if (frm.doc.smp_source == "Storage") {
			frm.set_value("smp_type", "Transformer Oil");
			frm.set_value("voltage_class", "NA");
			frm.set_value("eq_rating", "NA");
			frm.set_value("eq_vr", "NA");
			frm.set_value("eq_cr", "NA");
			frm.set_value("eq_no_of_phases", "NA");
			frm.set_value("eq_ott", "0.00");
			frm.set_value("eq_wtt", "0.00");
			frm.set_value("eq_oil_capacity", "0");
			frm.set_value("eq_load", "NA");
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
		}*/
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
					if (res.message) {
						//alert(JSON.stringify(res.message, null, 4));
						var wrapper = $(frm.fields_dict['eq_details_html'].wrapper);
						wrapper.html(frappe.render(eq_template, {doc: res.message}));
						//frm.set_df_property('eq_details_html', 'options', frappe.render(eq_template, {eq: res.message}));
						//frm.refresh_field('eq_details_html');
					}
				}
			});
		} else {
			var wrapper = $(frm.fields_dict['loc_details_html'].wrapper);
			wrapper.html(frappe.render(blank_template, {doc: res.message}));
			//frm.set_df_property('eq_details_html', 'options', frappe.render(eq_template, {eq: res.message}));
		}
		frm.refresh_field('loc_details_html');
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
					if (res.message) {
						//alert(JSON.stringify(res.message, null, 4));
						var wrapper = $(frm.fields_dict['loc_details_html'].wrapper);
						wrapper.html(frappe.render(loc_template, {doc: res.message}));
						//frm.set_df_property('eq_details_html', 'options', frappe.render(eq_template, {eq: res.message}));
						//frm.refresh_field('loc_details_html');
					}
				}
			});			
		} else {
			var wrapper = $(frm.fields_dict['loc_details_html'].wrapper);
			wrapper.html(frappe.render(blank_template, {doc: res.message}));
			//frm.set_df_property('eq_details_html', 'options', frappe.render(eq_template, {eq: res.message}));
		}
		frm.refresh_field('loc_details_html');
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
		} else if (frm.doc.docstatus == 0) {
			frm.toggle_reqd("collected_by", true);
			frm.toggle_reqd("collection_date", true);
			frm.toggle_reqd("smp_source", true);
			frm.toggle_reqd("smp_type", true);
			frm.toggle_reqd("smp_point", true);
			frm.toggle_reqd("smp_condition", true);
			frm.toggle_reqd("eq_owner", true);
			frm.toggle_reqd("weather_condition", true);
			frm.toggle_reqd("receipt_date", true);
			frm.toggle_reqd("laboratory", true);
			frm.toggle_reqd("material", true);
			frm.toggle_reqd("sample_condition", true);
			frm.toggle_reqd("equipment", true);
			frm.toggle_reqd("location", true);
		}
		frm.events.collected_by(frm);
		frm.events.equipment(frm);
		frm.events.location(frm);
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
