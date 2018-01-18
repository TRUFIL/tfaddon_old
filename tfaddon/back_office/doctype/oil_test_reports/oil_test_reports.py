# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.utils import cint, flt, cstr, getdate

class OilTestReports(Document):
	def onload (self):
		pass

	def on_update(self):
		doc = frappe.get_doc("Samples", self.sample)
		if (doc.status == "Received"):
			doc.status = "In Process"
			doc.save()

	def on_trash(self):
		frappe.db.sql("""update `tabSamples` set status='Received' where name=%s""",
			self.sample)

	def on_submit(self):
		if not self.report_no:
			self.report_no = frappe.model.naming.make_autoname("TL/OTR/.YY./", "Oil Test Reports")
			self.report_date = getdate()
			self.save()

		doc = frappe.get_doc("Samples", self.sample)
		doc.certificate = self.name
		doc.status = "Completed"
		doc.save()

	def before_cancel(self):
		doc = frappe.get_doc("Samples", self.sample)
		doc.certificate = ""
		doc.status = "Received"
		doc.save()


	def validate(self):
		if not (self.is_ost or self.is_dga or self.is_furan):
			frappe.throw(_("Please select the appropriate tests for which this certificate is generated"))
		else:
			if (self.is_ost):
				if not (self.ost_interpretation and self.ost_frequency):
					frappe.throw(_("OST Interpretation and Frequency is required"))

			if (self.is_dga):
				if not (self.dga_interpretation and self.dga_frequency):
					frappe.throw(_("DGA Interpretation and Frequency is required"))

			if (self.is_furan):
				if not (self.furan_interpretation and self.fruan_frequency):
					frappe.throw(_("Furan Interpretation and Frequency is required"))

			if not (self.recommendation):
				frappe.throw(_("Overall recommendation is required"))

		if (self.docstatus == 0):
			self.update_read_only_fields()

		if (self.is_alt_issued_to == 1):
			# Throw exception if Alt Customer is blank
			if not self.alt_customer or self.alt_customer == "":
				frappe.throw(_("Alt Customer is required"))

			# Throw exception if Alt Address is blank
			if not self.alt_address:
				frappe.throw(_("Alt Address is required"))
		else:
			# Make alt details blank
			self.alt_customer = ""
			self.alt_issued_to = ""
			self.alt_address = ""
			self.alt_issued_to_address = ""

	def update_read_only_fields(self):
		if (self.is_dga):
			self.dga_tdcg = self.calculate_tdcg()
			if (self.dga_tgc != "NT" and flt(self.dga_tgc,6) > 0.000001):
				self.dga_tdcg_tcg = cstr(round(flt(self.dga_tdcg,3) / (flt(self.dga_tgc,3) * 100),4))
			else:
				frappe.throw(_("Total Gas Content is required"))
		if (self.is_furan):
			self.furan_tfc = self.calculate_tfc()

	def calculate_tdcg(self):
		tdcg_fields = [self.dga_h2, self.dga_co, self.dga_ch4, self.dga_c2h6, self.dga_c2h4, self.dga_c2h2, self.dga_c3h8, self.dga_c3h6]
		return calculate_total(tdcg_fields)

	def calculate_tfc(self):
		tfc_fields = [self.furan_5h2f, self.furan_2fa, self.furan_2f, self.furan_2a, self.furan_5m2f]
		return calculate_total(tfc_fields)

def calculate_total(field_list, precision = 2):
	total=0.0
	for fld in field_list:
		if (fld == "NT" or fld == "ND"):
			continue
		elif (flt(fld, precision) > 0.000001):
			total += flt(fld,2)
	return total

def get_equipment_details(equipment):
	return frappe.get_doc("Equipments", equipment).as_dict()

