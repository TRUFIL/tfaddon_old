# -*- coding: utf-8 -*-
# Copyright (c) 2015, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Locations(Document):
	# before inserting or updating
	def before_insert(self):
		pass
	
	# before inserting or updating
	def validate(self):
		self.validate_mandatory_field()
		self.update_readonly_fields()
	
	# after saving
	def on_update(self):
		pass
	# when document is set as submitted
	def on_submit(self):
		pass
	
	# when document is set to be cancellec
	def on_cancel(self):
		pass
	
	# before it is about to be deleted
	def on_trash (self):
		pass

	# validate all the required fields are properly filled up
	def validate_mandatory_field(self):
		if not (self.ccd):
			if not (self.location and self.cd):
				frappe.throw(_("Substation and Customer Eq Designation is required if Code designation not available"), frappe.MandatoryError)
	
	# update all the derived fields 
	def update_readonly_fields(self):
		if (self.ccd):
			self.title = self.ccd.strip()
		elif (self.area and self.location and self.cd):
				self.title = self.owner + "|" + self.area.strip() + "|" + self.location.strip() + "|" + self.cd.strip()
		elif (self.location and self.cd):
			self.title = self.owner + self.location.strip() + "|" + self.cd.strip()
			

