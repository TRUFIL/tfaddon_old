# -*- coding: utf-8 -*-
# Copyright (c) 2015, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class FunctionalLocation(Document):
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
		if not (self.fl_cd):
			if not (self.fl_location and self.fl_point):
				frappe.throw(_("Substation and Functional Location is required if Code designation not available"), frappe.MandatoryError)
	
	# update all the derived fields 
	def update_readonly_fields(self):
		if (self.fl_cd):
			self.fl_title = self.fl_cd
		elif (self.fl_area and self.fl_location and self.fl_point):
				self.fl_title = self.fl_area + "/" + self.fl_location + "/" + self.fl_point
		elif (self.fl_location and self.fl_point):
			self.fl_title = self.fl_location + "/" + self.fl_point
