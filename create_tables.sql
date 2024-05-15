-- Create table for purchases
CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    store TEXT,
    date DATE,
    total_price DECIMAL(10, 2) NOT NULL
);

-- Create table for products
CREATE TABLE products (
    id SERIAL PRIMARY KEY, 
    purchase_id INT,
    name TEXT,
    category TEXT,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES purchases(id)
);
