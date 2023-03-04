CREATE DATABASE ScooRentDB;

USE ScooRentDB;

CREATE TABLE Users(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    phoneNumber NVARCHAR(15),
    firstName NVARCHAR(50),
    lastName NVARCHAR(50),
    email NVARCHAR(100),
    registrationDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);  -- Create users table.

CREATE TABLE Admins(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    username NVARCHAR(30),
    password NVARCHAR(150),
    canGet BOOLEAN NOT NULL DEFAULT TRUE,
    canCreate BOOLEAN NOT NULL DEFAULT TRUE,
    canDelete BOOLEAN NOT NULL DEFAULT TRUE,
    registrationDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);  -- Create admins table.

CREATE TABLE Scooters(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    scooterName nvarchar(100),
    isAvailable BOOLEAN NOT NULL DEFAULT true,
    isBooked BOOLEAN NOT NULL DEFAULT false,
    bookedByUserID INT DEFAULT NULL ,
    bookedAtDate TIMESTAMP
);  -- Create scooters table;

CREATE TABLE Cards(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ownerID INT,
    cardImagePath NVARCHAR(300),
    cardBankName NVARCHAR(35),
    hashedCardData NVARCHAR(150),
    fourLastDigits INT
);  -- Create cards table.

CREATE TABLE Orders(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    customerID INT,
    orderAmount decimal(12, 2),
    isActive BOOLEAN NOT NULL DEFAULT true,
    orderStartDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    orderFinishDate TIMESTAMP
);  -- Create orders table.