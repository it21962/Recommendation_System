-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: recommendations
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `coupons`
--

DROP TABLE IF EXISTS `coupons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupons` (
  `coupon_id` varchar(10) NOT NULL,
  `user_id` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `stake` float NOT NULL,
  `sport` varchar(50) NOT NULL,
  `league` varchar(50) NOT NULL,
  `company` varchar(50) NOT NULL,
  `selections` text,
  PRIMARY KEY (`coupon_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupons`
--

LOCK TABLES `coupons` WRITE;
/*!40000 ALTER TABLE `coupons` DISABLE KEYS */;
INSERT INTO `coupons` VALUES ('c1',1,'2025-05-21 11:47:12',25,'football','superleague','Novibet','a1:1.85,a2:2.10'),('c10',10,'2025-05-26 15:16:08',50,'football','superleague','Stoiximan','a2:2.40'),('c11',11,'2025-05-26 15:19:31',30,'basketball','euroleague','Novibet','a2:1.95'),('c123',33,'2025-05-20 12:56:28',20,'football','superleague','Novibet','a1:1.80,a2:2.10'),('c13',13,'2025-05-26 15:21:27',30,'basketball','euroleague','Stoiximan','a2:1.95'),('c2',2,'2025-05-21 11:48:19',40,'basketball','euroleague','Novibet','a2:1.60'),('c3',3,'2025-05-21 11:49:35',15,'tennis','atp','Novibet','a1:2.30'),('c4',4,'2025-05-21 11:50:26',30,'baseball','mlb','Novibet','a4:1.90'),('c5',4,'2025-05-26 12:46:15',30,'baseball','mlb','Stoiximan','a4:1.90'),('c6',4,'2025-05-26 12:54:00',50,'football','superleague','Stoiximan','a2:2.30'),('c7',7,'2025-05-26 13:33:39',30,'baseball','mlb','Stoiximan','a2:1.95'),('c8',8,'2025-05-26 13:33:39',50,'football','superleague','Stoiximan','a2:2.40'),('c9',9,'2025-05-26 15:16:46',30,'baseball','mlb','Stoiximan','a2:1.95');
/*!40000 ALTER TABLE `coupons` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-28 16:25:16
