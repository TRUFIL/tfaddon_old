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
		frm.set_query("alt_address", function(){
			if(doc.is_alt_issued_to && (!doc.alt_customer)) {
				frappe.throw(_('Please select Alt Customer'));
			}

			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Customer',
					link_name: doc.alt_customer
				}
			};
		});
	},
	equipment: function(frm, cdt, cdn) {
		if (frm.doc.equipment) {
			
			frappe.call ({
				'method': 'tfaddon.get_equipment_details',
				'args': {
					'equipment':frm.doc.equipment,
				},
				'callback': function(res) {
					if (res.message) {
						console.log(res.message);
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
				'method': 'tfaddon.get_location_details',
				'args': {
					'location':frm.doc.location,
				},
				'callback': function(res) {
					if (res.message) {
						console.log(res.message);
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
		if (frm.doc.sample) {
			if (frm.doc.eq_load == 0) {frm.doc.eq_load = "--";}
			if (frm.doc.eq_ott == 0) {frm.doc.eq_ott = "--";}
			if (frm.doc.eq_wtt == 0) {frm.doc.eq_wtt = "--";}
		}
	},
	sales_order: function (frm) {
		if (frm.doc.sales_order) {
			frappe.call ({
				'method': 'tfaddon.get_so_details',
				'args': {
					'doctype': 'Sales Order',
					'docname': frm.doc.sales_order
				},
				'callback': function(res) {
					if (res.message) {
						console.log(res.message);
						frm.set_value("po_no_date", res.message[0]["po_no"] + " dated " + 
							frappe.datetime.str_to_user(res.message[0]["po_date"]));
						frm.set_value("so_no_date", res.message[0]["name"] + " dated " + 
							frappe.datetime.str_to_user(res.message[0]["transaction_date"]));
						frm.set_value("issued_to", res.message[0]["customer_legal_name"]);
						frm.set_value("issued_to_address", res.message[0]["address_display"]);
					}
				}
			});
		}
	},
	eq_owner: function (frm) {
		if (frm.doc.eq_owner) {
			frappe.call ({
				'method': 'tfaddon.get_customer_details',
				'args': {
					'doctype': 'Customer',
					'docname': frm.doc.eq_owner
				},
				'callback': function(res) {
					if (res.message) {
						//console.log(res.message);
						//console.log(res.message[0]["customer_legal_name"]);
						frm.set_value("eq_owner_name", res.message[0]["customer_legal_name"]);
					}
				}
			});
		}
	},
	alt_customer: function (frm) {
		frm.set_value("alt_address",null);
		frm.set_value("alt_issued_to_address",null);
	},
	alt_address: function (frm) {
		erpnext.utils.get_address_display(frm, "alt_address", "alt_issued_to_address");		
	}
});
