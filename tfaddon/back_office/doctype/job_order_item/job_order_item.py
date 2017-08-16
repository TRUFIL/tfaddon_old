# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.controllers.print_settings import print_settings_for_item_table

class JobOrderItem(Document):
	def __setup__(self):
		print_settings_for_item_table(self)

