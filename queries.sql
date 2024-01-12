
---------------------------------QUERIES--------------------------------------------
--Queries are listed in the order of use in the 'main.py' file.

--Lists a user matching the username and password entered
SELECT username, password 
FROM users 
WHERE username = 'admin' AND password = 'admin';

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
        WHERE productName ILIKE '%handmade%' or 
        productCategory ILIKE '%wall decoration%' ;
    END IF;
END;
$$ LANGUAGE plpgsql;

--UNION
SELECT username, userid, password 
FROM users 
WHERE username = 'admin'
  UNION
SELECT NULL, NULL, password 
FROM users 
WHERE username = 'admin'
LIMIT 1;

--Lists the email, phone number and address of the selected user
SELECT email, phoneNumber, address
FROM users 
WHERE userid = 2;

--Update user info
UPDATE users 
SET password = 'admin'
where users.userID = 16;

UPDATE users 
SET phonenumber = '+905654289080' 
WHERE users.userID = 16;

UPDATE users 
SET email = 'adminNew@admin.com'
WHERE users.userID = 16;

UPDATE users 
SET address = 'YTU Library'
WHERE users.userID = 16;

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

--Lists the name, ID and price of the selected product
SELECT p.productName, p.productID, p.price 
FROM products p 
WHERE 5 = p.productID;

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

-- Update stock quantity of the selected product
UPDATE products 
SET stockQuantity = stockQuantity - 1
WHERE productID = 5;

--Lists the sales made by the requested user and the product information
SELECT p.productName, s.purchaseDate, s.quantity, s.totalAmount, s.saleid
FROM sales s, products p 
WHERE p.productID = s.productID AND 5 = s.userID;

--Deletes selected sale
DELETE FROM sales 
WHERE saleID = 5;

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

--Lists the name and surname of the selected user
SELECT u.name, u.surname
FROM users u
WHERE 5 = u.userID;

--VIEW
CREATE VIEW product_view AS
SELECT * FROM products;

--AGGREGATION
--Lists the average rate given to the selected product
SELECT s.productID, AVG(rate)
FROM comments c, sales s
WHERE s.saleID = c.saleID AND c.saleID = 5
GROUP BY s.productID ;

--Lists products with an average rate above 3
SELECT p.productName, AVG(c.rate)
FROM comments c, sales s, products p
WHERE s.saleID = c.saleID AND s.productID = p.productID  --??
GROUP BY p.productID 
HAVING AVG(c.rate) > 3
ORDER BY AVG(c.rate) desc

