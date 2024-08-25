from flask import Flask, request, jsonify
import os

from app.coffee_shop_webhook import add_to_order, cancel_ongoing_order, check_order_status, place_order, remove_from_order, start_ongoing_order
from app.mysqlconnector import create_connection


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, )
    print("Created App!")
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/test_post', methods=['POST'])
    def test_post():
        return 'POST request successful!'

    @app.route('/', methods=['POST'])
    def webhook():
        print("created webhook")
        req = request.get_json(silent=True, force=True)

        print("Connected to webhook!")

        if req is None:
            return jsonify({'error': 'Invalid request format = None'}), 400
        
        print(f"Received request: {req}")

        # get session ID from Dialogflow to store ongoing order data in a db
        session_path = req.get('session')
        if session_path:
            session_id = session_path.split('/')[-1]
            print(f"session_id = {session_id}")

        intent = req.get('queryResult').get('intent').get('displayName')

        # connect to db
        connection = create_connection()
        cursor = connection.cursor()

        try:
            # handle intents
            match intent:
                case 'order.start':
                    return start_ongoing_order(session_id, connection, cursor, req)
                case 'order.add - context: ongoing-order':
                    return add_to_order(session_id, connection, cursor, req)
                case 'order.remove - context: ongoing-order':
                    return remove_from_order(session_id, connection, cursor, req)
                case 'order.place - context: ongoing-order':
                    return place_order(session_id, connection, cursor)
                case 'order.cancel - context: ongoing-order':
                    return cancel_ongoing_order(session_id, connection, cursor, req)
                case 'order.status':
                    return check_order_status(cursor, req)
                case _:
                    return jsonify({'fulfillmentText': 'Intent not recognized.'})
        finally:
            # close cursor and connection
            print("Connection closing!")
            cursor.close()
            connection.close()
            
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
