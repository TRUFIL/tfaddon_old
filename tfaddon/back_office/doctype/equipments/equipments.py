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
		eq_params["capacity"] = self.get_capacity()
		
		# Voltage
		eq_params["voltage"] = self.get_voltage()

		# Voltage Ratio
		eq_params["voltage ratio"] = self.get_voltage_ratio()

		# Current
		eq_params["current"] = self.get_current()
		
		# Current Ratio
		eq_params["current ratio"] = self.get_current_ratio()

		# No of Phases
		eq_params["no of phases"] = self.get_phases()

		# Update Read Only Fields
		self.capacity = eq_params["capacity"]
		if (eq_params["voltage ratio"]):
			self.voltage = eq_params["voltage ratio"]
		else:
			self.voltage = eq_params["voltage"]

		if (eq_params["current ratio"]):
			self.current = eq_params["current ratio"]
		else:
			self.current = eq_params["current"]

		# return eq_params
		#self.set_onload('equipment_info', eq_params)

	def get_capacity(self):
		capacity = ""
		if (self.tr_rating1 and self.tr_rating2):
			capacity = str(self.tr_rating1) + "/" + str(self.tr_rating2)
		elif (self.tr_rating1):
			capacity = str(self.tr_rating1)
		else:
			capacity = ""
		if (capacity != ""):
			if (self.eq_category == "REACTOR"):
				capacity = capacity + " kVAr"
			else:
				capacity = capacity + " kVA"
		return capacity

	def get_voltage(self):
		voltage = ""
		if (self.eq_category == "CURRENT" or self.eq_category == "REACTOR" or self.eq_category == "BUSHING"):
			if (self.tr_pv):
				voltage = str(self.tr_pv) + " Volts"
			else:
				voltage = "Not Available"
		else:
			voltage = ""
		return voltage

	def get_voltage_ratio(self):
		vratio = ""
		if (self.eq_category == "TRANSFORMER" or self.eq_category == "POTENTIAL"):
			if (self.tr_pv and self.tr_sv and self.tr_tv):
				vratio = str(self.tr_pv) + "/" + str(self.tr_sv) + ("/" + str(self.tr_tv)) + " Volts"
			elif (self.tr_pv and self.tr_sv):
				vratio = str(self.tr_pv) + "/" + str(self.tr_sv) + " Volts"
			else:
				vratio = "Not Available"
		else:
			vratio = ""
		return vratio

	def get_current(self):
		current = ""
		if (self.eq_category == "BUSHING"):
			if (self.tr_pc):
				current = str(self.tr_pc) + " Amps"
			else:
				current = "Not Available"
		else:
			current = ""
		return current

	def get_current_ratio(self):
		cratio = ""
		if (self.eq_category == "CURRENT"):
			if (self.tr_pc and self.tr_sc):
				cratio = str(self.tr_pc) + "/" + str(self.tr_sc) + " Amps"
			else:
				cratio = "Not Available"
		else:
			cratio = ""
		return cratio

	def get_phases(self):
		phases = ""
		if (self.eq_category != "CONTAINER"):
			if (self.tr_phases):
				phases = self.tr_phases
			else:
				phases = "Not Available"
		else:
			phases = ""
		return phases

# Function to generate unique serial number
def generate_unique_serial_no():
	sl_no = datetime.now()
	return "#" + sl_no.strftime('%Y%m%d%H%M%S')


def get_eq_info_template():
	info_template = """
	<div>

	</div>
"""


"""
def get_default_equipment_info_template():
	return '''
{%- if eq_info["Capacity"] -%}'''+_('Capacity')+''': {{ eq_info["Capacity"] }}<br>{%- endif -%}
{%- if eq_info["Voltage"] -%}'''+_('Voltage')+''': {{ eq_info["Voltage"] }}<br>{%- endif -%}
{%- if eq_info["Voltage Ratio"] -%}'''+_('Voltage Ratio')+''': {{ eq_info["Voltage Ratio"] }}<br>{%- endif -%}
{%- if eq_info["Current"] -%}'''+_('Current')+''': {{ eq_info["Current"] }}<br>{%- endif -%}
{%- if eq_info["Current Ratio"] -%}'''+_('Current Ratio')+''': {{ eq_info["Current Ratio"] }}<br>{%- endif -%}
{%- if eq_info["No of Phases"] -%}'''+_('No of Phases')+''': {{ eq_info["No of Phases"] }}<br>{%- endif -%}


	'''
"""
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