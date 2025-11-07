-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: club_and_event
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `club`
--

DROP TABLE IF EXISTS `club`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `club` (
  `club_id` int NOT NULL,
  `club_name` varchar(100) DEFAULT NULL,
  `club_type` varchar(50) DEFAULT NULL,
  `date_formed` date DEFAULT NULL,
  `description` text,
  `faculty_id` int DEFAULT NULL,
  PRIMARY KEY (`club_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `club_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `facultyadvisor` (`faculty_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `club`
--

LOCK TABLES `club` WRITE;
/*!40000 ALTER TABLE `club` DISABLE KEYS */;
INSERT INTO `club` VALUES (1,'Tech Innovators','Technical','2019-06-10','Club for coding and hackathons',1),(2,'E-Cell','Entrepreneurship','2020-02-15','Club for startups and business ideas',2),(3,'MechArena','Mechanical','2018-08-25','Club for mechanical engineers',3),(4,'InfoSec Hub','Cybersecurity','2021-11-05','Cybersecurity awareness club',4),(5,'Green Builders','Civil','2022-01-12','Sustainable construction enthusiasts',5);
/*!40000 ALTER TABLE `club` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `event_id` int NOT NULL,
  `event_name` varchar(100) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `venue_id` int DEFAULT NULL,
  `event_type` varchar(50) DEFAULT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  `club_id` int DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `venue_id` (`venue_id`),
  KEY `club_id` (`club_id`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`venue_id`) REFERENCES `venue` (`venue_id`),
  CONSTRAINT `event_ibfk_2` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'Hackathon 2025','2025-09-20',2,'Technical',1500.00,1),(2,'Startup Pitch','2025-10-05',1,'Entrepreneurship',1200.00,2),(3,'AutoCAD Workshop','2025-09-15',5,'Workshop',800.00,3),(4,'Cyber Security Drill','2025-11-10',4,'Awareness',1000.00,4),(5,'Green Expo','2025-12-01',3,'Exhibition',2000.00,5),(9,'Shazam','2025-11-20',2,'Cultural',50000.00,1),(100,'Shazam','2025-11-20',2,'Cultural',50000.00,1),(101,'TechFest','2025-11-20',1,'Technical',50000.00,1),(102,'Shazam','2025-11-20',2,'Cultural',50000.00,1);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventregistration`
--

DROP TABLE IF EXISTS `eventregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventregistration` (
  `reg_id` int NOT NULL,
  `reg_date` date DEFAULT NULL,
  `attendance_status` varchar(50) DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  `event_id` int DEFAULT NULL,
  PRIMARY KEY (`reg_id`),
  KEY `student_id` (`student_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `eventregistration_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`),
  CONSTRAINT `eventregistration_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventregistration`
--

LOCK TABLES `eventregistration` WRITE;
/*!40000 ALTER TABLE `eventregistration` DISABLE KEYS */;
INSERT INTO `eventregistration` VALUES (1,'2025-09-05','Confirmed',1,1),(2,'2025-09-06','Pending',2,1),(3,'2025-09-07','Confirmed',3,2),(4,'2025-09-08','Confirmed',4,3),(5,'2025-09-09','Pending',5,4),(6,'2025-10-26','Pending',2,101),(7,'2025-10-27','Pending',3,4),(8,'2025-10-27','Pending',2,3),(9,'2025-10-27','Pending',5,4),(10,'2025-10-27','Pending',3,4),(11,'2025-10-27','Pending',2,2);
/*!40000 ALTER TABLE `eventregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facultyadvisor`
--

DROP TABLE IF EXISTS `facultyadvisor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facultyadvisor` (
  `faculty_id` int NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`faculty_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facultyadvisor`
--

LOCK TABLES `facultyadvisor` WRITE;
/*!40000 ALTER TABLE `facultyadvisor` DISABLE KEYS */;
INSERT INTO `facultyadvisor` VALUES (1,'Shankar','M','Hegde','Computer Science','shankar.hegde@college.edu'),(2,'Savitha','R','Pai','Electronics','savitha.pai@college.edu'),(3,'Vinay','K','Bhat','Mechanical','vinay.bhat@college.edu'),(4,'Lakshmi','S','Kiran','Information Science','lakshmi.kiran@college.edu'),(5,'Arun','P','Reddy','Civil','arun.reddy@college.edu');
/*!40000 ALTER TABLE `facultyadvisor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership`
--

DROP TABLE IF EXISTS `membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membership` (
  `membership_id` int NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `join_date` date DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  `club_id` int DEFAULT NULL,
  PRIMARY KEY (`membership_id`),
  KEY `student_id` (`student_id`),
  KEY `club_id` (`club_id`),
  CONSTRAINT `membership_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`),
  CONSTRAINT `membership_ibfk_2` FOREIGN KEY (`club_id`) REFERENCES `club` (`club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership`
--

LOCK TABLES `membership` WRITE;
/*!40000 ALTER TABLE `membership` DISABLE KEYS */;
INSERT INTO `membership` VALUES (1,'Active','2023-01-15','President',1,1),(2,'Active','2023-02-20','Member',2,1),(3,'Active','2023-03-10','Secretary',3,2),(4,'Inactive','2022-09-18','Treasurer',4,3),(5,'Active','2024-04-01','Member',5,4);
/*!40000 ALTER TABLE `membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `payment_mode` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `reg_id` int DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `reg_id` (`reg_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`reg_id`) REFERENCES `eventregistration` (`reg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,1500.00,'2025-09-07','UPI','Paid',1),(2,0.00,'2025-09-08','N/A','Pending',2),(3,1200.00,'2025-09-09','Card','Paid',3),(4,800.00,'2025-09-10','Cash','Paid',4),(5,0.00,'2025-09-11','N/A','Pending',5),(6,50000.00,'2025-10-26','UPI','Pending',6),(7,1000.00,'2025-10-27','UPI','Pending',7),(8,800.00,'2025-10-27','UPI','Pending',8),(9,1000.00,'2025-10-27','UPI','Pending',9),(10,1000.00,'2025-10-27','UPI','Pending',10),(11,1200.00,'2025-10-27','UPI','Pending',11);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsor`
--

DROP TABLE IF EXISTS `sponsor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsor` (
  `sponsor_id` int NOT NULL,
  `sponsor_name` varchar(100) DEFAULT NULL,
  `industry_type` varchar(50) DEFAULT NULL,
  `contact_phone` varchar(15) DEFAULT NULL,
  `contact_mail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sponsor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsor`
--

LOCK TABLES `sponsor` WRITE;
/*!40000 ALTER TABLE `sponsor` DISABLE KEYS */;
INSERT INTO `sponsor` VALUES (1,'Infosys','IT','9845000001','contact@infosys.com'),(2,'Wipro','IT','9845000002','contact@wipro.com'),(3,'Biocon','Biotech','9845000003','contact@biocon.com'),(4,'MTR Foods','Food','9845000004','contact@mtr.com'),(5,'Bosch India','Engineering','9845000005','contact@bosch.com');
/*!40000 ALTER TABLE `sponsor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsoredby`
--

DROP TABLE IF EXISTS `sponsoredby`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsoredby` (
  `event_id` int NOT NULL,
  `sponsor_id` int NOT NULL,
  PRIMARY KEY (`event_id`,`sponsor_id`),
  KEY `sponsor_id` (`sponsor_id`),
  CONSTRAINT `sponsoredby_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`),
  CONSTRAINT `sponsoredby_ibfk_2` FOREIGN KEY (`sponsor_id`) REFERENCES `sponsor` (`sponsor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsoredby`
--

LOCK TABLES `sponsoredby` WRITE;
/*!40000 ALTER TABLE `sponsoredby` DISABLE KEYS */;
INSERT INTO `sponsoredby` VALUES (1,1),(1,2),(2,3),(4,4),(5,5);
/*!40000 ALTER TABLE `sponsoredby` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `student_id` int NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `age` int DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `semester` int DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'Rakesh','Kumar','Gowda','2001-03-12',24,'9876100001',6,'rakesh.gowda@email.com'),(2,'Priya','Ramesh','Shetty','2002-07-19',23,'9876100002',4,'priya.shetty@email.com'),(3,'Manjunath','S','Rao','2000-11-05',25,'9876100003',8,'manju.rao@email.com'),(4,'Aishwarya','P','Naik','2003-01-22',22,'9876100004',3,'aishu.naik@email.com'),(5,'Darshan','V','Urs','2001-09-30',24,'9876100005',5,'darshan.urs@email.com'),(10,'Alex',NULL,'Roy','2004-07-25',21,'9999999999',5,'alexroy@example.com');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venue`
--

DROP TABLE IF EXISTS `venue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venue` (
  `venue_id` int NOT NULL,
  `building` varchar(100) DEFAULT NULL,
  `room_no` varchar(20) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `resources` text,
  PRIMARY KEY (`venue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venue`
--

LOCK TABLES `venue` WRITE;
/*!40000 ALTER TABLE `venue` DISABLE KEYS */;
INSERT INTO `venue` VALUES (1,'Main Building','101',200,'Booked','Projector, Whiteboard'),(2,'Auditorium','A1',500,'Booked','Stage, Mic, Sound System'),(3,'Library Block','L2',80,'Booked','Chairs, Projector'),(4,'Innovation Lab','IL1',120,'Available','3D Printers, Computers'),(5,'Civil Block','C5',150,'Available','Drawing Boards, Projectors');
/*!40000 ALTER TABLE `venue` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-27 15:27:36
