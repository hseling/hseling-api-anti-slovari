-- MySQL dump 10.13  Distrib 5.7.21, for osx10.11 (x86_64)
--
-- Host: localhost    Database: antislovari
-- ------------------------------------------------------
-- Server version	5.7.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dim`
--

DROP TABLE IF EXISTS `dim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dim` (
  `word` varchar(300) DEFAULT NULL,
  `lemma` varchar(300) DEFAULT NULL,
  `morphs` varchar(300) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dim`
--

LOCK TABLES `dim` WRITE;
/*!40000 ALTER TABLE `dim` DISABLE KEYS */;
/*!40000 ALTER TABLE `dim` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loan_affix`
--

DROP TABLE IF EXISTS `loan_affix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loan_affix` (
  `word` varchar(300) DEFAULT NULL,
  `lemma` varchar(300) DEFAULT NULL,
  `morphs` varchar(300) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loan_affix`
--

LOCK TABLES `loan_affix` WRITE;
/*!40000 ALTER TABLE `loan_affix` DISABLE KEYS */;
/*!40000 ALTER TABLE `loan_affix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main`
--

DROP TABLE IF EXISTS `main`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main` (
  `word` varchar(300) DEFAULT NULL,
  `lemma` varchar(300) DEFAULT NULL,
  `morphs` varchar(300) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main`
--

LOCK TABLES `main` WRITE;
/*!40000 ALTER TABLE `main` DISABLE KEYS */;
/*!40000 ALTER TABLE `main` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nonsense`
--

DROP TABLE IF EXISTS `nonsense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonsense` (
  `word` varchar(300) DEFAULT NULL,
  `lemma` varchar(300) DEFAULT NULL,
  `morphs` varchar(300) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nonsense`
--

LOCK TABLES `nonsense` WRITE;
/*!40000 ALTER TABLE `nonsense` DISABLE KEYS */;
/*!40000 ALTER TABLE `nonsense` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stop_seq`
--

DROP TABLE IF EXISTS `stop_seq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stop_seq` (
  `word` varchar(300) DEFAULT NULL,
  `lemma` varchar(300) DEFAULT NULL,
  `morphs` varchar(300) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stop_seq`
--

LOCK TABLES `stop_seq` WRITE;
/*!40000 ALTER TABLE `stop_seq` DISABLE KEYS */;
/*!40000 ALTER TABLE `stop_seq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vowel_seq`
--

DROP TABLE IF EXISTS `vowel_seq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vowel_seq` (
  `word` varchar(300) DEFAULT NULL,
  `lemma` varchar(300) DEFAULT NULL,
  `morphs` varchar(300) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vowel_seq`
--

LOCK TABLES `vowel_seq` WRITE;
/*!40000 ALTER TABLE `vowel_seq` DISABLE KEYS */;
/*!40000 ALTER TABLE `vowel_seq` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-26 12:01:19
