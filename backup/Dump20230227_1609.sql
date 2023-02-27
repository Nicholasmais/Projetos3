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
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,1,'2023-02-14','16:39:27','saida'),(2,1,'2023-02-14','19:07:27','saida'),(3,2,'2023-02-14','19:16:42','entrada'),(4,2,'2023-02-14','19:24:34','entrada'),(5,2,'2023-02-14','19:26:10','entrada'),(6,2,'2023-02-14','19:27:51','saida'),(7,2,'2023-02-14','19:29:13','saida'),(8,1,'2023-02-14','22:06:46','entrada'),(9,1,'2023-02-14','22:07:23','saida'),(10,1,'2023-02-14','22:27:41','saida'),(11,1,'2023-02-25','10:14:38','entrada'),(12,1,'2023-02-25','10:14:53','saida'),(13,1,'2023-02-25','11:28:31','saida'),(14,1,'2023-02-25','11:29:32','entrada'),(15,1,'2023-02-25','11:32:29','saida'),(16,1,'2023-02-25','11:34:23','saida'),(19,2,'2023-02-25','18:33:36','entrada'),(20,2,'2023-02-25','19:00:32','entrada'),(25,1,'2023-02-12','10:23:21','entrada'),(26,2,'2023-02-27','15:51:08','entrada'),(27,2,'2023-02-27','15:52:31','saida'),(28,2,'2023-02-27','15:52:48','entrada'),(29,2,'2023-02-27','15:53:31','saida'),(30,2,'2023-02-27','15:55:45','saida'),(31,2,'2023-02-27','15:56:09','saida'),(32,2,'2023-02-27','15:56:52','entrada'),(33,2,'2023-02-27','15:57:55','saida'),(34,2,'2023-02-27','15:58:18','entrada'),(35,2,'2023-02-27','15:58:36','entrada'),(36,2,'2023-02-27','16:03:03','saida'),(37,2,'2023-02-27','16:03:39','saida'),(38,2,'2023-02-27','16:04:02','entrada'),(39,2,'2023-02-27','16:04:38','entrada'),(40,2,'2023-02-27','16:04:53','saida');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `placas_cadastradas`
--

LOCK TABLES `placas_cadastradas` WRITE;
/*!40000 ALTER TABLE `placas_cadastradas` DISABLE KEYS */;
INSERT INTO `placas_cadastradas` VALUES (1,'#FCSS1','Nícholas'),(2,'AB 7288','Henry');
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

-- Dump completed on 2023-02-27 16:09:22
