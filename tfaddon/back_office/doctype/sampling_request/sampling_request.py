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
		if (self.is_new()):
			self.validate_new_document()
		#self.update_readonly_fields()

	def before_submit(self):
		#self.validate_response_fields()
		pass

	def on_submit(self):
		#frappe.msgprint(_("Current DocStatus :" + cstr(cint(self.docstatus)) + "    Current Status :" + self.workflow_state))
		pass

	def on_cancel(self):
		#frappe.msgprint(_("Current DocStatus :" + cstr(cint(self.docstatus)) + "    Current Status :" + self.workflow_state))
		pass
	
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

	def validate_assignment_fields(self):
		pass

	def validate_response_fields(self):
		if (self.workflow_state == "Closed"):
			if (self.act_start_date):
				if getdate(self.act_start_date) > getdate():
					frappe.throw(_("Actual Start Date cannot be future date"))
			else:
				frappe.throw(_("Start Date is Required"))

			if not (self.act_duration):
				frappe.throw(_("Activity Duration must not be 0"))

			if not (self.act_samples):
				frappe.throw(_("Actual No of Samples must not be 0"))

			if not (self.act_containers):
				frappe.throw(_("Actual No of Bottles must not be 0"))
			else:
				if (self.act_containers < self.act_samples):
					frappe.throw(_("Estimated No of Bottles can not be less than number of samples"))

			if (self.docstatus == 0):
				self.workflow_state = "In Process"


	def validate_cancelled_fields(self):
		if (self.act_samples > 0):
			frappe.throw(_("Actual No of Samples must not be 0"))

		if (self.act_containers < self.act_samples):
			frappe.throw(_("Actual No of Bottles can not be less than number of samples"))

	def declare_req_closed(self, args):
		if self.has_samples():
			frappe.db.set(self, 'act_start_date', args["act_start_date"])
			frappe.db.set(self, 'act_duration', args["act_duration"])
			frappe.db.set(self, 'response_remarks', args["response_remarks"])
			frappe.db.set(self, 'closer_date', getdate())
			frappe.db.set(self, 'workflow_state', 'Closed')
			frappe.db.set(self, 'act_samples', self.get_no_of_samples())
			frappe.db.set(self, 'act_containers', self.get_no_of_bottles())
		else:
			frappe.throw(_("Cannot set as Closed as no samples created under this sampling request."))

	def declare_req_cancelled(self, args):
		#frappe.msgprint(_("Inside declare_req_closed"))
		if self.has_samples():
			frappe.throw(_("Cannot set as Cancelled because samples are already created under this sampling request."))
		else:
			frappe.db.set(self, 'response_remarks', args["response_remarks"])
			frappe.db.set(self, 'closer_date', getdate())
			frappe.db.set(self, 'workflow_state', 'Cancelled')

	def has_samples(self):
		#return frappe.db.get_value("Samples", {"sampling_request": self.name})
		if (self.get_no_of_samples() > 0):
			return 0
		else:
			return 1

	def get_no_of_samples(self):
		smp = frappe.db.sql("""SELECT FORMAT(COUNT(s.name),0) as samples 
			FROM `tabSamples` as s 
			WHERE s.sampling_request = '{0}' AND s.docstatus = 1""".format(self.name), as_dict=True, formatted=True)
		return smp[0]["samples"]

	def get_no_of_bottles(self):
		bot = frappe.db.sql("""SELECT FORMAT(COUNT(c.name),0) as bottles 
			FROM  `tabSampling Containers` as c 
			JOIN `tabSamples` as s ON c.parent = s.name 
			WHERE s.sampling_request = '{0}' AND s.docstatus = 1""".format(self.name), as_dict=True, formatted=True)
		return bot[0]["bottles"]