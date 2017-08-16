# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils.data import getdate
from frappe.model.document import Document
from frappe import _, throw

class SampleDispatchRegister(Document):
	def validate(self):
		self.update_read_only_fields()
		self.validate_mandatory_field()


	def validate_mandatory_field(self):
		# Check for future Dates
		if self.dispatch_date:
			if getdate(self.dispatch_date) > getdate():
				frappe.throw(_("Dispatch Date cannot be future date"))
		else:
			frappe.throw(_("Dispatch Date is required"))

		# Check for valid Dispatch By
		if not self.dispatch_by:
			frappe.throw(_("Dispatched By is required"))

		# Check for Dispatch Mode
		if self.dispatch_mode in ["Courier", "Booking", "Bus", "Train", "Hand"]:
			if not self.person_courier:
				frappe.throw(_("Name of person/Courier is required"))
		else:
			frappe.throw(_("Please select Dispatch Mode"))

		if not self.ref_no and self.dispatch_mode in ["Courier", "Booking"]:
			frappe.throw(_("Reference No is required"))

		if not self.contact_no and self.dispatch_mode in ["Bus", "Train", "Hand"]:
			frappe.throw(_("Contact No is required"))


	def update_read_only_fields(self):
		self.title = self.bag_no + "-" + self.laboratory + "-" + self.name		