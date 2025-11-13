-- ============================================================
-- DATABASE CREATION
-- ============================================================

CREATE DATABASE IF NOT EXISTS donationmanagementsystem;
USE donationmanagementsystem;

-- ============================================================
-- TABLE CREATION (DDL)
-- ============================================================

CREATE TABLE donor (
    DonorID VARCHAR(50) PRIMARY KEY,
    FN VARCHAR(50),
    MN VARCHAR(50),
    LN VARCHAR(50),
    email VARCHAR(100),
    h_no VARCHAR(20),
    strret VARCHAR(100),
    pincod VARCHAR(10),
    area VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    total_donated DECIMAL(12,2)
);

CREATE TABLE donor_phone (
    Donor_id VARCHAR(50),
    ph_no VARCHAR(15),
    FOREIGN KEY (Donor_id) REFERENCES donor(DonorID)
);

CREATE TABLE beneficiary (
    b_id VARCHAR(50) PRIMARY KEY,
    FN VARCHAR(50),
    MN VARCHAR(50),
    LN VARCHAR(50),
    DOB DATE,
    Age INT,
    Need_type VARCHAR(100),
    phone VARCHAR(15),
    state VARCHAR(50),
    city VARCHAR(50),
    area VARCHAR(50),
    pin VARCHAR(10),
    strret VARCHAR(100),
    H_no VARCHAR(20)
);

CREATE TABLE organisation (
    O_Id VARCHAR(50) PRIMARY KEY,
    Org_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    contact_no VARCHAR(15)
);

CREATE TABLE registration_details (
    Reg_no VARCHAR(50) PRIMARY KEY,
    PAN_no VARCHAR(20),
    Date_of_Reg DATE,
    O_Id VARCHAR(50),
    FOREIGN KEY (O_Id) REFERENCES organisation(O_Id)
);

CREATE TABLE campaign (
    C_Id VARCHAR(50) PRIMARY KEY,
    C_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    target_amt DECIMAL(12,2),
    collected_amt DECIMAL(12,2),
    O_Id VARCHAR(50),
    FOREIGN KEY (O_Id) REFERENCES organisation(O_Id)
);

CREATE TABLE donation (
    Dot_id VARCHAR(50) PRIMARY KEY,
    Donation_type VARCHAR(50),
    Donation_date DATE,
    amt DECIMAL(12,2),
    Description TEXT,
    tax_deductible_amt DECIMAL(12,2),
    Donor_id VARCHAR(50),
    C_id VARCHAR(50),
    FOREIGN KEY (Donor_id) REFERENCES donor(DonorID),
    FOREIGN KEY (C_id) REFERENCES campaign(C_Id)
);

CREATE TABLE donation_item (
    Item_no VARCHAR(50) PRIMARY KEY,
    Item_description TEXT,
    Item_quantity INT,
    Unit VARCHAR(20)
);

CREATE TABLE distribution (
    DistId VARCHAR(50) PRIMARY KEY,
    Dist_date DATE,
    Quantity INT,
    Status VARCHAR(50),
    Dot_ID VARCHAR(50),
    Reg_no VARCHAR(50),
    FOREIGN KEY (Dot_ID) REFERENCES donation(Dot_id),
    FOREIGN KEY (Reg_no) REFERENCES registration_details(Reg_no)
);

-- ============================================================
-- SAMPLE INSERTS
-- ============================================================

INSERT INTO donor VALUES ("DNR123", "John", "", "Doe", "john@gmail.com",
"12A", "Street 1", "560001", "MG Road", "Bangalore", "Karnataka", 0);

INSERT INTO donor_phone VALUES ("DNR123", "9876543210");

INSERT INTO organisation VALUES ("ORG01", "Helping Hands", "Bangalore", "Karnataka", "9123456789");

INSERT INTO registration_details VALUES ("REG01", "ABCDE1234F", "2024-07-01", "ORG01");

INSERT INTO campaign VALUES ("CMP89", "Food Drive", "2024-12-01",
"2025-02-01", 100000, 0, "ORG01");

INSERT INTO donation VALUES ("DOT110", "Cash", "2025-01-10", 5000,
"Test Donation", 200, "DNR123", "CMP89");

-- ============================================================
-- STORED FUNCTION
-- ============================================================

DELIMITER $$

CREATE FUNCTION total_donation_by_donor(p_donor_id VARCHAR(50))
RETURNS DECIMAL(12,2)
DETERMINISTIC
RETURN (SELECT IFNULL(SUM(amt),0) FROM donation WHERE Donor_id = p_donor_id);

$$
DELIMITER ;

-- ============================================================
-- STORED PROCEDURE
-- ============================================================

DELIMITER $$

CREATE PROCEDURE add_donation_proc(
  IN p_Dot_id VARCHAR(50),
  IN p_Donation_type VARCHAR(50),
  IN p_Donation_date DATE,
  IN p_amt DECIMAL(12,2),
  IN p_Description TEXT,
  IN p_tax DECIMAL(12,2),
  IN p_Donor_id VARCHAR(50),
  IN p_C_id VARCHAR(50)
)
BEGIN
  INSERT INTO donation (Dot_id, Donation_type, Donation_date, amt, Description,
                        tax_deductible_amt, Donor_id, C_id)
  VALUES (p_Dot_id, p_Donation_type, p_Donation_date, p_amt,
          p_Description, p_tax, p_Donor_id, p_C_id);

  IF p_C_id IS NOT NULL THEN
    UPDATE campaign
    SET collected_amt = collected_amt + p_amt
    WHERE C_Id = p_C_id;
  END IF;
END $$

DELIMITER ;

-- ============================================================
-- TRIGGER
-- ============================================================

DELIMITER $$

CREATE TRIGGER trg_after_insert_donation
AFTER INSERT ON donation
FOR EACH ROW
BEGIN
  UPDATE donor
  SET total_donated = IFNULL(total_donated,0) + NEW.amt
  WHERE DonorID = NEW.Donor_id;
END $$

DELIMITER ;

-- ============================================================
-- NESTED QUERY
-- ============================================================

SELECT DonorID, FN, total_donated
FROM donor
WHERE total_donated > (SELECT AVG(total_donated) FROM donor);

-- ============================================================
-- JOIN QUERY
-- ============================================================

SELECT d.FN, dn.amt, c.C_name
FROM donation dn
JOIN donor d ON dn.Donor_id = d.DonorID
JOIN campaign c ON dn.C_id = c.C_Id;

-- ============================================================
-- AGGREGATE QUERY
-- ============================================================

SELECT Donor_id, COUNT(*), SUM(amt)
FROM donation
GROUP BY Donor_id;

