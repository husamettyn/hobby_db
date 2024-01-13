
---------------------------------QUERIES--------------------------------------------
--Queries are listed in the order of use in the 'main.py' file.

--Lists a user matching the username and password entered
SELECT username, password 
FROM users 
WHERE username = 'admin' AND password = 'admin';

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


--Lists the name, ID and price of the selected product
SELECT p.productName, p.productID, p.price 
FROM products p 
WHERE 5 = p.productID;


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


--Lists the name and surname of the selected user
SELECT u.name, u.surname
FROM users u
WHERE 5 = u.userID;


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

