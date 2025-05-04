SELECT * FROM Pharmacies;
INSERT INTO Pharmacies (Name, Address, Phone)
VALUES 
('صيدلية الرحمة', 'نجع حمادي - شارع الجمهورية', '01001234567'),
('صيدلية الشفاء', 'قنا - شارع مصطفى كامل', '01112223334');

SELECT PharmacyID, Name FROM Pharmacies;
SELECT PharmacyID, Name FROM Pharmacies;
SELECT PharmacyID, Name FROM Pharmacies WHERE PharmacyID = 1234;
SELECT PharmacyID, Name FROM Pharmacies WHERE PharmacyID = 1234;
INSERT INTO Pharmacies (Name, Address, Phone)
VALUES ('صيدلية جديدة', 'قنا - شارع التحرير', '01234567890');
INSERT INTO Drug_Stock (DrugID, SupplierID, PharmacyID, Quantity, DateSupplied)
VALUES 
(1, 1, 1234, 100, '2025-04-01'),
(2, 2, 1234, 50, '2025-04-03');
INSERT INTO Sales (DrugID, PharmacyID, QuantitySold, SaleDate)
VALUES 
(1, 1234, 20, '2025-04-15'),
(2, 1234, 10, '2025-04-18');
SELECT * FROM Drug_Stock;
SELECT * FROM Sales;
-- إدخال بيانات المخزون
INSERT INTO Drug_Stock (DrugID, SupplierID, PharmacyID, Quantity, DateSupplied)
VALUES 
(1, 1, 1234, 100, '2025-04-01'),
(2, 2, 1234, 50, '2025-04-03');

-- إدخال بيانات المبيعات
INSERT INTO Sales (DrugID, PharmacyID, QuantitySold, SaleDate)
VALUES 
(1, 1234, 20, '2025-04-15'),
(2, 1234, 10, '2025-04-18');
SELECT name FROM sys.databases;
