# -*- coding: utf-8 -*-
# Copyright (c) 2015, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime, date, time

class Equipments(Document):
	# load calculated details
	def onload(self):
		self.get_equipment_info()

	# before inserting or updating
	def before_insert(self):
		pass
	
	# before inserting or updating
	def validate(self):
		self.validate_mandatory_field()
		# Update Serial Number
		if (self.tr_sl_no == "#"):
			self.tr_sl_no = generate_unique_serial_no()
		
		# Update Equipment Title
		self.title = self.tr_manufacturer + '-' + self.tr_sl_no

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
		# validate equipment parameters on equipment type
		if (self.eq_category != "CONTAINER"):
			if not (self.tr_phases):
				frappe.throw(_("Please select appropriate No of Phases"), frappe.MandatoryError)

			if (self.eq_category == "TRANSFORMER" or self.eq_category == "POTENTIAL"):
				if (not self.tr_rating1 or self.tr_rating1 == 0):
					frappe.throw(_("Primary Rating is Mandatory"), frappe.MandatoryError)
				if (not self.tr_pv or self.tr_pv == 0):
					frappe.throw(_("Primary Voltage is Mandatory"), frappe.MandatoryError)
				if (not self.tr_sv or self.tr_sv == 0):
					frappe.throw(_("Secondary Voltage is Mandatory"), frappe.MandatoryError)
			elif (self.eq_category == "CURRENT"):
				if (not self.tr_rating1 or self.tr_rating1 == 0):
					frappe.throw(_("Primary Rating is Mandatory"), frappe.MandatoryError)
				if (not self.tr_pv or self.tr_pv == 0):
					frappe.throw(_("Primary Voltage is Mandatory"), frappe.MandatoryError)
				if (not self.tr_pc):
					frappe.throw(_("Primary current is Mandatory"), frappe.MandatoryError)
			elif (self.eq_category == "REACTOR"):
				if (not self.tr_rating1 or self.tr_rating1 == 0):
					frappe.throw(_("Primary Rating is Mandatory"), frappe.MandatoryError)
				if (not self.tr_pv or self.tr_pv == 0):
					frappe.throw(_("Primary Voltage is Mandatory"), frappe.MandatoryError)
			elif (self.eq_category == "BUSHING"):
				if (not self.tr_pv or self.tr_pv == 0):
					frappe.throw(_("Primary Voltage is Mandatory"), frappe.MandatoryError)
				if (not self.tr_pc or self.tr_pc == 0):
					frappe.throw(_("Primary current is Mandatory"), frappe.MandatoryError)
			else:
				if (not self.tr_pv or self.tr_pv == 0):
					frappe.throw(_("Primary Voltage is Mandatory"), frappe.MandatoryError)

	def get_equipment_info(self):
		eq_params = {}

		# Capacity
		if (self.eq_category == "TRANSFORMER"):
			if (self.tr_rating1 and self.tr_rating2):
				eq_params["Capacity"] = str(self.tr_rating1) + "/" + str(self.tr_rating2) + " kVA"
			elif (self.tr_rating1):
				eq_params["Capacity"] = str(self.tr_rating1) + " kVA"
			else:
				eq_params["Capacity"] = "Not Available"
		elif (self.eq_category == "CURRENT" or self.eq_category == "POTENTIAL"):
			if (self.tr_rating1):
				eq_params["Capacity"] = str(self.tr_rating1) + " VA"
			else:
				eq_params["Capacity"] = "Not Available"
		elif (self.eq_category == "REACTOR"):
			if (self.tr_rating1):
				eq_params["Capacity"] = str(self.tr_rating1) + " kVAr"
			else:
				eq_params["Capacity"] = "Not Available"
		else:
			eq_params["Capacity"] = ""
		
		# Voltage
		if (self.eq_category == "CURRENT" or self.eq_category == "REACTOR" or self.eq_category == "BUSHING"):
			if (self.tr_pv):
				eq_params["Voltage"] = str(self.tr_pv) + " Volts"
			else:
				eq_params["Voltage"] = "Not Available"
		else:
			eq_params["Voltage"] = ""

		# Voltage Ratio
		if (self.eq_category == "TRANSFORMER" or self.eq_category == "POTENTIAL"):
			if (self.tr_pv and self.tr_sv and self.tr_tv):
				eq_params["Voltage Ratio"] = str(self.tr_pv) + "/" + str(self.tr_sv) + ("/" + str(self.tr_tv)) + " Volts"
			elif (self.tr_pv and self.tr_sv):
				eq_params["Voltage Ratio"] = str(self.tr_pv) + "/" + str(self.tr_sv) + " Volts"
			else:
				eq_params["Voltage Ratio"] = "Not Available"
		else:
			eq_params["Voltage Ratio"] = ""

		# Current
		if (self.eq_category == "BUSHING"):
			if (self.tr_pc):
				eq_params["Current"] = str(self.tr_pc) + " Amps"
			else:
				eq_params["Current"] = "Not Available"
		else:
			eq_params["Current"] = ""
		
		# Current Ratio
		if (self.eq_category == "CURRENT"):
			if (self.tr_pc and self.tr_sc):
				eq_params["Current Ratio"] = str(self.tr_pc) + "/" + str(self.tr_sc) + " Amps"
			else:
				eq_params["Current Ratio"] = "Not Available"
		else:
			eq_params["Current Ratio"] = ""

		# No of Phases
		if (self.eq_category != "CONTAINER"):
			if (self.tr_phases):
				eq_params["No of Phases"] = self.tr_phases
			else:
				eq_params["No of Phases"] = "Not Available"
		else:
			eq_params["No of Phases"] = ""

		# Update Read Only Fields
		self.capacity = eq_params["Capacity"]
		if (eq_params["Voltage Ratio"]):
			self.voltage = eq_params["Voltage Ratio"]
		else:
			self.voltage = eq_params["Voltage"]

		if (eq_params["Current Ratio"]):
			self.current = eq_params["Current Ratio"]
		else:
			self.current = eq_params["Current"]

		# return eq_params
		self.set_onload('equipment_info', eq_params)

