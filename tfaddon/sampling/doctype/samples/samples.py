# -*- coding: utf-8 -*-
# Copyright (c) 2017, DGSOL InfoTech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
#from frappe.model.document import Document
from frappe import _
import tfaddon
from frappe.utils import cstr, flt, getdate, comma_and, cint
from tfaddon.controllers.tf_status_updater import TFStatusUpdater

class Samples(TFStatusUpdater):
	def onload(self):
		count=self.get_bottle_count_in_bag() + self.no_of_containers
		frappe.msgprint(_("Currently there are {0} bottles in bag no {1}".format(count,self.bag_no)))

	def before_insert(self):
		pass

	def on_update(self):
		pass

	def before_submit(self):
		self.status = "Collected"

	def on_submit(self):
		update_container_status(self.name,self.status)

	def before_update_after_submit(self):
		if self.has_disposed_details():
			self.status = "Disposed"
		elif self.has_completed_job_order():
			self.status = "Completed"
		elif self.has_open_job_order():
			self.status = "In Process"
		elif self.has_complete_details():
			self.status = "Received"
		elif self.has_verification_details():
			self.status = "Verified"

	def on_update_after_submit(self):
		update_container_status(self.name,self.status)

	def before_cancel(self):
		self.status = "Cancelled"

	def on_cancel(self):
		update_container_status(self.name,self.status)

	def validate(self):
		self.validate_bag_availability()
		self.validate_bag_capacity()
		self.validate_mandatory()

	def validate_bag_availability(self):
		if frappe.db.count("Sample Dispatch Register",{"bag_no":self.bag_no,"docstatus":1}) > 0:
			frappe.throw(_("Bag No {0} already dispatched".format(self.bag_no)))

	def validate_bag_capacity(self):
		if (self.get_bottle_count_in_bag() + self.no_of_containers) > 21:
			frappe.throw(_("Bag No {0} cannot accomodate {1} more containers".format(self.bag_no,self.no_of_containers)))

	def validate_mandatory(self):
		if (self.docstatus == 0):
			if (self.collected_by == "TRUFIL"):
				if not (self.sampling_request):
					frappe.throw(_("Sampling Request is required"))
				if not (self.sampler_name):
					frappe.throw(_("Sampler Name is required"))
			elif (self.collected_by == "Customer"):
				if not (self.sales_order):
					frappe.throw(_("Sales Order is required"))
			else:
				frappe.throw(_("Collected By is required"))

			if self.smp_source == "Equipment":
				if not self.smp_type:
					frappe.throw(_("Please select appropriate Sample Type"))
				if not self.smp_point:
					frappe.throw(_("Please select appropriate Sampling Point"))
			elif self.smp_source == "Storage":
				if self.smp_type != "Transformer Oil":
					frappe.throw(_("Sample Type must be Transformer Oil if sample is collected from Storage"))
			else:
				frappe.throw(_("Please select appropriate Sample Taken From"))

			if not self.weather_condition:
				frappe.throw(_("Please select appropriate Weather Condition"))

			if not self.smp_condition:
				frappe.throw(_("Please select appropriate Sampling Condition"))

			if not self.eq_owner:
				frappe.throw(_("Equipment/Location Owner is required"))

	def has_verification_details(self):
		if self.equipment and self.location:
			return 1
		else:
			return 0

	def has_complete_details(self):
		if (self.has_verification_details() and self.receipt_date and self.material and self.laboratory and self.receipt_condition):
			return 1
		else:
			return 0

	def has_dispatch_details(self):
		if (self.dispatch_id):
			return 1
		else:
			return 0

	def has_open_job_order(self):
		if (frappe.db.exists("Oil Test Reports", {"sample":self.name})):
			return 1
		else:
			return 0

	def has_completed_job_order(self):
		# Temporarily completion is declared by Certificate No availability
		if (self.certificate):
			self.status = "Completed"
			update_container_status(self.name,self.status)
			return True
		else:
			return False

	def has_disposed_details(self):
		return False

	def get_no_of_bottles(self):
		return frappe.db.count("Sampling Containers", filters={"parent":self.name})

	def generate_sample_id(self):
		container_list = [d.name for d in frappe.get_all('Sampling Containers', 
			filters = {'parent': self.name})]
		if container_list:
			return '-'.join(container_list)

	def update_child_doc_status(self):
		bottles = frappe.get_all("Sampling Containers", filters = {"parent":self.name})
		for bot in bottles:
			doc = frappe.get_doc({"doctype":"Sampling Containers", "name":bot})
			doc.status = self.status
			#doc.save()

	def declare_disposed(self, args):
		frappe.db.set(self, 'disposed_date', args["disposed_date"])
		frappe.db.set(self, 'status', 'Disposed')
		update_container_status(self.name,self.status)

	def declare_received(self, args):
		rdate = args["receipt_date"]
		sample_id = self.generate_new_sample_id()
		if getdate(rdate) > getdate() or getdate(rdate) < getdate(self.collection_date):
			frappe.throw(_("Received Date cannot be before collection date or future date"))
		frappe.db.set(self, 'receipt_date', args["receipt_date"])
		frappe.db.set(self, 'laboratory', args["laboratory"])
		frappe.db.set(self, 'material', args["material"])
		frappe.db.set(self, 'smp_condition', args["smp_condition"])
		frappe.db.set(self, 'sample_remarks', args["sample_remarks"])
		frappe.db.set(self, 'receipt_condition', args["receipt_condition"])
		frappe.db.set(self, 'status', 'Received')
		frappe.db.set(self, 'sample_id', sample_id)
		update_container_status(self.name,self.status)

	def generate_new_sample_id(self):
		return frappe.model.naming.make_autoname("TL/SM/.YY./", "Samples")

	def get_bottle_count_in_bag(self):
		if self.is_new(): 
			name=""
		else:
			name=self.name
		return frappe.db.sql("""select count(*) from `tabSampling Containers` as c  
			join `tabSamples` as p on p.name=c.parent 
			where p.bag_no = %s and p.name != %s 
			order by p.bag_no,c.parent;""",(self.bag_no,name))[0][0]

# Other Functiona
def update_container_status(docname, status):
	bottles = frappe.get_all("Sampling Containers", filters = {"parent":docname})
	for bot in bottles:
		frappe.db.set_value("Sampling Containers",bot,"status",status)

