-- DATA FOR USERS TABLE -------------------------------------------------------------

-- userID, username,password,name,surname,birthDate,email,phoneNumber,address
INSERT INTO users VALUES (nextval('users_seq'), 'bhains0', 'wJ4/Fuj#M', 'Bentley', 'Hains', '1990-04-14', 'bhains0@gmail.com', '+905052196176', '4 Arizona Center Suite 53');
INSERT INTO users VALUES (nextval('users_seq'), 'gepdell1', 'gU0a*abc', 'Gerry', 'Epdell', '1982-06-05', 'gepdell1@hotmail.com', '+905479538603', '02133 Schmedeman Place Room 1440');
INSERT INTO users VALUES (nextval('users_seq'), 'jprobate2', 'wI9&2.Oe3', 'Jenn', 'Probate', '1998-05-14', 'jprobate2@gmail.com', '+905949670535', '357 Laurel Terrace Suite 32');
INSERT INTO users VALUES (nextval('users_seq'), 'gvuitte3', 'sD99AfctkPV', 'Gale', 'Vuitte', '1997-09-24', 'gvuitte3@hotmail.com', '+905039061650', '6190 Welch Avenue Suite 47');
INSERT INTO users VALUES (nextval('users_seq'), 'aluberti4', 'yG6h4n9J', 'Anson', 'Luberti', '1979-04-13', 'aluberti4@gmail.com', '+905128827985', '461 Golf Pass Suite 76');
INSERT INTO users VALUES (nextval('users_seq'), 'jcrudgington5', 'sX4Y2dLj', 'Johnnie', 'Crudgington', '1979-08-11', 'jcrudgington5@gmail.com', '+905274783013', '4 Lakewood Lane Room 76');
INSERT INTO users VALUES (nextval('users_seq'), 'bfrith6', 'wX3T,V7Q8yf0', 'Bea', 'Frith', '1991-01-13', 'bfrith6@hotmail.com', '+905373170290', '86133 Rigney Lane Room 1344');
INSERT INTO users VALUES (nextval('users_seq'), 'sflode7', 'gB7DrixW', 'Sloan', 'Flode', '2003-12-17', 'sflode7@hotmail.com', '+905238403886', '68 Redwing Plaza 10th Floor');
INSERT INTO users VALUES (nextval('users_seq'), 'thayller8', 'gA5XsX4K', 'Tirrell', 'Hayller', '1981-02-21', 'thayller8@hotmail.com', '+905823977143', '16 Butterfield Road Room 1350');
INSERT INTO users VALUES (nextval('users_seq'), 'lcheney9', 'hU4suf65u', 'Luther', 'Cheney', '2000-10-03', 'lcheney9@gmail.com', '+905117348173', '3 Birchwood Court Apt 924');
INSERT INTO users VALUES (nextval('users_seq'), 'rbellaya', 'vS5U&OWVVunn8', 'Rossie', 'Bellay', '1980-05-27', 'rbellaya@gmail.com', '+905654289080', '25 Pierstorff Court 19th Floor');
INSERT INTO users VALUES (nextval('users_seq'), 'alivockb', 'dV4C_4r_cy83', 'Alfonse', 'Livock', '1976-08-19', 'alivockb@gmail.com', '+905665061508', '9 Memorial Junction Suite 39');
INSERT INTO users VALUES (nextval('users_seq'), 'lwyantc', 'pY9cKYIC!', 'Loutitia', 'Wyant', '1989-06-10', 'lwyantc@gmail.com', '+905388860463', '63621 American Avenue 8th Floor');
INSERT INTO users VALUES (nextval('users_seq'), 'aclohissyd', 'sD0HXGHH?N', 'Alane', 'Clohissy', '2001-08-25', 'aclohissyd@gmail.com', '+905411824287', '898 Hudson Lane Room 1140');
INSERT INTO users VALUES (nextval('users_seq'), 'sspareye', 'uW9T1234wd', 'Stormy', 'Sparey', '1998-03-11', 'sspareye@gmail.com', '+905301894676', '4 Dapin Alley Apt 1490');


-- DATA FOR PRODUCTS TABLE -------------------------------------------------------------

