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
-- Table structure for table `novibet_users`
--

DROP TABLE IF EXISTS `novibet_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `novibet_users` (
  `user_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `birth_year` int DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `registration_date` datetime DEFAULT NULL,
  `company` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `novibet_users`
--

LOCK TABLES `novibet_users` WRITE;
/*!40000 ALTER TABLE `novibet_users` DISABLE KEYS */;
INSERT INTO `novibet_users` VALUES (1,'Vasilis Nousis',1999,'GR','EUR','Male','2025-05-26 12:14:18','Novibet'),(5,'Vasilis Nousis',1999,'GR','EUR','Male','2025-05-26 12:03:12','Novibet'),(10,'Giannis Papadopoulos',1990,'GR','EUR','Male','2025-05-26 13:06:31','Novibet'),(12,'Bill Ts',1991,'GR','EUR','Male','2025-05-26 15:20:36','Novibet'),(18,'Bill hrt',1997,'GR','EUR','Male','2025-05-27 16:24:03','Novibet');
/*!40000 ALTER TABLE `novibet_users` ENABLE KEYS */;
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
