# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime, date, time
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate
from collections import defaultdict

__version__ = '1.2.1'
__title__ = "TRUFIL Addon"

# Function to generate unique serial number
def generate_unique_serial_no():
	sl_no = datetime.now()
	return "#" + sl_no.strftime('%Y%m%d%H%M%S')

def cur_year():
	cur_date = datetime.now()
	return cur_date.strftime('%Y')

def get_no_of_samples(doctype, docname):
	return frappe.db.count("Samples",filters={"sampling_request":"SRQ-170003"})

@frappe.whitelist()
def update_field(doctype, docname, field, value=None):
	frappe.db.set_value("Doctype", "docname", "field", "value")

@frappe.whitelist()
def get_no_of_bottles(doctype, filters=None):
	conditions = []
	bottles = frappe.db.sql("""SELECT count(*) FROM `tabSampling Containers` 
		WHERE docstatus < 2  {fcond} {mcond} """.format(**{ 
			'fcond': get_filters_cond(doctype, filters, conditions), 
			'mcond': get_match_cond(doctype) 
			}) 
		)
	return bottles[0][0]

@frappe.whitelist()
def get_no_of_samples(doctype, filters=None):
	conditions = []
	samples = frappe.db.sql("""SELECT count(*) FROM `tabSamples`
		WHERE docstatus < 2  {fcond} {mcond} """.format(**{ 
			'fcond': get_filters_cond(doctype, filters, conditions), 
			'mcond': get_match_cond(doctype) 
			}) 
		)
	return samples[0][0]

