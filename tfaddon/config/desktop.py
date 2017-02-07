# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "TRUFIL Addon",
			"color": "yellow",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("TRUFIL Addon")
		},
		{
			"module_name": "Back Office",
			"color": "yellow",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Back Office")
		}	
	]
