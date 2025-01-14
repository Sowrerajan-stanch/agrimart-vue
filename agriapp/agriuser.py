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
        quantity = int(args.get('quantity'))
        user_id = args.get('user')
        
        user = frappe.get_doc('AgriUser', user_id)
        
        product = frappe.get_doc('Product', product_id)

        for cart_item in user.cart:
            if product.product_name == cart_item.ordered_product_name: 
                frappe.throw("Product Already in the cart!")
                return {
                    "error":"Product Already in the cart!"
                }

        user.append("cart", {
            "order_id": uuid.uuid4(),
            "ordered_date": datetime.now().strftime("%d-%m-%y"),
            "status": "unpaid",
            "total_amount": quantity * int(product.product_price),
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
        
    
        
    
        
        ordered_product = frappe.new_doc("Products_list")
        ordered_product.order_id = uuid.uuid4()
        ordered_product.ordered_date = datetime.now().strftime("%d-%m-%y/%H:%M:%S")
        ordered_product.total_amount = total
        ordered_product.status = "paid"
        ordered_product.user = user.name
        ordered_product.insert()

        for cart_item in user.cart:
            ordered_product.append("products",{
                "product_name":cart_item.ordered_product_name,
                "product_price":cart_item.ordered_product_price,
                "quantity": cart_item.ordred_quanity,
                "product_total_amount": int(cart_item.ordered_product_price) * int(cart_item.ordred_quanity)
            })

        ordered_product.save()

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
    orders = frappe.get_list("Products_list",pluck="name")
    user_orders = []
    for order in orders:
        o = frappe.get_doc("Products_list",order)
        if o.user == args.get("user"):
            user_orders.append(o)
    print(args.get("user"))
    return user_orders

@frappe.whitelist(allow_guest=True)
def fetch_cart(**args):
    user = frappe.get_doc("AgriUser",args.get("user"))
    return user.cart
	
@frappe.whitelist(allow_guest=True)
def fetch_order_detail(**args):
    order = frappe.get_doc("Products_list",{
        "order_id":args.get("order_id")
    })

    order_details = {
        "order_id":order.order_id,
        "ordered_date":order.ordered_date,
        "status":order.status,
        "total_amount":order.total_amount,
        "products":order.products,
    }
    return order_details

    