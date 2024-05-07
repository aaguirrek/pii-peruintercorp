# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import base64
import binascii
import json

from six import string_types
from six.moves.urllib.parse import urlencode, urlparse
from pyfcm import FCMNotification

import frappe
import frappe.client
import frappe.handler
from frappe import _
from frappe.utils.response import build_response
from frappe.utils.password import update_password as _update_password, check_password
  
@frappe.whitelist()
def buscarCliente( cliente = None ):
    txt="SELECT * FROM tabCustomer WHERE name like '%"+cliente+"%' or tax_id = '"+cliente+"' or mobile_no = '"+cliente+"' or email_id like '%"+cliente+"%';"
    data = frappe.db.sql(txt, as_dict=1)
    return data


@frappe.whitelist(allow_guest=False)
def vouchers(voucher,user):
	frappe.set_user(user)
	url = "http://localhost:5300/copilot/"+voucher
	payload = {}
	headers = {}
	response = requests.request("GET", url, headers=headers, data=payload)
	return response.json()