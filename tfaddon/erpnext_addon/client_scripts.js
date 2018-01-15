// sales_commom.js
erpnext.selling.SellingController = erpnext.TransactionController.extend({
		setup_queries: function() {
		if(this.frm.fields_dict["items"].grid.get_field('item_code')) {
			this.frm.set_query("item_code", "items", function() {
				return {
					query: "erpnext.controllers.queries.item_query",
					filters: {'is_sales_item': 1, 'is_product_bundle': 1}
				}
			});
		}

});

// product_bundle.js
cur_frm.fields_dict['items'].grid.get_field("item_code").get_query = function() {
	return{
		query: 	"erpnext.selling.doctype.product_bundle.product_bundle.get_non_bundled_item_code"
	}
}

// item.js
frappe.ui.form.on('Item', {
	is_fixed_asset: function(frm) { 
		//frm.set_value("is_stock_item", frm.doc.is_fixed_asset ? 0 : 1);
		if (frm.doc.is_fixed_asset) {
			if (frm.doc.item_group == "Bundle") {
				frappe.msgprint(__('Fixed Asset cannot be a part of Item Group {0}'.format("Bundle")));
				frappe.validated = 0;
			}
			frm.set_value("is_stock_item", 0);
		}
	},
	item_group: function(frm) {
		if (frm.doc.item_group == "Bundle") { 
			if (frm.doc.is_stock_item || frm.doc.is_fixed_asset || frm.doc.is_purchase_item) {
				frappe.msgprint(__('Bundled Item cannot be a Stock Item or Fixed Asset or Purchase Item'));
				frappe.validated = 0;
			} else {
				frm.set_value("is_product_bundle", 1);
				frm.set_value("default_warehouse","");
			}
		}
	},
	is_stock_item: function(frm) {
		if(!frm.doc.is_stock_item) {
			if (frm.doc.item_group == "Bundle") {
				frappe.msgprint(__('Stock Item cannot be a part of Item Group Bundled'));
				frappe.validated = 0;
			}
			frm.set_value("has_batch_no", 0);
			frm.set_value("create_new_batch", 0);
			frm.set_value("has_serial_no", 0);
			frm.set_value("default_warehouse", "");
		}
	},

})