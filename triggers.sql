
-------------------------------------TRIGGERS---------------------------------------

-- Delete related comments
--triggers when a user deletes a sale record
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

--Set purchase date of new sale with current date and time
CREATE OR REPLACE FUNCTION update_purchase_date()
RETURNS TRIGGER AS $$
BEGIN
    -- Yeni satışın satın alma tarihini güncel tarih ve saat ile ayarla
    NEW.purchasedate := TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_purchase_date
BEFORE INSERT ON sales
FOR EACH ROW
EXECUTE FUNCTION update_purchase_date();

--Updates stock quantity when a product is inserted
CREATE OR REPLACE FUNCTION updateQuantity()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET stockQuantity = stockQuantity + NEW.stockQuantity
    WHERE productID = NEW.productID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER updateQuantityTrigger
AFTER INSERT ON products
FOR EACH ROW 
EXECUTE FUNCTION updateQuantity();

