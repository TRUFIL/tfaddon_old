# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
#from frappe.model.document import Document
from frappe import _
import tfaddon
from tfaddon.controllers.tf_status_updater import TFStatusUpdater

class Samples(TFStatusUpdater):
	def onload(self):
		pass
	def on_submit(self):
		if not self.sample_id:
			self.sample_id = frappe.model.naming.make_autoname("TL/SM/.YY./", "Samples")
			self.status = "Verified"
			self.save()
		
	def validate(self):
		self.validate_mandatory()

	def has_dispatch_details(self):
		pass

	def has_receipt_details(self):
		pass

	def has_open_job_order(self):
		#return frappe.db.get_value("Job Order", {"sample_name": self.name})
		#last_login, last_ip = frappe.db.get_value("User", "test@example.com", ["last_login", "last_ip"])
		docstatus, status = frappe.db.get_value("Job Order", {"sample_name": self.name}, ["docstatus", "status"])
		if (docstatus == 1 and status != "Completed"):
			return True
		else:
			return False


	def has_completed_job_order(self):
		pass

	def has_disposed_details(self):
		pass

	def validate_mandatory(self):
		if (self.collected_by == "TRUFIL"):
			if not (self.sampling_request):
				frappe.throw(_("Sampling Request is required"))
			if not (self.sampler_name):
				frappe.throw(_("Sampler Name is required"))

		if (self.collected_by == "Customer"):
			if not (self.sales_order):
				frappe.throw(_("Sales Order is required"))
		elif (self.collected_by == "TRUFIL"):
			if not (self.sampler_name):
				frappe.throw(_("Sampler Name is required"))
		else:
			frappe.throw(_("Collected By is required"))

		if self.smp_source == "Equipment":
			if not self.smp_type:
				frappe.throw(_("Please select appropriate Sample Type"))
			if not self.smp_point:
				frappe.throw(_("Please select appropriate Sampling Point"))
		elif self.smp_source == "Storage":
			if self.smp_type != "Transformer Oil":
				frappe.throw(_("Sample Type must be Transformer Oil if sample is collected from Storage"))
		else:
			frappe.throw(_("Please select appropriate Sample Taken From"))

		if not self.weather_condition:
			frappe.throw(_("Please select appropriate Weather Condition"))

		if not self.smp_condition:
			frappe.throw(_("Please select appropriate Sampling Condition"))

		if not self.eq_owner:
			frappe.throw(_("Equipment/Location Owner is required"))

		"""if not self.eq_location:
			frappe.throw(_("Location is required"))"""

		if not self.receipt_date:
			frappe.throw(_("Receipt Date is required"))

		if not self.material:
			frappe.throw(_("Material tested is required"))

		if not self.laboratory:
			frappe.throw(_("Receiving Laboratory is required"))

		if not self.receipt_condition:
			frappe.throw(_("Sample Condition is required"))

		if not self.equipment:
			frappe.throw(_("Equipment is required"))

		if not self.location:
			frappe.throw(_("Location is required"))

# Other Functiona
