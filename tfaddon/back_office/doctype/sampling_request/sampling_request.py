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
	def validate(self):
		frappe.msgprint(_("Current DocStatus :" + cstr(cint(self.docstatus)) + "    Current Status :" + self.workflow_state))
		if (self.is_new() or self.docstatus == 0):
			self.validate_new_document()
		elif (self.docstatus == 1 and self.workflow_state == "Closed"):
			self.validate_response_fields()
		elif (self.docstatus == 2): # and self.workflow_state == "Cancelled"):
			self.validate_cancelled_fields()
		#self.validate_mandatory_field()
		self.update_readonly_fields()

	def on_submit(self):
		pass

	def on_cancel(self):
		pass
	
	def validate_mandatory_field(self):
		if (self.is_new()):
			self.validate_new_document()
		elif (self.docstatus == 0):
			self.validate_new_document()
		elif (self.docstatus == 1 and self.workflow_state == "Closed"):
			self.validate_response_fields()
		elif (self.docstatus == 2 and self.workflow_state == "Cancelled"):
			self.validate_cancelled_fields()

	def update_readonly_fields(self):
		if (self.docstatus == 1):
			self.closer_date = getdate()
		else:
			self.closer_date = ""

	def validate_new_document(self):
		if self.est_start_date:
			if getdate(self.est_start_date) < getdate():
					frappe.throw(_("Start Date cannot be past date"))
		else:
			frappe.throw(_("Start Date is Required"))
	
		if (self.est_duration == 0):
			frappe.throw(_("Activity Duration must not be 0"))

		if (self.est_samples == 0):
			frappe.throw(_("Estimated No of Samples must not be 0"))

		if (self.est_containers < self.est_samples):
			frappe.throw(_("Estimated No of Bottles can not be less than number of samples"))

	def validate_response_fields(self):
		if (self.act_start_date):
			if getdate(self.act_start_date) >= getdate():
					frappe.throw(_("Start Date cannot be future date"))
			else:
				frappe.throw(_("Start Date is Required"))

		if (isinstance(self.act_duration, int) and self.act_duration != 0):
			pass
		else:
			frappe.throw(_("Activity Duration must not be 0"))

		if (isinstance(self.act_samples, int) and self.act_samples != 0):
			pass
		else:
			frappe.throw(_("Actual No of Samples must not be 0"))

		if (isinstance(self.act_containers, int) and self.act_samples != 0):
			if (self.act_containers < self.act_samples):
				frappe.throw(_("Estimated No of Bottles can not be less than number of samples"))
		else:
			frappe.throw(_("Actual No of Bottles must not be 0"))


	def validate_cancelled_fields(self):
		if (self.act_samples > 0):
			frappe.throw(_("Actual No of Samples must not be 0"))

		if (self.act_containers < self.act_samples):
			frappe.throw(_("Actual No of Bottles can not be less than number of samples"))
