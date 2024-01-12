
--------------------------------------FUNCTIONS-----------------------------------

-- Update phone number and address
CREATE OR REPLACE FUNCTION updateUserInfo(p_userID INT, new_phoneNumber VARCHAR(13), new_address VARCHAR(255))
RETURNS VOID AS $$
BEGIN
  UPDATE users
  SET phoneNumber = new_phoneNumber, address = new_address
  WHERE userID = p_userID;
  
  IF NOT FOUND THEN
      RAISE EXCEPTION 'Kullanıcı bulunamadı!';
  END IF;

END;
$$ LANGUAGE plpgsql;

SELECT updateUserInfo(1, '+905519774022', '63 American Avenue 6th Floor');


-- Delete sales
CREATE OR REPLACE FUNCTION deleteSale(p_saleID INT, p_userID INT)
RETURNS VOID AS $$
BEGIN
    --users can delete their own sale records
    IF EXISTS (SELECT 1 FROM sales WHERE saleID = p_saleID AND userID = p_userID) THEN
        DELETE FROM sales WHERE saleID = p_saleID;
    ELSE
        RAISE EXCEPTION 'You cannot delete this sale record!';
    END IF;
END;
$$ LANGUAGE plpgsql;

SELECT deleteSale(1, 11);

-- Update or insert comment
CREATE OR REPLACE FUNCTION update_or_insert_comment(p_saleid integer, p_rate numeric)
RETURNS BOOLEAN AS $$
DECLARE
  comment_cursor CURSOR FOR SELECT * FROM comments WHERE saleid = p_saleid;
  comment_row comments%ROWTYPE;
  is_success BOOLEAN := false;
BEGIN
  OPEN comment_cursor;
  FETCH comment_cursor INTO comment_row;
  
  IF FOUND THEN
    -- Satır varsa, güncelle
    UPDATE comments SET rate = p_rate WHERE saleid = p_saleid;
    is_success := true;
  ELSE
    -- Satır yoksa, ekle
    INSERT INTO comments(saleid, rate) VALUES (p_saleid, p_rate);
    is_success := true;
  END IF;
  
  CLOSE comment_cursor;
  RETURN is_success;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_products_by_name(p_productname TEXT)
RETURNS SETOF product_type AS $$
BEGIN
    IF p_productname = ' ' THEN
        RETURN QUERY
        SELECT 
            productid, sellerid, productname, description, 
            productcategory, price, stockquantity, soldquantity
        FROM 
            products;
    ELSE
        RETURN QUERY
        SELECT 
            productid, sellerid, productname, description, 
            productcategory, price, stockquantity, soldquantity
        FROM 
            products
        WHERE 
            productname ILIKE '%' || p_productname || '%' 
			or productcategory ILIKE '%' || p_productname || '%' ;
    END IF;
END;
$$ LANGUAGE plpgsql;