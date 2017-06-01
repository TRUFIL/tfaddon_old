# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime, date, time

class Samples(Document):
	def validate(self):
		self.validate_mandatory()

	def validate_mandatory(self):
		msg=''
		if self.status == 'NEW':
			if not self.container_1:
				msg = msg + "Bottle ID in Container 1, "
			if not self.collection_date:
				msg = "Collection Date, "
			if not self.weather_condition:
				msg = msg + "Weather Condition, "
			if not self.smp_condition:
				msg = msg + "Sampling Condition, "
			if not self.collected_by:
				msg = msg + "Collected By, "
			if self.collected_by == 'TRUFIL':
				if not self.sampler_name:
					msg = msg + "Sampler Name, "
			else:
				self.sampler_name = 'NA'
			if not self.smp_location:
				msg = msg + "Plant/ SS/ CD, "
			if not self.smp_eq_serial:
				msg = msg + "Make/ Serial No, "
			if not self.smp_eq_rating:
				msg = msg + "Capacity, "
			if not self.smp_eq_vr:
				msg = msg + "Voltage, "
			if not self.smp_point:
				msg = msg + "Sampling Point, "
			if msg: 
				msg = msg + "etc. are required fields"
				frappe.throw(_(msg))

# Other Functiona
