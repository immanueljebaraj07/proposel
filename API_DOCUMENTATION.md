# API Documentation

## Authentication Endpoints

### Login
- **Endpoint:** `POST /api/auth/login`
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "string"
  }
  ```
- **Response:**
  - **200 OK**: Returns user data and token
  - **401 Unauthorized**: Incorrect credentials
- **Example cURL:**
  ```bash
  curl -X POST http://example.com/api/auth/login -d '{"email":"user@example.com", "password":"string"}' -H 'Content-Type: application/json'
  ```

## Product Endpoints

### Get Products
- **Endpoint:** `GET /api/products`
- **Response:**
  - **200 OK**: Returns a list of products
- **Example cURL:**
  ```bash
  curl -X GET http://example.com/api/products
  ```

### Create Product
- **Endpoint:** `POST /api/products`
- **Request Body:**
  ```json
  {
    "name": "Product Name",
    "price": 100.0,
    "description": "Product Description"
  }
  ```
- **Response:**
  - **201 Created**: Returns created product
- **Example cURL:**
  ```bash
  curl -X POST http://example.com/api/products -d '{"name":"Product Name", "price":100.0, "description":"Product Description"}' -H 'Content-Type: application/json'
  ```

## Proposal Endpoints

### Create Proposal
- **Endpoint:** `POST /api/proposals`
- **Request Body:**
  ```json
  {
    "productId": 1,
    "amount": 200,
    "message": "Proposal Message"
  }
  ```
- **Response:**
  - **201 Created**: Returns created proposal
- **Example cURL:**
  ```bash
  curl -X POST http://example.com/api/proposals -d '{"productId":1, "amount":200, "message":"Proposal Message"}' -H 'Content-Type: application/json'
  ```

## Error Handling
- **Error Format:**
  ```json
  {
    "error": "Error message"
  }
  ```
- **Common Errors:**
  - **400 Bad Request**: Validation errors
  - **404 Not Found**: Resource not found
  - **500 Internal Server Error**: Server error

# Conclusion
This documentation provides an overview of the API endpoints available for authentication, product management, and proposal handling. For deeper integration, ensure to check out the error handling section and examples provided above.