# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import base64
import binascii
import json
import requests

from six import string_types
import frappe
import frappe.client
import frappe.handler
from frappe import _
from frappe.utils.response import build_response
from frappe.utils.password import update_password as _update_password, check_password
  
@frappe.whitelist()
def buscarCliente( cliente = None ):
    txt			= "SELECT * FROM tabCustomer WHERE name like '%"+cliente+"%' or tax_id = '"+cliente+"' or mobile_no = '"+cliente+"' or email_id like '%"+cliente+"%';"
    data 		= frappe.db.sql(txt, as_dict=1)
    return data

@frappe.whitelist(allow_guest=False)
def vouchers(voucher,user=None):
	url 		= "http://localhost:5300/copilot/"+voucher
	payload 	= {}
	headers 	= {}
	response 	= requests.request("GET", url, headers=headers, data=payload)
	return response.json()

@frappe.whitelist(allow_guest=True)
def get_user_data(acces_token='',dominio="agendatusviajes.com"):
	
	url 		= f"https://{dominio}/api/sessions?access_token="+acces_token
	payload 	= {
		'server_key': 'eee4a212a9641f281fe0a2318b22eefe',
		'type'		: 'get'
	}
	files 			= []
	headers 		= {}
	response 		= requests.request("POST", url, headers=headers, data=payload, files=files)
	response 		= response.json()
	user_id 		= response["data"][0]["user_id"]
	name = frappe.get_list(doctype="Papas",fields=["name"],filters=[["user_id","=",user_id],["dominio","=",dominio]])

	if len(name)==0:
		doc = frappe.get_doc("Papas",user_id)
		user_id = doc.name 
	else:
		user_id = name[0].name
	return frappe.get_list(doctype="El VIaje De Promo", fields=["*"] ,or_filters=[["responsable1",'=',user_id],["responsable2",'=',user_id],["responsable3",'=',user_id]] )


@frappe.whitelist()
def crearusuarios_red_social(doc,event=None):
	
	nombres 		= doc.nombres.replace(" ","_")
	ap 				= doc.apellido_paterno.replace(" ","_")
	am 				= doc.apellido_materno.replace(" ","_")
	
	if doc.correo is None:
		doc.correo 	= (nombres+"_"+ap+"_"+am).lower()+"@santanaviajes.com"

	url 			= "https://"+doc.dominio+"/api/create-account"
	doc.full_name 	= doc.nombres + " " + doc.apellido_paterno + " " + doc.apellido_materno
	
	payload = {
		'server_key'		: 'eee4a212a9641f281fe0a2318b22eefe',
		'username'			: doc.telefono,
		'password'			: doc.contrasena,
		'email'				: doc.correo,
		'confirm_password'	: doc.contrasena,
		'gender'			: 'male',
		'phone_number'		: doc.telefono
	}
	files					= []
	headers 				= {}
	response 				= requests.request("POST", url, headers=headers, data=payload, files=files)
	doc.user_id				= response.json()["user_id"]
	
	try:
		url = "https://"+doc.dominio+"/api/update-user-data?access_token="+response.json()["access_token"]
		payload = {
			'server_key'	: 'eee4a212a9641f281fe0a2318b22eefe',
			'phone_number'	: doc.telefono,
			"first_name"	: doc.nombres,
			"last_name"		: doc.apellido_paterno + " " + doc.apellido_materno,
			"gender"		: "male"
		}
		files				= []
		headers 			= {}
		response 			= requests.request("POST", url, headers=headers, data=payload, files=files)
	except:
		pass
	return response

@frappe.whitelist()
def crearusuarios_red_social2(dominio="agendatusviajes.com"):
	docs = frappe.get_list(doctype="El VIaje De Promo", fields=["*"],filters=[["colegio","=","5a27ff465f"]], limit_page_length=200)
	for doc in docs:

		url						= f"https://{dominio}/api/create-account"
		doc.full_name 			= doc.nombres + " " + doc.primer_apellido + " " + doc.segundo_apellido
		payload = {
			'server_key' 		: "eee4a212a9641f281fe0a2318b22eefe",
			'username' 			: doc.dni_o_pasaporte,
			'password' 			: "elviajedepromo",
			'email' 			: doc.dni_o_pasaporte+"@santanaviajes.com",
			'confirm_password' 	: "elviajedepromo",
			'gender' 			: "male",
			'phone_number' 		: doc.celular
		}
		
		files					= []
		headers 				= {}
		response 				= requests.request("POST", url, headers=headers, data=payload, files=files)
		doc.user_id				= response.json()["user_id"]
		
		try:
		
			url 				= f"https://{dominio}/api/update-user-data?access_token="+response.json()["access_token"]	
		
			payload 			= {
				'server_key'	: "eee4a212a9641f281fe0a2318b22eefe",
				'phone_number'	: doc.celular,
				"first_name"	: doc.nombres,
				"last_name"		: doc.apellido_paterno + " " + doc.apellido_materno,
				"gender"		: "male" 
			}
		
			files 				= []
			headers 			= {}
			
			response 			= requests.request("POST", url, headers=headers, data=payload, files=files)
		except:
			pass
			
	return response

@frappe.whitelist()
def resetpass(user):
	papa=frappe.get_list("Papas",fields=["correo","dominio","contrasena"],filters=[['telefono',"=",user]])
	url = f"https://{papa[0].dominio}/api/reset_password"

	payload = {'server_key': 'eee4a212a9641f281fe0a2318b22eefe',
	'new_password': papa[0].contrasena,
	'username': user,
	'code': '1_b71ff04df24097c998747e66c58e50de',
	'email': papa[0].correo}
	files=[

	]
	headers = {
	'Cookie': '_us=1727305693; ad-con=%7B%26quot%3Bdate%26quot%3B%3A%26quot%3B2024-09-24%26quot%3B%2C%26quot%3Bads%26quot%3B%3A%5B%5D%7D; PHPSESSID=fs4adekoqofgsaodfdk4icq1nm; access=1; mode=day'
	}

	response = requests.request("POST", url, headers=headers, data=payload, files=files)

	return response.json()