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
		if (self.status == 'Draft' or self.status == 'Assigned'):
			# validate transaction date v/s today's date
			if self.est_start_date:
				if getdate(self.est_start_date) < getdate(self.transaction_date):
					frappe.throw(_("Start Date cannot be past date"))

			# validate other mandatory field
			if not self.est_start_date:
				frappe.throw(_("Start Date is Required"))
			if not self.est_duration:
				frappe.throw(_("Activity Duration is Required"))
			if not self.contact_name:
				frappe.throw(_("Person to Contact is Required"))
			if not self.contact_no:
				frappe.throw(_("Contact No is Required"))
			if not self.site_location:
				frappe.throw(_("Site Location is Required"))
			if not self.est_samples:
				frappe.throw(_("Estimated No of Samples is Required"))
			if not self.est_container:
				frappe.throw(_("Estimated No of Bottles is Required"))
			if not self.assigned_to:
				frappe.throw(_("Job Assigned to is Required"))

	def update_readonly_fields(self):
		pass
	
