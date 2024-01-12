
---------------------------------QUERIES--------------------------------------------

--Seçilen ürüne verilen ortalama puanı listeler
SELECT AVG(rate)
FROM comments c, sales s
WHERE s.saleID = c.saleID AND c.saleID = <istenenIDdegeriYazılacak> --??
GROUP BY s.productID ;

--Ortalama puanı 3'ten fazla olan ürünleri listeler
SELECT p.productName, AVG(c.rate)
FROM comments c, sales s, products p
WHERE s.saleID = c.saleID AND s.productID = p.productID  --??
GROUP BY p.productID 
HAVING AVG(c.rate) > 3
ORDER BY AVG(c.rate) desc

--İstenen kategorideki ürünleri lsteler
SELECT * FROM products WHERE productCategory = 'jewelry';
