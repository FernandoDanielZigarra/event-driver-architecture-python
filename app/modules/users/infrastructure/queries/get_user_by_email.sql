SELECT id, username, email, first_name, last_name, created_at, updated_at
FROM users
WHERE email = $1;
