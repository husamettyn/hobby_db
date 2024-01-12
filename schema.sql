
--USERS TABLE-------------------------------------------------------------
CREATE OR REPLACE FUNCTION checkAge(birthDate TIMESTAMP) 
RETURNS BOOLEAN AS $$
BEGIN
  RETURN birthDate <= NOW() - INTERVAL '18 years';
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS users (
  userID INT NOT NULL PRIMARY KEY,
  username VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(20) NOT NULL,
  name VARCHAR(20) NOT NULL,
  surname VARCHAR(20) NOT NULL,
  birthDate DATE NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  phoneNumber VARCHAR(13),
  address VARCHAR(255),
  CHECK (checkAge(birthDate) = TRUE),
  CONSTRAINT check_phoneNumber CHECK (phoneNumber LIKE '+905%')
);
-- DROP TABLE users

--PRODUCTS TABLE-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
  productID INT NOT NULL PRIMARY KEY,
  sellerID INT NOT NULL,
  productName VARCHAR(50) UNIQUE NOT NULL,
  description text,
  productCategory VARCHAR(30) NOT NULL,
  price NUMERIC NOT NULL,
  stockQuantity INT NOT NULL,
  soldQuantity INT,
  CHECK (stockQuantity >= 0),
  FOREIGN KEY (sellerID) 
    REFERENCES users (userID) ON DELETE CASCADE
);
-- DROP TABLE products

--SALES TABLE-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sales (
  saleID INT NOT NULL PRIMARY KEY,
  userID INT NOT NULL,
  productID INT NOT NULL,
  purchaseDate TIMESTAMP,
  quantity INT,
  totalAmount NUMERIC,
  FOREIGN KEY (userID) 
    REFERENCES users (userID),
  FOREIGN KEY (productID)
    REFERENCES products (productID)
);
-- DROP TABLE sales

--COMMENTS TABLE-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS comments(
  saleID INT NOT NULL PRIMARY KEY,
  rate INT NOT NULL,
  CHECK (rate BETWEEN 0 AND 5),
  FOREIGN KEY (saleID) 
    REFERENCES sales (saleID) ON DELETE CASCADE
);
-- DROP TABLE comments
