CREATE DATABASE  IF NOT EXISTS `condominio` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `condominio`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: condominio
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `apartamento`
--

DROP TABLE IF EXISTS `apartamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartamento` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `apartamento` int DEFAULT NULL,
  `responsavel` int DEFAULT NULL,
  PRIMARY KEY (`codigo`),
  UNIQUE KEY `apartamento` (`apartamento`),
  KEY `responsavel` (`responsavel`),
  CONSTRAINT `apartamento_ibfk_1` FOREIGN KEY (`responsavel`) REFERENCES `pessoas` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartamento`
--

LOCK TABLES `apartamento` WRITE;
/*!40000 ALTER TABLE `apartamento` DISABLE KEYS */;
INSERT INTO `apartamento` VALUES (1,1,1),(2,2,3),(3,3,1),(4,4,28),(5,5,NULL),(6,6,NULL),(7,7,NULL),(8,8,NULL),(9,9,NULL),(10,10,NULL);
/*!40000 ALTER TABLE `apartamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `codigo_veiculo` int DEFAULT NULL,
  `data_passagem` date DEFAULT NULL,
  `horario_passagem` time DEFAULT NULL,
  `passagem` enum('entrada','saida') DEFAULT NULL,
  PRIMARY KEY (`codigo`),
  KEY `logs_ibfk_1_idx` (`codigo_veiculo`),
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`codigo_veiculo`) REFERENCES `placas_cadastradas` (`codigo`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,1,'2023-02-14','16:39:27','saida'),(2,1,'2023-02-14','19:07:27','saida'),(3,2,'2023-02-14','19:16:42','entrada'),(4,2,'2023-02-14','19:24:34','entrada'),(5,2,'2023-02-14','19:26:10','entrada'),(6,2,'2023-02-14','19:27:51','saida'),(7,2,'2023-02-14','19:29:13','saida'),(8,1,'2023-02-14','22:06:46','entrada'),(9,1,'2023-02-14','22:07:23','saida'),(10,1,'2023-02-14','22:27:41','saida'),(11,1,'2023-02-25','10:14:38','entrada'),(12,1,'2023-02-25','10:14:53','saida'),(13,1,'2023-02-25','11:28:31','saida'),(14,1,'2023-02-25','11:29:32','entrada'),(15,1,'2023-02-25','11:32:29','saida'),(16,1,'2023-02-25','11:34:23','saida'),(19,2,'2023-02-25','18:33:36','entrada'),(20,2,'2023-02-25','19:00:32','entrada'),(25,1,'2023-02-12','10:23:21','entrada'),(26,2,'2023-02-27','15:51:08','entrada'),(27,2,'2023-02-27','15:52:31','saida'),(28,2,'2023-02-27','15:52:48','entrada'),(29,2,'2023-02-27','15:53:31','saida'),(30,2,'2023-02-27','15:55:45','saida'),(31,2,'2023-02-27','15:56:09','saida'),(32,2,'2023-02-27','15:56:52','entrada'),(33,2,'2023-02-27','15:57:55','saida'),(34,2,'2023-02-27','15:58:18','entrada'),(35,2,'2023-02-27','15:58:36','entrada'),(36,2,'2023-02-27','16:03:03','saida'),(37,2,'2023-02-27','16:03:39','saida'),(38,2,'2023-02-27','16:04:02','entrada'),(39,2,'2023-02-27','16:04:38','entrada'),(40,2,'2023-02-27','16:04:53','saida'),(41,2,'2023-03-07','09:55:28','entrada'),(42,2,'2023-03-07','09:55:34','entrada'),(43,2,'2023-03-07','09:55:38','entrada'),(44,2,'2023-03-07','10:06:09','saida'),(45,2,'2023-03-07','10:06:26','entrada'),(46,2,'2023-03-07','10:06:29','saida'),(47,2,'2023-03-07','10:06:33','saida'),(48,2,'2023-03-07','10:06:37','saida'),(49,2,'2023-03-07','10:07:18','entrada'),(50,2,'2023-03-07','10:07:22','entrada'),(51,2,'2023-03-07','10:07:58','entrada'),(52,2,'2023-03-07','10:08:02','entrada'),(53,2,'2023-03-07','10:08:05','saida'),(54,2,'2023-03-07','10:08:12','entrada'),(55,2,'2023-03-07','10:08:15','saida'),(56,2,'2023-03-07','10:09:56','entrada'),(57,2,'2023-03-07','10:10:00','entrada'),(58,2,'2023-03-07','10:10:03','saida'),(59,2,'2023-03-07','10:21:31','saida'),(60,2,'2023-03-07','10:21:35','saida'),(61,2,'2023-03-07','10:22:33','saida'),(62,2,'2023-03-07','10:22:37','saida'),(63,2,'2023-03-07','10:23:13','saida'),(64,2,'2023-03-07','10:23:14','entrada'),(65,2,'2023-03-07','10:23:16','entrada'),(66,2,'2023-03-07','10:23:16','entrada'),(67,2,'2023-03-07','10:23:33','saida'),(68,2,'2023-03-07','10:23:34','entrada'),(69,2,'2023-03-07','10:23:34','entrada'),(70,2,'2023-03-07','10:23:34','entrada'),(71,2,'2023-03-07','10:23:34','entrada'),(72,2,'2023-03-07','10:23:35','saida'),(73,2,'2023-03-07','10:24:24','entrada'),(74,2,'2023-03-07','10:24:27','saida'),(75,2,'2023-03-07','10:24:57','saida'),(76,2,'2023-03-07','10:25:12','entrada'),(77,2,'2023-03-07','10:25:25','saida'),(78,2,'2023-03-07','10:26:16','entrada'),(79,2,'2023-03-07','10:26:20','entrada'),(80,2,'2023-03-07','10:30:13','saida'),(93,2,'2023-03-07','11:24:59','saida'),(95,2,'2023-03-07','11:28:07','saida'),(99,2,'2023-03-07','13:22:59','saida'),(103,22,'2023-03-07','13:41:57','saida');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pessoas`
--

DROP TABLE IF EXISTS `pessoas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pessoas` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) DEFAULT NULL,
  `apartamento` smallint DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `tipo_pessoa` enum('responsavel','morador') DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pessoas`
--

LOCK TABLES `pessoas` WRITE;
/*!40000 ALTER TABLE `pessoas` DISABLE KEYS */;
INSERT INTO `pessoas` VALUES (1,'Nícholas',9,'1999-09-06','responsavel'),(2,'Vinícius',1,'1996-01-19','morador'),(3,'Henry',2,'2001-07-22','responsavel'),(28,'Ícaro',4,'2096-08-06','responsavel');
/*!40000 ALTER TABLE `pessoas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `placas_cadastradas`
--

DROP TABLE IF EXISTS `placas_cadastradas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `placas_cadastradas` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `placa` varchar(255) DEFAULT NULL,
  `responsavel` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `placas_cadastradas`
--

LOCK TABLES `placas_cadastradas` WRITE;
/*!40000 ALTER TABLE `placas_cadastradas` DISABLE KEYS */;
INSERT INTO `placas_cadastradas` VALUES (1,'#FCSS1','1'),(2,'AB 7288','3'),(22,'MK 1109','28');
/*!40000 ALTER TABLE `placas_cadastradas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-07 13:44:50
