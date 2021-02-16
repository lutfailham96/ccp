-- MySQL dump 10.17  Distrib 10.3.25-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: computer_monitor
-- ------------------------------------------------------
-- Server version	10.3.25-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('545ad7a72420');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `computer`
--

DROP TABLE IF EXISTS `computer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `computer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `computer_id` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `computer_name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `computer_location` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `computer_power_status` tinyint(1) NOT NULL,
  `computer_cmd` tinyint(1) NOT NULL,
  `computer_cmd_date` int(11) NOT NULL,
  `computer_ping_timestamp` int(11) NOT NULL,
  `computer_instance` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `computer_id` (`computer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `computer`
--

LOCK TABLES `computer` WRITE;
/*!40000 ALTER TABLE `computer` DISABLE KEYS */;
INSERT INTO `computer` VALUES (132,'MIGAS_PTSA_A1','A1','PTSA',1,1,1613374652,1613457314,'MIGAS','2020-08-11 10:15:31','2021-02-16 06:28:19'),(134,'MIGAS_PTSA_D1','D1','PTSA',1,1,1613374652,1613457302,'MIGAS','2020-08-11 10:54:35','2021-02-16 06:15:37'),(136,'MIGAS_PTSA_B1','B1','PTSA',1,1,1613374652,1613457301,'MIGAS','2020-08-11 13:43:23','2021-02-16 06:13:35'),(137,'MIGAS_PTSA_A2','A2','PTSA',0,0,1613374652,1613374624,'MIGAS','2020-08-11 14:19:03','2021-02-15 14:37:32'),(138,'MIGAS_PTSA_A4','A4','PTSA',0,0,1613374652,1613374636,'MIGAS','2020-08-11 14:46:35','2021-02-15 14:37:32'),(139,'MIGAS_PTSA_A5','A5','PTSA',0,0,1613374652,1612860953,'MIGAS','2020-08-11 14:51:21','2021-02-15 14:37:32'),(140,'MIGAS_PTSA_A3','A3','PTSA',0,0,1613374652,1613374628,'MIGAS','2020-08-11 14:54:49','2021-02-15 14:37:32'),(141,'MIGAS_PTSA_F1','F1','PTSA',0,0,1613374652,1612860958,'MIGAS','2020-08-11 15:29:22','2021-02-15 14:37:32'),(146,'MIGAS_PTSA_C1','C1','PTSA',1,1,1613374652,1613457313,'MIGAS','2020-08-13 10:09:19','2021-02-16 06:11:18'),(150,'MIGAS_DEV_D1','D1','DEV',0,1,1597809840,1597809940,'MIGAS','2020-08-13 13:21:22','2020-08-19 11:07:01'),(151,'MIGAS_DEV_D2','D2','DEV',2,0,1597809840,1597302058,'MIGAS','2020-08-13 13:21:36','2020-08-19 11:03:59'),(152,'MIGAS_DEV_D3','D3','DEV',0,0,1597809840,1597367766,'MIGAS','2020-08-13 13:21:36','2020-08-19 11:03:59'),(153,'__','','',0,1,1597809776,1600915557,'','2020-09-20 16:35:20','2020-09-24 09:47:01'),(154,'MIGAS_PTSA_F2','F2','PTSA',0,0,1613374652,1613026005,'MIGAS','2020-10-21 09:05:45','2021-02-15 14:37:32');
/*!40000 ALTER TABLE `computer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `username` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(95) COLLATE utf8mb4_unicode_ci NOT NULL,
  `instance` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Lutfa Ibtihaji Ilham','admin','pbkdf2:sha256:150000$DhHIczCV$b8ca57921588fbc8f3affe28d0cd7bba6d44fde2699582582fd7a2bfa180a9b0','MIGAS','PTSA|DEV','2020-08-10 14:28:48','2020-08-11 15:49:40');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-16 13:35:19
