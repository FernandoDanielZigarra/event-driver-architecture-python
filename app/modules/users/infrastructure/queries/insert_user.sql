INSERT INTO users (username, email, first_name, last_name, hashed_password, created_at, updated_at)
VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
RETURNING id, username, email, first_name, last_name, created_at, updated_at;
