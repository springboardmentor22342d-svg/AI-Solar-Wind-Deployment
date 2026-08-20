"""
app/auth – Authentication module.

Handles:
  - JWT token creation and verification
  - Password hashing (bcrypt via passlib)
  - User login and registration logic
  - OAuth2 password flow (FastAPI security)

Key SQL concept: Users table uses a Primary Key (PK) – a unique ID for
every registered user, ensuring no duplicates in the database.
"""
