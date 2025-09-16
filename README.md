# AIChatVault 

A secure chat platform with robust authentication and administrative controls.

## Features

- 🔐 User Authentication (Login/Register)
- 💬 AI Chat Interface
- 👥 Role-based Access Control (User/Admin)
- ⚡ Fast API Backend
- 🔄 Rate Limiting for Guest Users

## API Endpoints

### Authentication Endpoints
```http
POST /auth/register
```
- Register a new user
- Body: `{ "username": string, "email": string, "password": string}`
- Returns: User object

```http
POST /auth/token
```
- Login and get access token
- Form data: `username`, `password`
- Returns: `{ "access_token": string, "token_type": "bearer" }`

```http
GET /auth/me
```
- Get current user profile
- Requires: Bearer token
- Returns: User object

### Chat Endpoints
```http
POST /chat/
```
- Send message to AI
- Requires: Bearer token (optional)
- Body: `{ "message": string, "request_count": number }`
- Returns: `{ "response": string }`
- Note: Guest users limited to 5 requests

### Admin Endpoints
Requires admin role and bearer token

```http
GET /admin/users
```
- Get all users
- Returns: List of user objects

```http
GET /admin/users/{user_id}
```
- Get specific user details
- Returns: Detailed user object with logs

```http
PATCH /admin/users/{user_id}/deactivate
```
- Deactivate a user
- Returns: Success message

```http
PATCH /admin/users/{user_id}/reactivate
```
- Reactivate a user
- Returns: Success message

```http
DELETE /admin/delete-user/{user_id}
```
- Delete a user
- Returns: Success message

```http
GET /admin/logs
```
- Get all request logs
- Returns: List of log entries

```http
DELETE /admin/delete_logs
```
- Delete all request logs
- Returns: Success message with count

### Response Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error
