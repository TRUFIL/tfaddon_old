# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime, date, time


__version__ = '1.0.0'
__title__ = "TRUFIL Addon"

# Function to generate unique serial number
def generate_unique_serial_no():
	sl_no = datetime.now()
	return "#" + sl_no.strftime('%Y%m%d%H%M%S')

def cur_year():
	cur_date = datetime.now()
	return cur_date.strftime('%Y')