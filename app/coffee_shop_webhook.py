from flask import app, jsonify, request
from app.mysqlconnector import create_connection
        
# order.start intent
def start_ongoing_order(session_id, connection, cursor, req):
    # Retrieve customer name from context
    contexts = req.get('queryResult').get('outputContexts', [])
    customer_name = None
    for context in contexts:
        if context.get('name').endswith('customer-name'):
            customer_name = context.get('parameters', {}).get('name')
            break

    print(f"Started ongoing order for customer {customer_name} with session_id {session_id}.")

    try:
        # Get order_id based on session_id
        order_id = get_order_id(session_id,cursor)

        # First, delete the details associated with the order
        cursor.execute('DELETE FROM orderDetails WHERE order_id = %s;', (order_id,))
        print(f"Deleted order details associated with session {session_id}.")

        # Then clear any previous orders associated with session
        cursor.execute('DELETE FROM orders WHERE session_id = %s;', (session_id,))
        print(f"Deleted previous orders associated with session {session_id}.")
        
        cursor.execute('INSERT INTO orders (session_id, customer_name, order_status) VALUES (%s, %s, %s)', (session_id, customer_name, 'Pending'))
        print(f"Created new order for {customer_name} with status Pending.")
    
        # Commit new order
        connection.commit()
        print("New order created in database!")

    except Exception as e:
        # Rollback in case of error
        connection.rollback()
        print(f"Error: {e}")
        return jsonify({'fulfillmentText': 'An error occurred while processing your order. Please try again.'})

    return jsonify({'fulfillmentText': 'Great! Let\’s get started with your new order.\nWe are currently offering coffee, tea, and pastries. What would you like to add to your order?'})

# order.add intent
def add_to_order(session_id, connection, cursor, req):
    products = req.get('queryResult').get('parameters').get('product_name')
    print(f"Products in order: {products}.")
    quantities = req.get('queryResult').get('parameters').get('number')
    print(f"Quantities of products in order: {quantities}.")

    if not products:
        return jsonify({'fulfillmentText': "I didn't catch what you wanted to order. Please try again."})
    
    # Convert quantities to integers to avoid float issues
    quantities = [int(q) for q in quantities]
    print(f"Converted Quantities: {quantities}")

    # check quantities list matches length of products list
    if len(quantities) < len(products):
        quantities += [1] * (len(products) - len(quantities))

    # get order_id using session_id
    order_id = get_order_id(session_id, cursor)
    if order_id is None:
        return jsonify({'fulfillmentText': 'No order found for the session. Please start a new order.'})
    print(f"Order ID: {order_id}")

    try:
        # iterate through each product, quantity
        for product, quantity in zip(products, quantities):
            cursor.execute('SELECT product_id FROM products WHERE product_name = %s;', (product,))
            product_id_tuple = cursor.fetchone()
            print(f"product id tuple: {product_id_tuple}")

            if product_id_tuple:
                # Unpack the tuple to get actual product_id value
                product_id = product_id_tuple[0]
                print(f"product id: {product_id}")
                cursor.execute('INSERT INTO orderDetails (order_id, product_id, quantity) VALUES (%s, %s, %s);', (order_id, product_id, quantity))
                print(f"Added {quantity} of {product_id} to order {order_id}.")
            else:
                return jsonify({'fulfillmentText': f"Sorry, {product} is not available."})

        # Commit the transaction
        connection.commit()
        print("Committed the added items to order in database!")

    except Exception as e:
        # Rollback in case of error
        connection.rollback()
        print(f"Error: {e}")
        return jsonify({'fulfillmentText': 'An error occurred while processing your order. Please try again.'})

    return jsonify({'fulfillmentText': f"Added {', '.join(f'{q} {p}(s)' for p, q in zip(products, quantities))} to your order. Anything else?"})


# order.remove intent
def remove_from_order(session_id, connection, cursor, req):
    products = req.get('queryResult').get('parameters').get('product')
    quantities = req.get('queryResult').get('parameters').get('product')

    if not products:
        return jsonify({'fulfillmentText': "I didn't catch what you wanted to remove. Please try again."})

    # check quantities list matches length of products list
    if len(quantities) < len(products):
        quantities += [1] * (len(products) - len(quantities))   

    # get order_id using session_id
    order_id = get_order_id(session_id, cursor)


    try:
        # iterate through each product, quantity
        for product, quantity in zip(products, quantities):
            cursor.execute('SELECT product_id FROM products WHERE product_name = %s;', (product,))
            product_id_tuple = cursor.fetchone()

            if product_id_tuple:
                # Unpack the tuple to get actual product_id value
                product_id = product_id_tuple[0]
                # if the product desired to remove does not exist in the ongoing-order, return message for user to try again
                product_exists = cursor.execute('SELECT EXISTS ( SELECT 1 FROM orderDetails WHERE session_id = %s;', (session_id,))
                if not product_exists:
                    return jsonify({'fulfillmentText': f"Sorry, {product} is not available to remove from your order. Please try again."})
            # elif 
                # if the quantity desired to remove is greater than the current quantity of the product, return message stating max amount that can be removed, and remove orderDetail for product_id
                
            else:
                return jsonify({'fulfillmentText': f"Sorry, {product} is not available."})
            
        # Commit the transaction
        connection.commit()
        print("Committed the items removed from order to database!")
    
    except Exception as e:
        # Rollback in case of error
        connection.rollback()
        print(f"Error: {e}")
        return jsonify({'fulfillmentText': 'An error occurred while processing your order. Please try again.'})
    
    return jsonify({'fulfillmentText': f"Removed {', '.join(f'{q} {p}(s)' for p, q in zip(products, quantities))} to your order. Anything else?"})

# order.place intent
def place_order(session_id, connection, cursor, req):
    return req

# order.cancel intent
def cancel_ongoing_order(session_id, connection, cursor, req):
    return req

# order.status intent
def check_order_status(cursor, req):
    # extract the order number from the request
    order_number = req.get('queryResult').get('parameters').get('order_number')

    # connect to db
    # connection = create_connection()
    # cursor = connection.cursor()

    # query order status
    query = "SELECT order_status FROM orders WHERE order_id = %s"
    cursor.execute(query, (order_number,))
    result = cursor.fetchone()

    if result:
        order_status = result[0]
        response_text = f"Your order with ID {order_number} is current {order_status}."
    else:
        response_text = f"Sorry, I couldn't find an order with ID {order_number}."
    
    # close cursor and connection
    # cursor.close()
    # connection.close()

    return jsonify({'fulfillmentText': response_text})

# get order_id from session_id
def get_order_id (session_id, cursor):
    cursor.execute('SELECT order_id FROM orders WHERE session_id = %s;', (session_id,))
    order_id_tuple = cursor.fetchone()

    if order_id_tuple:
        # Return the first element of the tuple, which is the actual order_id
        return order_id_tuple[0]
    return None # no order_id is found