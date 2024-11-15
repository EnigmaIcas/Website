-- Alumni Table
CREATE TABLE Alumni (
  ID(P) INT PRIMARY KEY,
  FirstName VARCHAR(50),
  LastName VARCHAR(50),
  CGPA DECIMAL(4,2),
  UniversityID(F) INT
);

-- Universities Table
CREATE TABLE Universities (
  UniversityID(P) INT PRIMARY KEY,
  UniversityName VARCHAR(100),
  Country VARCHAR(100),
  City VARCHAR(100),
  NoOfStudents INT
);

-- Members Table
CREATE TABLE Members (
  MemberID(P) INT PRIMARY KEY,
  StudentID(F) INT,
  DivisionID(F) INT,
  Role VARCHAR(50)
);

-- ProjectAllotment Table
CREATE TABLE ProjectAllotment (
  AllotmentID(P) INT PRIMARY KEY,
  ProjectID(F) INT,
  MemberID(F) INT,
  Role VARCHAR(50)
);

-- Projects Table
CREATE TABLE Projects (
  ProjectID(P) INT PRIMARY KEY,
  ProjectName VARCHAR(100),
  ProjectDescription TEXT,
  StartDate DATE,
  EndDate DATE
);

-- Funding Table
CREATE TABLE Funding (
  FID(P) INT PRIMARY KEY,
  ProjectID(F) INT,
  Amount DECIMAL(10,2),
  MaterialName VARCHAR(100),
  Quantity INT
);