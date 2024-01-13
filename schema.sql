
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

--VIEW
CREATE VIEW product_view AS
SELECT * FROM products;

---SEQUENCES-------------------------------------------------------------
CREATE SEQUENCE users_seq
START 1
INCREMENT 1
OWNED BY users.userID;

CREATE SEQUENCE products_seq
START 1
INCREMENT 1
OWNED BY products.productID;

CREATE SEQUENCE sales_seq 
START 1
INCREMENT 1
OWNED BY sales.saleID;

--RECORD
CREATE TYPE product_type AS (
    productid INT,
    sellerid INT,
    productname VARCHAR(50),
    description TEXT,
    productcategory VARCHAR(30),
    price NUMERIC,
    stockquantity INT,
    soldquantity INT
);

--FUNCTION
--Lists products in the desired category or name
CREATE OR REPLACE FUNCTION get_products_by_name(p_productName TEXT)
RETURNS SETOF product_type AS $$
BEGIN
    IF p_productName = ' ' THEN
        RETURN QUERY
        SELECT productID, sellerID, productName, description, 
        productCategory, price, stockQuantity, soldQuantity
        FROM products;
    ELSE
        RETURN QUERY
        SELECT productID, sellerID, productName, description, 
        productCategory, price, stockQuantity, soldQuantity
        FROM products
        WHERE productName ILIKE '%' || p_productName || '%' or 
        productCategory ILIKE '%' || p_productName || '%';
    END IF;
END;
$$ LANGUAGE plpgsql;

--FUNCTION
--Returns the total price of the product
CREATE OR REPLACE FUNCTION calculateTotalAmount(p_productID INT,p_quantity INT) 
RETURNS NUMERIC AS $$
DECLARE
  v_price NUMERIC;
BEGIN
  SELECT price INTO v_price 
  FROM products 
  WHERE productID = p_productID;
  RETURN v_price * p_quantity;
END;
$$ LANGUAGE plpgsql;


--TRIGGER
--Set purchase date of new sale with current date and time
CREATE OR REPLACE FUNCTION update_purchase_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.purchasedate := TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_purchase_date
BEFORE INSERT ON sales
FOR EACH ROW
EXECUTE FUNCTION update_purchase_date();

--TRIGGER
--Deletes comments related to the deleted sale
CREATE OR REPLACE FUNCTION deleteRelatedComments()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM comments
    WHERE saleID = OLD.saleID;  
      RAISE NOTICE 'Comment for sale ID % has been deleted', OLD.saleID;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER deleteRelatedCommentsTrigger
AFTER DELETE 
ON sales
FOR EACH ROW
EXECUTE FUNCTION deleteRelatedComments();


--CURSOR, FUNCTION
--Updates if there is a comment, if not inserts
CREATE OR REPLACE FUNCTION update_or_insert_comment(p_saleID integer, p_rate numeric)
RETURNS BOOLEAN AS $$
DECLARE
  comment_cursor CURSOR FOR SELECT * FROM comments WHERE saleID = p_saleID;
  comment_row comments%ROWTYPE;
  is_success BOOLEAN := false;
BEGIN
  OPEN comment_cursor;
  FETCH comment_cursor INTO comment_row;

  IF FOUND THEN
    -- Update if row exists
    UPDATE comments SET rate = p_rate WHERE saleID = p_saleID;
    is_success := true;
  ELSE
    -- Insert if not exist
    INSERT INTO comments(saleID, rate) VALUES (p_saleID, p_rate);
    is_success := true;
  END IF;

  CLOSE comment_cursor;
  RETURN is_success;
END;
$$ LANGUAGE plpgsql;