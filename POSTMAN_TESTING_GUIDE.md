# Stock Alert System - Postman Testing Guide

## Base URL

\`\`\`
http://localhost:8000/api/
\`\`\`

## Authentication Flow

### 1. Register New User

**Method:** `POST`  
**URL:** `{{base_url}}/register/`  
**Headers:**
\`\`\`
Content-Type: application/json
\`\`\`
**Body (JSON):**
\`\`\`json
{
"username": "testuser",
"email": "test@example.com",
"password": "testpass123",
"password2": "testpass123"
}
\`\`\`
**Expected Response (201):**
\`\`\`json
{
"id": 1,
"username": "testuser",
"email": "test@example.com"
}
\`\`\`

### 2. Login User

**Method:** `POST`  
**URL:** `{{base_url}}/login/`  
**Headers:**
\`\`\`
Content-Type: application/json
\`\`\`
**Body (JSON):**
\`\`\`json
{
"username": "testuser",
"password": "testpass123"
}
\`\`\`
**Expected Response (200):**
\`\`\`json
{
"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
\`\`\`

**Important:** Copy the `access` token for subsequent requests!

### 3. Refresh Token

**Method:** `POST`  
**URL:** `{{base_url}}/token/refresh/`  
**Headers:**
\`\`\`
Content-Type: application/json
\`\`\`
**Body (JSON):**
\`\`\`json
{
"refresh": "your_refresh_token_here"
}
\`\`\`

## Stock Endpoints

### 4. Get All Stocks

**Method:** `GET`  
**URL:** `{{base_url}}/stocks/`  
**Headers:**
\`\`\`
Authorization: Bearer your_access_token_here
Content-Type: application/json
\`\`\`
**Expected Response (200):**
\`\`\`json
[
{
"id": 1,
"symbol": "AAPL",
"name": "Apple Inc.",
"current_price": "150.25",
"last_updated": "2024-01-15T10:30:00Z"
},
{
"id": 2,
"symbol": "GOOGL",
"name": "Alphabet Inc.",
"current_price": "2800.50",
"last_updated": "2024-01-15T10:30:00Z"
}
]
\`\`\`

## Alert Endpoints

### 5. Create Threshold Alert

**Method:** `POST`  
**URL:** `{{base_url}}/alerts/`  
**Headers:**
\`\`\`
Authorization: Bearer your_access_token_here
Content-Type: application/json
\`\`\`
**Body (JSON):**
\`\`\`json
{
"stock": 1,
"alert_type": "threshold",
"operator": ">",
"threshold_price": "160.00"
}
\`\`\`
**Expected Response (201):**
\`\`\`json
{
"id": 1,
"stock": 1,
"alert_type": "threshold",
"operator": ">",
"threshold_price": "160.00",
"duration_minutes": null,
"is_active": true,
"created_at": "2024-01-15T10:30:00Z"
}
\`\`\`

### 6. Create Duration Alert

**Method:** `POST`  
**URL:** `{{base_url}}/alerts/`  
**Headers:**
\`\`\`
Authorization: Bearer your_access_token_here
Content-Type: application/json
\`\`\`
**Body (JSON):**
\`\`\`json
{
"stock": 2,
"alert_type": "duration",
"operator": "<",
"threshold_price": "2700.00",
"duration_hours": 1
}
\`\`\`

### 7. Get User's Alerts

**Method:** `GET`  
**URL:** `{{base_url}}/alerts/`  
**Headers:**
\`\`\`
Authorization: Bearer your_access_token_here
Content-Type: application/json
\`\`\`
**Expected Response (200):**
\`\`\`json
[
{
"id": 1,
"stock": 1,
"alert_type": "threshold",
"operator": ">",
"target_price": "160.00",
"duration_hours": null,
"is_active": true,
"created_at": "2024-01-15T10:30:00Z"
}
]
\`\`\`

### 8. Get Specific Alert

**Method:** `GET`  
**URL:** `{{base_url}}/alerts/1/`  
**Headers:**
\`\`\`
Authorization: Bearer your_access_token_here
Content-Type: application/json
\`\`\`

### 9. Update Alert

**Method:** `PUT`  
**URL:** `{{base_url}}/alerts/1/`  
**Headers:**
\`\`\`
Authorization: Bearer your_access_token_here
Content-Type: application/json
\`\`\`
**Body (JSON):**
\`\`\`json
{
"stock": 1,
"alert_type": "threshold",
"operator": ">",
"threshold_price": "170.00"
}
\`\`\`

### 10. Delete Alert

**Method:** `DELETE`  
**URL:** `{{base_url}}/alerts/1/`  
**Headers:**
\`\`\`
Authorization: Bearer your_access_token_here
\`\`\`
**Expected Response:** `204 No Content`

### 11. Get Triggered Alerts

**Method:** `GET`  
**URL:** `{{base_url}}/triggered-alerts/`  
**Headers:**
\`\`\`
Authorization: Bearer your_access_token_here
Content-Type: application/json
\`\`\`
**Expected Response (200):**
\`\`\`json
[
{
"id": 1,
"alert": 1,
"stock_price_at_trigger": "165.50",
"triggered_at": "2024-01-15T11:00:00Z"
}
]
\`\`\`

## Postman Environment Variables

Create a Postman environment with these variables:

| Variable        | Value                       |
| --------------- | --------------------------- |
| `base_url`      | `http://localhost:8000/api` |
| `access_token`  | `your_jwt_access_token`     |
| `refresh_token` | `your_jwt_refresh_token`    |

## Testing Workflow

1. **Setup Environment:** Create environment variables
2. **Register User:** Create a new user account
3. **Login:** Get JWT tokens and save to environment
4. **Get Stocks:** View available stocks
5. **Create Alerts:** Set up price alerts
6. **View Alerts:** Check your active alerts
7. **Update/Delete:** Modify or remove alerts
8. **Check Triggered:** View triggered alerts

## Common Error Responses

### 401 Unauthorized

\`\`\`json
{
"detail": "Authentication credentials were not provided."
}
\`\`\`
**Solution:** Add Authorization header with Bearer token

### 400 Bad Request

\`\`\`json
{
"field_name": ["This field is required."]
}
\`\`\`
**Solution:** Check required fields in request body

### 404 Not Found

\`\`\`json
{
"detail": "Not found."
}
\`\`\`
**Solution:** Check if resource exists and belongs to authenticated user

## Alert Condition Options

| Condition | Description                          |
| --------- | ------------------------------------ |
| `>`       | Trigger when price goes above target |
| `<`       | Trigger when price goes below target |

## Alert Type Options

| Type        | Description            | Required Fields                                          |
| ----------- | ---------------------- | -------------------------------------------------------- |
| `threshold` | Immediate trigger      | `stock`, `operator`, `threshold_price`                   |
| `duration`  | Trigger after duration | `stock`, `operator`, `threshold_price`, `duration_hours` |

## Tips for Testing

1. **Use Environment Variables:** Set up base_url and tokens as variables
2. **Test Authentication First:** Always start with register/login
3. **Save Tokens:** Use Postman's test scripts to auto-save tokens
4. **Test Error Cases:** Try invalid data to test error handling
5. **Check Response Status:** Verify HTTP status codes match expectations

## Auto-Save Token Script

Add this to your login request's "Tests" tab:
\`\`\`javascript
if (pm.response.code === 200) {
const response = pm.response.json();
pm.environment.set("access_token", response.access);
pm.environment.set("refresh_token", response.refresh);
}
\`\`\`

This will automatically save tokens to your environment variables.
