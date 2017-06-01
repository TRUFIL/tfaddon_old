# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils import cstr, flt, getdate, comma_and, cint
from frappe.model.document import Document
from frappe import _
from datetime import datetime, date, time


class SamplingRequest(Document):
	# before inserting or updating
	def validate(self):
		self.validate_mandatory_field()
		self.update_readonly_fields()

	def validate_mandatory_field(self):
		msg = ''
		today = date.today()
		if self.status == 'NEW':
			# validate transaction date v/s today's date
			if self.transaction_date:
				if getdate(self.transaction_date) > today:
					frappe.throw(_("Date Cannot be a future Date"))

			# validate other mandatory field
			if not self.assigned_to:
				msg = msg + "Job Assigned To, "
			if not self.contact_name:
				msg = msg + "Person to Contact, "
			if not self.contact_no:
				msg = msg + "Contact No, "
			if not self.est_samples:
				msg = msg + "Estimated No of Samples, "
			if not self.est_container:
				msg = msg + "Estimated No of Bottles, "
			if msg: 
				msg = msg + "are required to proceed"
				frappe.throw(_(msg))

		if self.status == 'ASSIGNED':
			if not self.act_samples:
				msg = msg + "Actual No of Samples, "
			if not self.act_bottles:
				msg = msg + "Actual No of Bottles, "
			if msg: 
				msg = msg + "are required to proceed"
				frappe.throw(_(msg))


	def update_readonly_fields(self):
		pass
	
