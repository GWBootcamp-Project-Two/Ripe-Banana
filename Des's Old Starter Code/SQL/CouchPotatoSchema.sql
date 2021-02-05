DROP TABLE IF EXISTS gwsis.streamingservices ; 
CREATE TABLE IF NOT EXISTS gwsis.streamingservices (
  Service_ID INT(11) AUTO_INCREMENT,
  Service_Name VARCHAR(250),
  Service_Type VARCHAR(50),
  Service_Img VARCHAR(1000),
  Service_URL VARCHAR(100),
  Popular INT(10) DEFAULT 0,
  PRIMARY KEY (Service_ID));
   
DROP TABLE IF EXISTS gwsis.streamingservices ; 
CREATE TABLE IF NOT EXISTS gwsis.serviceselection (
  SRV_Selection_ID INT(11) AUTO_INCREMENT,
  Select_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
  Service_ID INT(50),
  PRIMARY KEY (SRV_Selection_ID)
  )
