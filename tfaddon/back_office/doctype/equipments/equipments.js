// Copyright (c) 2016, DGSOL InfoTech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipments', {
	refresh: function(frm) {
		doc = frm.doc;
		cur_frm.set_query("eq_oil_type", function(){
			return {
				"filters": {"material_type": "Transformer Oil"}
			}
		});
		frm.events.show_hide_fields(frm);
	},

	eq_type: function(frm) {
		if (frm.doc.eq_type) {
			cur_frm.add_fetch('eq_type','eq_group','eq_group');
		}
		else {
			cur_frm.set_value("frm.doc.eq_group", null);	
			//frm.doc.eq_group = null;					
		}
	},

	eq_group: function(frm) {
		frm.events.show_hide_fields(frm);
	},

	show_hide_fields: function(frm) {
		// Show or Hide fields based on eq_group
		if (frm.doc.eq_group == "TRANSFORMER") {
			frm.toggle_display("voltage_class", true);
			frm.toggle_display("eq_capacity", true);
			frm.toggle_display("eq_pv", true);
			frm.toggle_display("eq_sv", true);
			frm.toggle_display("eq_tv", true);
			frm.toggle_display("eq_pc", false);
			frm.toggle_display("eq_sc", false);
			frm.toggle_display("eq_phases", true);
			frm.set_df_property('eq_capacity', 'label', 'Rating (kVA)');
		} 
		else if (frm.doc.eq_group == "POTENTIAL") {
			frm.toggle_display("voltage_class", true);
			frm.toggle_display("eq_capacity", true);
			frm.toggle_display("eq_pv", true);
			frm.toggle_display("eq_sv", true);
			frm.toggle_display("eq_tv", true);
			frm.toggle_display("eq_pc", false);
			frm.toggle_display("eq_sc", false);
			frm.toggle_display("eq_phases", true);
			frm.set_df_property('eq_capacity', 'label', 'Rating (VA)');
		} 
		else if (frm.doc.eq_group == "CURRENT" ) {
			frm.toggle_display("voltage_class", true);
			frm.toggle_display("eq_capacity", true);
			frm.toggle_display("eq_pv", false);
			frm.toggle_display("eq_sv", false);
			frm.toggle_display("eq_tv", false);
			frm.toggle_display("eq_pc", true);
			frm.toggle_display("eq_sc", true);
			frm.toggle_display("eq_phases", true);
			frm.set_df_property('eq_capacity', 'label', 'Rating (VA)');
		}
		else if (frm.doc.eq_group == "REACTOR" ) {
			frm.toggle_display("voltage_class", true);
			frm.toggle_display("eq_capacity", true);
			frm.toggle_display("eq_pv", false);
			frm.toggle_display("eq_sv", false);
			frm.toggle_display("eq_tv", false);
			frm.toggle_display("eq_pc", true);
			frm.toggle_display("eq_sc", false);
			frm.toggle_display("eq_phases", true);
			frm.set_df_property('eq_capacity', 'label', 'Rating (kVAr)');
		}
		else if (frm.doc.eq_group == "BUSHING" ) {
			frm.toggle_display("voltage_class", true);
			frm.toggle_display("eq_capacity", false);
			frm.toggle_display("eq_pv", false);
			frm.toggle_display("eq_sv", false);
			frm.toggle_display("eq_tv", false);
			frm.toggle_display("eq_pc", true);
			frm.toggle_display("eq_sc", false);
			frm.toggle_display("eq_phases", true);
		}
		else {
			frm.toggle_display("voltage_class", false);
			frm.toggle_display("eq_capacity", false);
			frm.toggle_display("eq_pv", false);
			frm.toggle_display("eq_sv", false);
			frm.toggle_display("eq_tv", false);
			frm.toggle_display("eq_pc", false);
			frm.toggle_display("eq_sc", false);
			frm.toggle_display("eq_phases", false);
			frm.set_df_property('eq_capacity', 'label', 'Rating (kVA)');
		}
	}
});

