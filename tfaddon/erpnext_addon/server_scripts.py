# product_bundle.py
def get_non_bundled_item_code(doctype, txt, searchfield, start, page_len, filters):
	from erpnext.controllers.queries import get_match_cond

	return frappe.db.sql("""select name, item_name, description from tabItem
		where is_product_bundle=0 and is_sales_item=1 
		and %s like %s %s limit %s, %s""" % (searchfield, "%s",
		get_match_cond(doctype),"%s", "%s"),
		("%%%s%%" % txt, start, page_len))

# item.py
class Item(WebsiteGenerator):
	def validate(self):
		self.validate_product_bundle()

	def validate_product_bundle(self):
		if (self.is_product_bundle):
			if self.is_stock_item:
				frappe.throw(_("product bundle must be a non-stock item."))

			if self.is_fixed_asset:
				frappe.throw(_("product bundle must be a non-asset item."))

			if self.is_purchase_item:
				frappe.throw(_("product bundle must be a non-purchase item."))

