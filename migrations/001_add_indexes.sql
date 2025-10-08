-- Add index to improve the performance of the user dashboard query
CREATE INDEX idx_users_created_at ON users (created_at);
CREATE INDEX idx_users_status ON users (status);
CREATE INDEX idx_user_products_user_id ON user_products (user_id);
CREATE INDEX idx_user_products_product_id ON user_products (product_id);