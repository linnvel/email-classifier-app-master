-- MySQL dump 10.13  Distrib 8.0.19, for osx10.15 (x86_64)
--
-- Host: localhost    Database: emailclassifier
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `emails`
--

drop database if exists `emailclassifier`;
create database `emailclassifier` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use emailclassifier;

DROP TABLE IF EXISTS `emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emails` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(30) DEFAULT NULL,
  `predicted_label` varchar(50) DEFAULT NULL,
  `upload_by` int DEFAULT NULL,
  `upload_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails`
--

LOCK TABLES `emails` WRITE;
/*!40000 ALTER TABLE `emails` DISABLE KEYS */;
INSERT INTO `emails` VALUES (8,'61256','sci.space',4,'2020-04-03 06:00:47'),(9,'60761','comp.sys.mac.hardware',4,'2020-04-03 15:26:11'),(16,'104635','rec.sport.baseball',4,'2020-04-04 02:46:11'),(18,'104628','rec.sport.baseball',4,'2020-04-04 03:14:48'),(19,'104640','rec.sport.baseball',4,'2020-04-04 03:17:48'),(21,'67395','comp.windows.x',4,'2020-04-04 03:18:43');
/*!40000 ALTER TABLE `emails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `mid_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `mail_address` varchar(100) DEFAULT NULL,
  `occupation` varchar(30) DEFAULT NULL,
  `pass_word` varchar(100) DEFAULT NULL,
  `register_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'james','james@yahoo.com','James','','Bond','2341238234','123 3rd Ave, NYC, NY100000','Spy','$5$rounds=535000$ymaN3LGWEovjKtfI$35P4N2XQpSCPtgMEEvjXdaT0rlQfXWMrUaGIx28Q5T0','2020-04-02 21:42:09'),(3,'helen','helen@yahoo.com','Helen','X','Bond','2341238234','123 3rd Ave, NYC, NY100000','Spy','$5$rounds=535000$ZXs9VN3hZdAyg77w$O2K38bnghS/YeVbyNinilLWl1be/gXdhJbBtQy6byQ4','2020-04-02 21:48:29'),(4,'sherry','xychen012@gmail.com','Sherry','Xiaoyi','Chen','97212834722','123 Harrison St, Princeton, NJ08084','Student','$5$rounds=535000$9g5V1zPlRsMIMx3v$oNj0eyWxhIH2bDZtARYBX4ek.uIOoABOO4BV/4AL/44','2020-04-03 00:59:12'),(5,'sussie','sussie@gmail.com','Sussie','Su','Zhou','','','','$5$rounds=535000$xERdVl6ybbOT1g2G$WNMVZD3V2gtJiKX9yWFJhKb5Qij2sE9RDznJVWNejW/','2020-04-03 14:48:32');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-04 10:59:55
