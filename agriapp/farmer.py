import frappe

@frappe.whitelist(allow_guest=True)
def authenticate_farmer(**args):
    email,password = args["email"],args["password"]
    farmer = frappe.get_doc("Farmer",{
        "email":email
    })
    print(farmer.get_password("password"))
    if(not farmer or not (password == farmer.get_password("password"))):
        frappe.throw("Invalid Credentials!")
        return {"message":"Invalid Credentials!"}
    farmer_details = {
        "email":email,
        "username":farmer.username,
        "address":farmer.location,
        "farmerId":farmer.name
    }
    return {"message":"Login Succesfull","farmer_details":farmer_details}

@frappe.whitelist(allow_guest=True)
def add_product(**args):
    product_name,product_desc,product_price = args.get("product_name") ,args.get("product_description"),args.get("product_price")
    farmer = args.get("farmer")

    farmer_doc = frappe.get_doc("Farmer",farmer)

    if not product_name or not product_desc or not product_price:
        frappe.throw("Please add product details correctly!")
    
    new_product = frappe.get_doc({
        "doctype":"Product",
        "product_name":product_name,
        "product_description":product_desc,
        "product_price":product_price,
        "farmer":farmer,
    })

    new_product.insert()

    farmer_doc.append("selling_products",{
        "product_name":product_name,
        "product_desc":product_desc,
        "product_price":product_price,
    })

    frappe.db.commit()
    farmer_doc.save()