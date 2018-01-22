# frappe.model.naming.py
def set_name_by_naming_series(doc):
	"""Sets name by the `naming_series` property"""
	if not doc.naming_series:
		doc.naming_series = get_default_naming_series(doc.doctype)

	if not doc.naming_series:
		frappe.throw(frappe._("Naming Series mandatory"))

	##### Modified on 16-01-2018
	if not doc.company:
		frappe.throw(frappe._("Company mandatory"))
	else:
		company = frappe.get_doc("Company",doc.company)

	if doc.doctype in ["Sales Invoice","Delivery Note"]:
		if doc.is_return:
			doc.naming_series = doc.naming_series + "RET-"

	key = company.abbr + "-" + doc.naming_series + ".YY.-.#####"

	doc.name = make_autoname(key, '', doc)
	##### Modified on 16-01-2018


# product_bundle.py
def get_non_bundled_item_code(doctype, txt, searchfield, start, page_len, filters):
	from erpnext.controllers.queries import get_match_cond

	return frappe.db.sql("""select name, item_name, description from tabItem
		where is_product_bundle=0 and is_sales_item=1 
		and %s like %s %s limit %s, %s""" % (searchfield, "%s",
		get_match_cond(doctype),"%s", "%s"),
		("%%%s%%" % txt, start, page_len))

# erpnext.stock.doctype.item.item.py
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

# erpnext.controllers.selling_controller.py

class SellingController(StockController):
	def validate_order_type(self):
		# valid_types = ["Sales", "Maintenance", "Shopping Cart"]
		valid_types = ["Services","Sales", "Maintenance", "Shopping Cart"]
		if not self.order_type:
			self.order_type = "Sales"
		elif self.order_type not in valid_types:
			throw(_("Order Type must be one of {0}").format(comma_or(valid_types)))

