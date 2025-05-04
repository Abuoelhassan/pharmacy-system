CREATE TABLE Pharmacies (
    PharmacyID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Address NVARCHAR(255),
    Phone VARCHAR(15),
    Governorate NVARCHAR(50) DEFAULT 'قنا'
);
CREATE TABLE Drugs (
    DrugID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Description NVARCHAR(255),
    ExpiryDate DATE,
    Price DECIMAL(10,2),
    QuantityInStock INT
);
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    ContactNumber VARCHAR(15),
    Address NVARCHAR(255)
);
CREATE TABLE Drug_Stock (
    StockID INT PRIMARY KEY IDENTITY(1,1),
    DrugID INT FOREIGN KEY REFERENCES Drugs(DrugID),
    SupplierID INT FOREIGN KEY REFERENCES Suppliers(SupplierID),
    PharmacyID INT FOREIGN KEY REFERENCES Pharmacies(PharmacyID),
    Quantity INT NOT NULL,
    DateSupplied DATE NOT NULL
);
CREATE TABLE Sales (
    SaleID INT PRIMARY KEY IDENTITY(1,1),
    DrugID INT FOREIGN KEY REFERENCES Drugs(DrugID),
    PharmacyID INT FOREIGN KEY REFERENCES Pharmacies(PharmacyID),
    QuantitySold INT NOT NULL,
    SaleDate DATE NOT NULL
);
CREATE TABLE Admins (
    AdminID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    FullName NVARCHAR(100),
    Role NVARCHAR(50) DEFAULT 'مدير'
);
INSERT INTO Drugs (Name, Description, ExpiryDate, Price, QuantityInStock)
VALUES 
('باراسيتامول', 'خافض حرارة ومسكن للآلام', '2025-12-31', 15.00, 200),
('أموكسيسيلين', 'مضاد حيوي واسع المجال', '2026-06-15', 25.00, 150);
INSERT INTO Suppliers (Name, ContactNumber, Address)
VALUES 
('شركة فارما جروب', '01234567890', 'القاهرة - مدينة نصر'),
('النيل للأدوية', '01099887766', 'الإسكندرية - سيدي جابر');
INSERT INTO Suppliers (Name, ContactNumber, Address)
VALUES 
('شركة فارما جروب', '01234567890', 'القاهرة - مدينة نصر'),
('النيل للأدوية', '01099887766', 'الإسكندرية - سيدي جابر');
INSERT INTO Drug_Stock (DrugID, SupplierID, PharmacyID, Quantity, DateSupplied)
VALUES 
(1, 1, 1234, 100, '2025-04-01'),
(2, 2, 1234, 50, '2025-04-03');

INSERT INTO Sales (DrugID, PharmacyID, QuantitySold, SaleDate)
VALUES 
(1, 1234, 20, '2025-04-15'),
(2, 1234, 10, '2025-04-18');

INSERT INTO Admins (Username, PasswordHash, FullName)
VALUES 
('admin', '123456', 'رحيم أحمد');
SELECT PharmacyID, Name FROM Pharmacies WHERE PharmacyID = 1234;
SET IDENTITY_INSERT Pharmacies ON;
  INSERT INTO Pharmacies (PharmacyID, Name, Address, Phone)
VALUES (1234, 'صيدلية جديدة', 'قنا - شارع التحرير', '01234567890');
SET IDENTITY_INSERT Pharmacies OFF;
INSERT INTO Drug_Stock (DrugID, SupplierID, PharmacyID, Quantity, DateSupplied)
VALUES 
(1, 1, 1234, 100, '2025-04-01'),
(2, 2, 1234, 50, '2025-04-03');
INSERT INTO Sales (DrugID, PharmacyID, QuantitySold, SaleDate)
VALUES 
(1, 1234, 20, '2025-04-15'),
(2, 1234, 10, '2025-04-18');
SELECT name FROM sys.databases;
