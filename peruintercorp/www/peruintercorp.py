# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _

no_cache=1
def get_context(context):
    context["nuestras_soluciones"] = frappe.get_doc("Nuestras Soluciones")
    context["pagina_principal"] = frappe.get_doc("Pagina principal")
    context["seccion_3"] = frappe.get_doc("Seccion 3")
    context["proyectos"] = frappe.get_list("Proyectos", fields=["*"],limit_page_length=4, ignore_permissions  = True)
    context["clientes"] = frappe.get_list("Clientes Web", fields=["*"],limit_page_length=12, ignore_permissions  = True)
    return context