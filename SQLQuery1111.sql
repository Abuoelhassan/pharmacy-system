-- Create Database
CREATE DATABASE QenaPharmacies;
GO

-- Use the created database
USE QenaPharmacies;
GO

-- Create Pharmacies Table
CREATE TABLE Pharmacies (
    PharmacyID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Address NVARCHAR(200) NOT NULL,
    Phone NVARCHAR(15)
);
GO

-- Create Warehouses Table
CREATE TABLE Warehouses (
    WarehouseID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Address NVARCHAR(200) NOT NULL,
    Capacity INT NOT NULL
);
GO

-- Create Medicines Table
CREATE TABLE Medicines (
    MedicineID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Quantity INT NOT NULL,
    LocationType NVARCHAR(50) NOT NULL, -- 'Pharmacy' or 'Warehouse'
    LocationID INT NOT NULL -- References PharmacyID or WarehouseID
);
GO