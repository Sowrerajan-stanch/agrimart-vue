import frappe
import uuid
from datetime import datetime
from frappe.utils.password import passlibctx

@frappe.whitelist(allow_guest=True)
def authenticate_user(**args):
    email,password = args["email"],args["password"]
    user = frappe.get_doc("AgriUser",{
        "email":email
    })
    print(user.get_password("password"))
    if(not user or not (password == user.get_password("password"))):
        frappe.throw("Invalid Credentials!")
        return {"message":"Invalid Credentials!"}
    user_details = {
        "email":email,
        "fullname":user.full_name,
        "address":user.address,
        "userId":user.name
    }
    return {"message":"Login Succesfull","user_details":user_details}
    
    


@frappe.whitelist(allow_guest=True)
def add_to_cart(**args):
    try:
        product_id = args.get('product_id')
        quantity = args.get('quantity')
        total_amount = args.get('total_amount')
        user_id = args.get('user')
        
        user = frappe.get_doc('AgriUser', user_id)
        
        product = frappe.get_doc('Product', product_id)

        

        user.append("cart", {
            "order_id": uuid.uuid4(),
            "ordered_date": datetime.now().strftime("%d-%m-%y"),
            "status": "unpaid",
            "total_amount": total_amount,
            "ordered_product_name": product.product_name,
            "ordered_product_price": product.product_price,
            "ordred_quanity": quantity,
            "farmer_id": product.farmer,
            # "parent_doctype": "AgriUser",
            # "parent": user_id
        })
        
        user.save(ignore_permissions=True)
        frappe.db.commit()
        return {"message": "Product added to cart successfully"}
    except Exception as e:
        frappe.log_error(f"Error adding product to cart: {e}")
        return {"error": str(e)}
	# Order id
	# order date
	#status
	# Total Amount
	# product name
	# Product Price
	# Quantity
	# farmer name
@frappe.whitelist(allow_guest=True)
def pay_products(**args):
    try:
        user = frappe.get_doc("AgriUser",args["user"])
        total = 0
        
        for cart_item in user.cart:
            cart_item.status = "paid"
            total += int(cart_item.total_amount)
        
        for cart_item in user.cart:
            user.append("ordered_products", {
                "order_id": cart_item.order_id,
                "ordered_date": cart_item.ordered_date,
                "status": cart_item.status,
                "total_amount": cart_item.total_amount,
                "user": user.name,
                "username": user.full_name,
                "address": user.address,
                "farmer":cart_item.farmer_id
            })
            print(user.ordered_products)
            farmer_doc = frappe.get_doc("Farmer", cart_item.farmer_id)
            buyer_detail = {
                "farmer_id": cart_item.farmer_id,
                "ordered_date": cart_item.ordered_date,
                "product_name": cart_item.ordered_product_name,
                "product_price": cart_item.ordered_product_price,
                "quantity": cart_item.ordred_quanity,
                "amount": cart_item.total_amount,
                "status":cart_item.status,
                "user":user.name,
                "username":user.full_name
            }

            farmer_doc.add_buyer_details(buyer_detail)
        user.cart = []
        user.total = 0
        user.save()
        frappe.db.commit()
        return user
    except Exception as e:
        frappe.log_error(f"Error adding product to cart: {e}")
        return {"error": str(e)}

@frappe.whitelist(allow_guest=True)
def fetch_orders(**args):
    user = frappe.get_doc("AgriUser",args.get("user"))
    return user.ordered_products

@frappe.whitelist(allow_guest=True)
def fetch_cart(**args):
    user = frappe.get_doc("AgriUser",args.get("user"))
    return user.cart
	
    
    # Order_id
    # ordered_date
    # status
    # total_amount
    # user
    #farmer
    
    