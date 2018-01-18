# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe 
from frappe import _ 
from datetime import datetime, date, time
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate
from collections import defaultdict

__version__ = '2.1.0'
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

@frappe.whitelist()
def get_equipment_details(equipment):
	return frappe.get_doc("Equipments", equipment).as_dict()

@frappe.whitelist()
def get_location_details(location):
	return frappe.get_doc("Locations", location).as_dict()

@frappe.whitelist() 
def get_so_details(doctype, docname):
	return frappe.db.sql("""Select name,customer,customer_name,customer_legal_name,transaction_date, 
		po_no,po_date,collected_by,address_display 
		from `tabSales Order`
		where name = %s""",(docname),as_dict=True, formatted=True)

@frappe.whitelist() 
def get_customer_details(doctype, docname):
	
	return frappe.db.sql("""Select customer_name,customer_legal_name,customer_type, 
		customer_group,territory,cin,yoi,pan 
		from `tabCustomer`
		where disabled=0 and name = %s""",(docname), as_dict=True, formatted=True)

	#return erpnext.controllers.queries.customer_query(doctype, docname)