-- productID, sellerID , productName, description, productCategory, price, stockQuantity, soldQuantity
INSERT INTO products VALUES (nextval('products_seq'), 1, 'macrame wall hanging', '30x50 dimensions, beige color, suitable for long-term use', 'wall decoration', 250.00, 2, 0);
INSERT INTO products VALUES (nextval('products_seq'), 2, 'landscape oil painting', '50x50 dimensions, soft colors', 'wall decoration', 570.00, 1, 0);
INSERT INTO products VALUES (nextval('products_seq'), 3, 'friendship bracelet', 'adjustable size, colors may vary depending on stock availability', 'jewelry', 20.00, 12, 5);
INSERT INTO products VALUES (nextval('products_seq'), 4, 'quartz beaded necklace', 'adjustable size, symbolizes power', 'jewelry', 160.00, 11, 3);
INSERT INTO products VALUES (nextval('products_seq'), 5, 'brass ring', 'fully handmade, tarnish free', 'jewelry', 240.00, 20, 2);
INSERT INTO products VALUES (nextval('products_seq'), 5, 'koi fish brass brooch', 'tarnish free, koi fish symbolize perseverance', 'jewelry', 350.00, 7, 2);
INSERT INTO products VALUES (nextval('products_seq'), 6, 'denim backpack', 'suitable for a 14" laptop', 'bag', 400.00, 5, 2);
INSERT INTO products VALUES (nextval('products_seq'), 1, 'macrame phone pouch', '20x14 dimensions, available in black and blue colors', 'bag', 50.00, 9, 1);
INSERT INTO products VALUES (nextval('products_seq'), 6, 'crossbody leather bag', '25x15 dimensions, adjustable size, unisex', 'bag', 450.00, 5, 3);
INSERT INTO products VALUES (nextval('products_seq'), 7, 'ocean-scented candle', '12 hours burning time', 'candle', 25.00, 27, 4);
INSERT INTO products VALUES (nextval('products_seq'), 2, 'natural soap', 'perfume-free', 'soap', 30.00, 25, 3);
INSERT INTO products VALUES (nextval('products_seq'), 7, 'sulfur soap', 'good for eczema, not suitable for the face', 'soap', 35.00, 43, 7);


-- DATA FOR SALES TABLE -------------------------------------------------------------

-- saleID, userID, productID, purchaseDate, quantity, totalAmount 
INSERT INTO sales VALUES (nextval('sales_seq'), 11, 3, '2023-12-01 12:55:55', 2, calculateTotalAmount(3, 2));
INSERT INTO sales VALUES (nextval('sales_seq'), 13, 3, '2023-11-25 14:30:12', 3, calculateTotalAmount(3, 3));
INSERT INTO sales VALUES (nextval('sales_seq'), 15, 4, '2023-11-26 12:55:55', 1, calculateTotalAmount(4, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 15, 6, '2023-12-16 18:23:20', 1, calculateTotalAmount(6, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 10, 4, '2023-12-17 16:27:12', 1, calculateTotalAmount(4, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 7, 4, '2023-11-12 22:50:55', 1, calculateTotalAmount(4, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 6, 5, '2023-10-01 23:13:12', 2, calculateTotalAmount(5, 2));
INSERT INTO sales VALUES (nextval('sales_seq'), 8, 6, '2023-10-25 21:45:15', 1, calculateTotalAmount(6, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 4, 7, '2023-10-14 16:24:34', 1, calculateTotalAmount(7, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 5, 7, '2023-10-18 19:25:34', 1, calculateTotalAmount(7, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 2, 8, '2023-10-18 17:45:34', 1, calculateTotalAmount(8, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 5, 9, '2023-10-18 15:25:34', 2, calculateTotalAmount(9, 2));
INSERT INTO sales VALUES (nextval('sales_seq'), 1, 9, '2023-10-15 19:25:34', 1, calculateTotalAmount(9, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 3, 10, '2023-10-19 19:25:34', 2, calculateTotalAmount(10, 2));
INSERT INTO sales VALUES (nextval('sales_seq'), 5, 10, '2023-11-18 22:25:34', 2, calculateTotalAmount(10, 2));
INSERT INTO sales VALUES (nextval('sales_seq'), 8, 11, '2023-12-18 19:25:34', 3, calculateTotalAmount(11, 3));
INSERT INTO sales VALUES (nextval('sales_seq'), 7, 12, '2023-11-14 20:25:34', 1, calculateTotalAmount(12, 1));
INSERT INTO sales VALUES (nextval('sales_seq'), 8, 12, '2023-10-20 12:25:34', 5, calculateTotalAmount(12, 5));
INSERT INTO sales VALUES (nextval('sales_seq'), 5, 12, '2023-10-05 14:25:34', 1, calculateTotalAmount(12, 1));

-- DATA FOR COMMENTS TABLE-------------------------------------------------------------

-- saleID, rate
INSERT INTO comments VALUES (1, 4);
INSERT INTO comments VALUES (2, 5);
INSERT INTO comments VALUES (3, 3);
INSERT INTO comments VALUES (4, 5);
INSERT INTO comments VALUES (5, 5);
INSERT INTO comments VALUES (6, 4);
INSERT INTO comments VALUES (7, 4);
INSERT INTO comments VALUES (8, 5);
INSERT INTO comments VALUES (9, 3);
INSERT INTO comments VALUES (10, 4);
INSERT INTO comments VALUES (11, 3);
INSERT INTO comments VALUES (12, 5);
INSERT INTO comments VALUES (13, 5);
INSERT INTO comments VALUES (14, 3);
INSERT INTO comments VALUES (15, 4);
INSERT INTO comments VALUES (16, 3);
INSERT INTO comments VALUES (17, 2);
INSERT INTO comments VALUES (18, 3);
INSERT INTO comments VALUES (19, 2);
