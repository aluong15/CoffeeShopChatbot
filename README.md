# Coffee Shop Chatbot

## Overview

This repository features a Flask-based chatbot created for a conceptual coffee shop, integrated with Dialogflow for natural language understanding. The chatbot manages customer orders, tracks their status, and uses context management to add or remove items from an ongoing order.

## Features

- **Order Management:**
  - Start a new order
  - Add items to the order
  - Remove items from the order (In Work)
  - Place the order (In Work)
  - Cancel the order (In Work)

- **Product Information:**
  - Provides details about coffee, tea, and pastries (Future Enhancement)
  - Suggests products and ingredients (Future Enhancement)

## Technologies Used

- **Dialogflow:** Provides natural language understanding to process and understand user intents.
- **Flask:** A micro web framework for handling HTTP requests.
- **ngrok:** Exposes local servers to the internet for testing (optional for deployment).
- **MySQL:** Database for storing product and order information.
- **Python:** Programming language used for developing the chatbot.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/coffee-shop-chatbot.git
   cd coffee-shop-chatbot

2. **Set Up the Database:**

  Ensure you have MySQL installed on your system.
  Create a database for the chatbot.

  ## Tables Used

### `products`
- **Description:** Table with sample data of products sold in the coffee shop.
- **Columns:**
  - **productID:** Unique identifier for each product.
  - **productName:** Name of the product.
  - **productDescription:** General description of the product.
  - **price:** Unit price of the product.

### `orders`
- **Description:** Table with sample customer order information.
- **Columns:**
  - **orderID:** Unique identifier for each order.
  - **customerName:** Name of the customer who placed the order.
  - **orderStatus:** Status of the order ("New", "In Progress", "Complete").

### `orderDetails`
- **Description:** Table that tracks the products and respective quantities for each order.
- **Columns:**
  - **orderDetailsID:** Unique identifier for the number of a particular product in the specified order.
  - **orderID:** Corresponding order number for the order's details (linked to `orders` table).
  - **productID:** ID of the product being ordered (linked to `products` table).
  - **quantity:** Number of products in the order details.


3. **Configure the Application:**

   - Edit `mysqlconnector.py` with your database connection details.
   - Update other configurations as necessary for your environment.

4. **Run the Flask Application:**

   ```bash
   python app.py

5. **Expose Local Server (Optional):**

  If you need to expose your local server using ngrok, run:

  ```bash
  ngrok http 5000

  Ensure you have ngrok installed. Replace '5000' with your Flask port if different.

6. **Interact with the Chatbot:**

   - Use the provided endpoint (e.g., `http://localhost:5000`) to interact with the chatbot.
   - To set up fulfillment in Dialogflow:
     - Go to the [Dialogflow Console](https://dialogflow.cloud.google.com/).
     - Navigate to your agent and go to the **Fulfillment** section in the left-hand menu.
     - Enable the **Webhook** option and enter your ngrok or public server URL (e.g., `https://<your-ngrok-id>.ngrok.io/webhook/`).
     - Save the changes.
     - Ensure that your Dialogflow intents are configured to use this webhook for fulfillment by checking the **Fulfillment** checkbox in each intent’s **Action and Parameters** section.
   - You can test the chatbot using tools like Postman or directly via a web interface if available.