# Function to generate unique serial number
def generate_unique_serial_no():
	sl_no = datetime.now()
	return "#" + sl_no.strftime('%Y%m%d%H%M%S')



def get_default_equipment_info_template():
	return '''
{% if eq_info["Capacity"] %}'''+_('Capacity')+''': {{ eq_info["Capacity"] }}<br>{% endif -%}
{% if eq_info["Voltage"] %}'''+_('Voltage')+''': {{ eq_info["Voltage"] }}<br>{% endif -%}
{% if eq_info["Voltage Ratio"] %}'''+_('Voltage Ratio')+''': {{ eq_info["Voltage Ratio"] }}<br>{% endif -%}
{% if eq_info["Current"] %}'''+_('Current')+''': {{ eq_info["Current"] }}<br>{% endif -%}
{% if eq_info["Current Ratio"] %}'''+_('Current Ratio')+''': {{ eq_info["Current Ratio"] }}<br>{% endif -%}
{% if eq_info["No of Phases"] %}'''+_('No of Phases')+''': {{ eq_info["No of Phases"] }}<br>{% endif -%}


	'''

"""
@frappe.whitelist()
def get_default_address_template():
	'''Get default address template (translated)'''
	return '''{{ address_line1 }}<br>{% if address_line2 %}{{ address_line2 }}<br>{% endif -%}\
{{ city }}<br>
{% if state %}{{ state }}<br>{% endif -%}
{% if pincode %}{{ pincode }}<br>{% endif -%}
{{ country }}<br>
{% if phone %}'''+_('Phone')+''': {{ phone }}<br>{% endif -%}
{% if fax %}'''+_('Fax')+''': {{ fax }}<br>{% endif -%}
{% if email_id %}'''+_('Email')+''': {{ email_id }}<br>{% endif -%}'''

"""