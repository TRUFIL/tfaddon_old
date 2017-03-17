// Copyright (c) 2016, DGSOL InfoTech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transformers', {
	refresh: function(frm) {
		frm.toggle_display(['eq_params_html'], !frm.doc.__islocal);

	}
});
