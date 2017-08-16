# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SamplingPoint(Document):
	def autoname(self):
		if self.sampling_source == "Equipment":
			self.name = "Equipment-" + self.sampling_point
		else:
			self.name = self.sampling_point
