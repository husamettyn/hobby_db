
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





