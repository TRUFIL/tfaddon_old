# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import frappe.utils
from frappe.utils import cstr, flt, getdate, comma_and, cint
from frappe import _
from datetime import datetime, date, time

class SampleTransportDetails(Document):
	def autoname(self):
		key = 'YY.#####'
		self.name = frappe.model.naming.make_autoname(key)

	def validate(self):
		if self.status == "Draft":
			self.validate_dispatch_details()
		elif self.status == "Dispatched":
			self.validate_receipt_details()

	def validate_dispatch_details(self):
		if (not self.dispatch_date):
			frappe.throw(_("Dispatch Date is Required"), frappe.MandatoryError)
		elif getdate(self.dispatch_date) > getdate():
			frappe.throw(_("Dispatch Date cannot be future date"), frappe.MandatoryError)

		if (not self.destination_lab):
			frappe.throw(_("Destination Lab is Required"), frappe.MandatoryError)

		if (not self.dispatch_mode):
			frappe.throw(_("Mode of Dispatch is Required"), frappe.MandatoryError)

		if (not self.dispatch_ref): 
			if (self.dispatch_mode == 'By Courier' or self.dispatch_mode == 'By Booking'):
				frappe.throw(_("Dispatch Doc Ref is Required"), frappe.MandatoryError)

		if (not self.sender_name):
			frappe.throw(_("Sender's Name is Required"), frappe.MandatoryError)

		if (not self.status):
			self.status = "Draft"

	def validate_receipt_details(self):
		if (not self.received_date):
			frappe.throw(_("Received Date is Required"), frappe.MandatoryError)
		elif getdate(self.received_date) > getdate():
			frappe.throw(_("Received Date cannot be future date"), frappe.MandatoryError)

		if (not self.receiving_lab):
			frappe.throw(_("Receiving Lab is Required"), frappe.MandatoryError)



	def clear_dispatch_details(self):
		self.destination_lab = self.dispatch_mode = self.dispatch_ref = self.exp_delivery_date = self.sender_name = self.sender_remark = ''

	def clear_receipt_details(self):
		self.receiving_lab = self.receiver_name = self.receiver_remarks = ''



