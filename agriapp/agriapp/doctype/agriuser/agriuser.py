# Copyright (c) 2024, Sowrerajan and contributors
# For license information, please see license.txt

import frappe
import uuid
from frappe.model.document import Document
from datetime import datetime

class AgriUser(Document):
	def validate(self):
		if not self.product:
			return
		
		if self.quantity <=0 :
			frappe.throw("Quantity Needs to be atleast 1")
				
		self.append("cart",{
			"order_id":uuid.uuid4()	,
			"ordered_date": str(datetime.now().strftime("%d-%m-%y")),
			"status":"unpaid",
			"total_amount": self.quantity * int(self.product_price),
			"ordered_product_name":self.product_name,
			"ordered_product_price":self.product_price,
			"ordred_quanity":self.quantity,
			"farmer_id":self.farmer_id
		})
		self.product = ''
		self.product_name = ''
		self.farmer_name = ''
		self.farmer_id = ''
		self.product_price = ''
		self.quantity = 0
		# self.save()
		total = 0
		for product in self.cart:
			total += int(product.total_amount)
		self.total = total


	@frappe.whitelist()
	def update_cart_and_ordered_products(doc):
		if len(doc.cart) <= 0:
			frappe.throw("The Cart is empty")
		

		doc = frappe.get_doc(frappe.parse_json(doc))
		
		total_amount = 0
		
		for cart_item in doc.cart:
			cart_item.status = 'paid'
			total_amount += int(cart_item.total_amount)
	
		for cart_item in doc.cart:
			doc.append("ordered_products", {
				"order_id": cart_item.order_id,
				"ordered_date": cart_item.ordered_date,
				"status": cart_item.status,
				"total_amount": cart_item.total_amount,
				"user": doc.name,
				"username": doc.full_name,
				"address": doc.address,
				"farmer":cart_item.farmer_id
			})
			farmer_doc = frappe.get_doc("Farmer", cart_item.farmer_id)
			buyer_detail = {
				"farmer_id": cart_item.farmer_id,
				"ordered_date": cart_item.ordered_date,
				"product_name": cart_item.ordered_product_name,
				"product_price": cart_item.ordered_product_price,
				"quantity": cart_item.ordred_quanity,
				"amount": cart_item.total_amount,
				"status":cart_item.status,
				"user":doc.name,
				"username":doc.full_name

			}

			farmer_doc.add_buyer_details(buyer_detail)
    
		
		
		doc.cart = []
		doc.total = 0
		
		doc.save()
		
	@frappe.whitelist()
	def add_to_cart():
		print("hello")
		return "Hello"





		
		

		

		

			

