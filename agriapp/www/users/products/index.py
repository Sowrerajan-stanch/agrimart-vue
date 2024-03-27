import frappe
def get_context(context):
	products = frappe.db.get_list("Product",pluck="name")
	context.products = products

	if frappe.local.form_dict:
		product = frappe.get_doc('Product',frappe.local.form_dict["id"])
		context.product = product
		return context
	return context

@frappe.whitelist(allow_guest=True)
def add_to_cart():
	print("Called")

