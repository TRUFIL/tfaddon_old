# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _


__version__ = '1.0.0'
__title__ = "TRUFIL Addon"

# Function to generate unique serial number
def generate_unique_serial_no():
	from datetime import datetime, date, time
	sl_no = datetime.now()
	return "#" + sl_no.strftime('%Y%m%d%H%M%S')

