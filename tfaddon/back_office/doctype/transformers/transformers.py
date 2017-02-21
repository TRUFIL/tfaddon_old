# -*- coding: utf-8 -*-
# Copyright (c) 2015, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Transformers(Document):
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

	# validate all the required fields 
	def validate_mandatory_field(self):
		# validate for Rating and Voltages based on transformer type
		if (self.tr_type != "Drum"):
			if (self.tr_type == "Transformers" or self.tr_type == "CVT"):
				if not (self.tr_rating1 and self.tr_pv and tr_sv):
					frappe.throw(_("Rating 1, Primary Voltage and Secondary voltage is required for given transformer type"), frappe.MandatoryError)
			elif (self.tr_type == "Reactors" or self.tr_type == "Rectifiers"):
				if not (self.tr_rating1 and self.tr_pv):
					frappe.throw(_("Rating 1 and Primary Voltage is required for given transformer type"), frappe.MandatoryError)
			elif (self.tr_type == "Bushing" or self.tr_type == "OCB"):
				if not (self.tr_pv):
					frappe.throw(_("Primary Voltage is required for given transformer type"), frappe.MandatoryError)
			else:
				frappe.throw(_("Rating 1 is required for given transformer type"), frappe.MandatoryError)

		# validate No of phases
		if (self.tr_type != "Drum"):
			if not (self.tr_phases):
				frappe.throw(_("Please select appropriate No of Phases"), frappe.MandatoryError)

	# update all the derived fields 
	def update_readonly_fields(self):
		# Check for Serial Number
		if (self.tr_sl_no == "#"):
			self.tr_sl_no = generate_unique_serial_no()

		# Update Equipment Title


		# Update Voltage Ratio


		# Update Rating


# Function to generate unique serial number
def generate_unique_serial_no():
	sl_no = "#"

	return sl_no