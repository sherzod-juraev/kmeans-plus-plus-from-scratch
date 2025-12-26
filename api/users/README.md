# Users API

This module handles user management including signup, authentication, updating, reading, and deleting users.

## Table of Contents

- [Endpoints](#endpoints)
- - [Signup](#1-signup)
- - [Refresh token](#2-refresh-token)
- - [Get user](#3-get-user)
- - [Full update user](#4-full-update-user)
- - [Partial update user](#5-partial-update-user)
- - [Delete user](#6-delete-user)
- [Model / Schemas](#models--schemas)

## Endpoints

### 1. **Signup**

- **URL:** `/signup`
- **Method:** `POST`
- **Summary:** Create a new user
- **Request Body:** `OAuth2PasswordRequestForm`

```json
  {
    "username": "string",
    "password": "string"
  }
```


- **Response:**

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

- **Notes**:
- - Sets a refresh_token cookie with httponly flag.

### 2. **Refresh Token**

- **URL:** `/refresh`
- **Method:** `POST`
- **Summary:** Refresh access token using a valid refresh token cookie
- **Response:**

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### 3. **Get User**

- **URL:** `/`
- **Method:** `GET`
- **Summary:** Get current user info
- **Dependencies:** Requires valid access token
- **Response Model:** `UserRead`

```json
{
  "id": "uuid",
  "username": "string",
  "full_name": "string | null"
}
```

### 4. **Full Update User**

- **URL:** `/`
- **Method:** `PUT`
- **Summary:** Fully update user data
- **Request Body:** `UserUpdateFull`

```json
{
  "username": "string",
  "full_name": "string"
}
```
- **Response Model:** `UserRead`

### 5. **Partial Update User**

- **URL:** `/`
- **Method:** `PATCH`
- **Summary:** Partially update user data
- **Request Body:** `UserUpdatePartial`

```json
{
  "username": "string | null",
  "full_name": "string | null"
}
```
- **Response Model:** `UserRead`

### 6. **Delete User**

- **URL:** `/`
- **Method:** `DELETE`
- **Summary:** Delete the user
- **Request Body:** `UserDelete`

```json
{
  "username": "string",
  "password": "string"
}
```
- **Notes:** Deletes the user and removes `refresh_token` cookie.
- **Response:** `204 No Content`

## Models / Schemas

- **UserCreate:** `username`, `password` (validated)
- **UserUpdateFull:** `username`, `full_name` (validated)
- **UserUpdatePartial:** `username?`, `full_name?` (validated, optional)
- **UserRead:** `id`, `username`, `full_name?`
- **UserDelete:** `username`, `password` (validated)
- **TokenResponse:** `access_token`, `token_type` (default "bearer")

## Notes

- All password fields are hashed before storing in the database.
- Username must match pattern: `^[a-z0-9_-]{3,50}$`
- Password must match pattern: `^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,25}$`
- Full name allows letters, spaces, and hyphens only, 1–100 characters.
- Access tokens are required for all operations except signup and token refresh.