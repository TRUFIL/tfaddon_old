// Copyright (c) 2017, DGSOL InfoTech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Oil Test Reports', {
	refresh: function(frm) {
		var doc = frm.doc;
		frm.set_query("sample", function(){
			return {
				"filters": {"docstatus": 1, "status": "Received"}
			}
		});
	},
	equipment: function(frm, cdt, cdn) {
		if (frm.doc.equipment) {
			/*
			frappe.call ({
				'method': 'tfaddon.get_equipment_details',
				'args': {
					'equipment':frm.doc.equipment,
				},
				'callback': function(res) {
					if (res.message) {
						console.log(res.message);
					}
				}

			});
			*/
			frappe.call ({
				'method': 'frappe.client.get',
				'args': {
					'doctype': 'Equipments',
					'name': frm.doc.equipment
				},
				'callback': function(res) {
					if (res.message) {
						frm.set_value("owner_eq_id", res.message.owner_eq_id? res.message.owner_eq_id: "-- ");
						frm.set_value("eq_type", res.message.eq_type);
 						frm.set_value("manufacturer_full_name", res.message.manufacturer_full_name);
						if (res.message.eq_sl_no[0] == "#") {
							frm.set_value("eq_sl_no", "-- ");
						} else {
							frm.set_value("eq_sl_no", res.message.eq_sl_no);
						}
						frm.set_value("eq_yom", res.message.eq_yom? res.message.eq_yom : "NS");
						frm.set_value("eq_cooling", res.message.eq_cooling);
						frm.set_value("voltage_class", res.message.voltage_class);
						frm.set_value("capacity", res.message.capacity);
						frm.set_value("voltage", res.message.voltage);
						frm.set_value("current", res.message.current);
						frm.set_value("eq_phases", res.message.eq_phases);
						if(res.message.eq_oil_type) {
							oil_type = res.message.eq_oil_type;
						} else {
							oil_type = "-- ";
						}
						if(res.message.eq_oil_qty) {
							oil_qty = res.message.eq_oil_qty + " kl"; 
						} else {
							oil_qty = "-- ";
						}
						frm.set_value("insulating_fluid", res.message.eq_oil_type + " / " + oil_qty);
					}
				}
			});
		}
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
						frm.set_value("installation_location", res.message.area + "/ " + res.message.location);
						frm.set_value("installation", res.message.installation? res.message.installation: "NS");
						frm.set_value("loc_cd", res.message.cd? res.message.cd: "NS" );
						frm.set_value("loc_ccd", res.message.ccd? res.message.ccd: "NS");
					}
				}
			});			
		}
	},
	sample: function(frm, cdt, cdn) {
		/*
		if (frm.doc.sample) {
			frappe.call ({
				"method": "frappe.client.get_value",
				"args": {
					"doctype": "Samples",
					"fildname": "status",
					"filters": {"name":frm.doc.sample}
				},
				"callback": function(res) {
					if (res.message && res.message.status != "Received") {
						//frappe.throw(_("Invalid Sample or Sample Not received"));
						msgprint("Invalid Sample or Sample Not received")
						validated=false;
						console.log(res.message.status);
					}
				}
			});
		}
		*/
		if (frm.doc.sales_order) {
			//alert('Inside sales_order Trigger...');
			frappe.call ({
				'method': 'frappe.client.get_list',
				'args': {
					'doctype': 'Sampling Containers',
					'fields': ['container_no','container_type','cust_identification'],
					'filters': {'parent': frm.doc.sample} 
				},
				'callback': function(res) {
					
					//console.log(res);
					if (res.message) {
						//alert('Inside callback if...');
						//$.each()
						var c_cont = "";
						var t_cont = "";
						for (i=0; i < res.message.length; i++) {
							if (c_cont != "") {c_cont += " & ";}
							if (t_cont != "") {t_cont += " & ";}
							t_cont += res.message[i].container_no;
							if (!res.message[i].cust_identification) {
								c_cont += "--";
							} else {
								c_cont += res.message[i].cust_identification;
							}
						}
						frm.set_value("trufil_container", t_cont);
						frm.set_value("customer_container", c_cont);

						//console.log(c_cont);
						//console.log(t_cont);
					}
				}
			});
			frappe.call ({
				'method': 'frappe.client.get',
				'args': {
					'doctype': 'Customer',
					'name': frm.doc.eq_owner
				},
				'callback': function(res) {
					if (res.message) {
						frm.set_value("eq_owner_name", res.message.customer_legal_name);
					}
				}
			});
			if (frm.doc.eq_load == 0) {frm.doc.eq_load = "--";}
			if (frm.doc.eq_ott == 0) {frm.doc.eq_ott = "--";}
			if (frm.doc.eq_wtt == 0) {frm.doc.eq_wtt = "--";}
		}
	}
});
