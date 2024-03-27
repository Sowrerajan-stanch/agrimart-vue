# Copyright (c) 2024, Sowrerajan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Farmer(Document):
	@frappe.whitelist()
	def add_product(doc):
		doc = frappe.get_doc(frappe.parse_json(doc))
		if not doc.product_name or not doc.product_desc or not doc.product_price:
			frappe.throw("Please add product details correctly!")
		new_product = frappe.get_doc({
			"doctype":"Product",
			"product_name":doc.product_name,
			"product_description":doc.product_desc,
			"product_price":doc.product_price,
			"farmer":doc.name,
			"farmer_name":doc.username
		})

		new_product.insert()

		doc.append("selling_products",{
			"product_name":doc.product_name,
			"product_desc":doc.product_desc,
			"product_price":doc.product_price,
		})

		doc.product_name = ''
		doc.product_desc = ''
		doc.product_price = ''

		doc.save()

	def add_buyer_details(self,buyer_details):	
		farmer = frappe.get_doc("Farmer",buyer_details["farmer_id"])
		farmer.append("users",{
			"user": buyer_details["user"],
            "username": buyer_details["username"],
            "ordered_date": buyer_details["ordered_date"],
            "product_name": buyer_details["product_name"],
            "product_price": buyer_details["product_price"],
            "quantity": buyer_details["quantity"],
            "amount": buyer_details["amount"],
			"status":buyer_details["status"]
		})
		farmer.save()
		frappe.db.commit()