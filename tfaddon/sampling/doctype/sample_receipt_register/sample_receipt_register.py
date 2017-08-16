# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.data import getdate
from frappe.model.document import Document
from frappe import _, throw

class SampleReceiptRegister(Document):
	def validate(self):
		self.update_read_only_fields()
		self.validate_mandatory_field()


	def validate_mandatory_field(self):
		# Check for future Dates
		if self.receipt_date:
			if getdate(self.receipt_date) > getdate():
				frappe.throw(_("Receipt Date cannot be future date"))
		else:
			frappe.throw(_("Receipt Date is required"))


	def update_read_only_fields(self):
		self.title = self.laboratory + "-" + self.bag_no + "-" + self.name