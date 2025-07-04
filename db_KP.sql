-- MySQL dump untuk database KP yang telah diperbaiki
-- Database: db_kp
-- ------------------------------------------------------

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

-- Hapus tabel properties lama jika ada
DROP TABLE IF EXISTS `properties`;

-- Struktur tabel untuk tabel `users`
DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','pengguna') NOT NULL DEFAULT 'pengguna',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

-- Data untuk tabel `users`
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Administrator','admin@telkom.co.id','pbkdf2:sha256:600000$KvdIFquH8tgupXs3$cdbe17684980c07ca70b9edff6db949969e53618b01b6cffcae03259df080706','admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

-- Struktur tabel untuk `properti_tanah`
DROP TABLE IF EXISTS `properti_tanah`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `properti_tanah` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `location` varchar(100) NOT NULL,
  `price` bigint NOT NULL,
  `land_area` decimal(10,2) NOT NULL,
  `certificate` varchar(50) DEFAULT NULL,
  `facing` varchar(50) DEFAULT NULL,
  `water_source` varchar(50) DEFAULT NULL,
  `internet` enum('Ya','Tidak') DEFAULT 'Tidak',
  `hook` enum('Ya','Tidak') DEFAULT 'Tidak',
  `power` int DEFAULT 0,
  `road_width` varchar(50) DEFAULT NULL,
  `description` text,
  `status` enum('aktif','tidak_aktif') DEFAULT 'aktif',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `properti_tanah_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Struktur tabel untuk `properti_tanah_bangunan`
DROP TABLE IF EXISTS `properti_tanah_bangunan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `properti_tanah_bangunan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `location` varchar(100) NOT NULL,
  `price` bigint NOT NULL,
  `land_area` decimal(10,2) NOT NULL,
  `building_area` decimal(10,2) NOT NULL,
  `bedrooms` int DEFAULT 0,
  `bathrooms` int DEFAULT 0,
  `floors` int DEFAULT 1,
  `certificate` varchar(50) DEFAULT NULL,
  `condition_property` varchar(50) DEFAULT NULL,
  `facing` varchar(50) DEFAULT NULL,
  `water_source` varchar(50) DEFAULT NULL,
  `internet` enum('Ya','Tidak') DEFAULT 'Tidak',
  `hook` enum('Ya','Tidak') DEFAULT 'Tidak',
  `power` int DEFAULT 0,
  `dining_room` varchar(50) DEFAULT NULL,
  `living_room` varchar(50) DEFAULT NULL,
  `road_width` varchar(50) DEFAULT NULL,
  `furnished` varchar(50) DEFAULT NULL,
  `description` text,
  `status` enum('aktif','tidak_aktif') DEFAULT 'aktif',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `properti_tanah_bangunan_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data contoh untuk properti_tanah
LOCK TABLES `properti_tanah` WRITE;
/*!40000 ALTER TABLE `properti_tanah` DISABLE KEYS */;
INSERT INTO `properti_tanah` VALUES 
(1,'Tanah Kavling Siap Bangun Surabaya Timur','Surabaya Timur',500000000,120.00,'SHM','Timur','PDAM','Ya','Ya',1300,'6 meter','Tanah kavling strategis di kawasan berkembang Surabaya Timur, cocok untuk investasi atau hunian.','aktif','2025-01-01 10:00:00','2025-01-01 10:00:00',1),
(2,'Tanah Strategis Dekat Universitas','Surabaya Selatan',750000000,200.00,'SHM','Selatan','PDAM','Ya','Tidak',2200,'8 meter','Tanah strategis dekat kampus dan fasilitas umum, potensi investasi tinggi.','aktif','2025-01-01 10:15:00','2025-01-01 10:15:00',1),
(3,'Tanah Komersial Jalan Utama','Surabaya Pusat',1200000000,150.00,'SHM','Utara','PDAM','Ya','Ya',2200,'10 meter','Tanah komersial di jalan utama, cocok untuk usaha atau investasi jangka panjang.','aktif','2025-01-01 10:30:00','2025-01-01 10:30:00',1);
/*!40000 ALTER TABLE `properti_tanah` ENABLE KEYS */;
UNLOCK TABLES;

-- Data contoh untuk properti_tanah_bangunan
LOCK TABLES `properti_tanah_bangunan` WRITE;
/*!40000 ALTER TABLE `properti_tanah_bangunan` DISABLE KEYS */;
INSERT INTO `properti_tanah_bangunan` VALUES 
(1,'Rumah Modern 2 Lantai Surabaya Barat','Surabaya Barat',1500000000,150.00,120.00,3,2,2,'SHM','bagus','Barat','PDAM','Ya','Ya',2200,'Ada','Ada','Semi Furnished','Rumah modern dengan desain kontemporer, lokasi strategis dekat pusat kota.','aktif','2025-01-01 11:00:00','2025-01-01 11:00:00',1),
(2,'Rumah Minimalis Siap Huni','Surabaya Utara',980000000,100.00,80.00,2,1,1,'SHM','baru','Timur','PDAM','Ya','Tidak',1300,'Ada','Ada','Furnished','Rumah minimalis siap huni dengan fasilitas lengkap dan akses mudah ke berbagai tempat.','aktif','2025-01-01 11:15:00','2025-01-01 11:15:00',1),
(3,'Rumah Mewah 3 Lantai','Surabaya Selatan',2500000000,250.00,200.00,4,3,3,'SHM','baru','Selatan','PDAM','Ya','Ya',3500,'Ada','Ada','Furnished','Rumah mewah dengan fasilitas premium, kolam renang, dan taman yang luas.','aktif','2025-01-01 11:30:00','2025-01-01 11:30:00',1),
(4,'Rumah Keluarga Strategis','Surabaya Timur',1200000000,120.00,90.00,3,2,2,'SHM','bagus','Utara','PDAM','Ya','Ya',2200,'Ada','Ada','Semi Furnished','Rumah keluarga dengan lokasi strategis, dekat sekolah dan pusat perbelanjaan.','aktif','2025-01-01 11:45:00','2025-01-01 11:45:00',1);
/*!40000 ALTER TABLE `properti_tanah_bangunan` ENABLE KEYS */;
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Database updated on 2025-07-04
