-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.31 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para edumind
CREATE DATABASE IF NOT EXISTS `edumind` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `edumind`;

-- Volcando estructura para tabla edumind.alumnos
CREATE TABLE IF NOT EXISTS `alumnos` (
  `id_alumno` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) NOT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `matricula` varchar(30) NOT NULL,
  `grupo` varchar(20) NOT NULL,
  `semestre` int NOT NULL,
  `especialidad` varchar(100) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` text,
  `estatus` enum('Activo','Reprobado','Baja') DEFAULT 'Activo',
  PRIMARY KEY (`id_alumno`),
  UNIQUE KEY `matricula` (`matricula`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla edumind.alumnos: 0 rows
/*!40000 ALTER TABLE `alumnos` DISABLE KEYS */;
/*!40000 ALTER TABLE `alumnos` ENABLE KEYS */;

-- Volcando estructura para tabla edumind.asistencias
CREATE TABLE IF NOT EXISTS `asistencias` (
  `id_asistencia` int NOT NULL AUTO_INCREMENT,
  `id_alumno` int NOT NULL,
  `fecha` date NOT NULL,
  `estado` enum('Asistió','Falta','Retardo') NOT NULL,
  PRIMARY KEY (`id_asistencia`),
  KEY `fk_asistencia_alumno` (`id_alumno`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla edumind.asistencias: 0 rows
/*!40000 ALTER TABLE `asistencias` DISABLE KEYS */;
/*!40000 ALTER TABLE `asistencias` ENABLE KEYS */;

-- Volcando estructura para tabla edumind.calificaciones
CREATE TABLE IF NOT EXISTS `calificaciones` (
  `id_calificacion` int NOT NULL AUTO_INCREMENT,
  `id_alumno` int NOT NULL,
  `id_materia` int NOT NULL,
  `parcial` int NOT NULL,
  `calificacion` decimal(4,2) NOT NULL,
  `fecha_registro` date DEFAULT NULL,
  PRIMARY KEY (`id_calificacion`),
  KEY `fk_calificacion_alumno` (`id_alumno`),
  KEY `fk_calificacion_materia` (`id_materia`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla edumind.calificaciones: 0 rows
/*!40000 ALTER TABLE `calificaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `calificaciones` ENABLE KEYS */;

-- Volcando estructura para tabla edumind.docentes
CREATE TABLE IF NOT EXISTS `docentes` (
  `id_docente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) NOT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `correo` varchar(150) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_docente`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla edumind.docentes: 0 rows
/*!40000 ALTER TABLE `docentes` DISABLE KEYS */;
INSERT INTO `docentes` (`id_docente`, `nombre`, `apellido_paterno`, `apellido_materno`, `correo`, `usuario`, `contraseña`, `fecha_registro`) VALUES
	(1, 'Admin', 'Principal', 'Sistema', 'admin@cetis61.edu.mx', 'admin', '12345', '2026-05-13 09:36:30');
/*!40000 ALTER TABLE `docentes` ENABLE KEYS */;

-- Volcando estructura para tabla edumind.materias
CREATE TABLE IF NOT EXISTS `materias` (
  `id_materia` int NOT NULL AUTO_INCREMENT,
  `nombre_materia` varchar(100) NOT NULL,
  `semestre` int NOT NULL,
  `especialidad` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_materia`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla edumind.materias: 0 rows
/*!40000 ALTER TABLE `materias` DISABLE KEYS */;
/*!40000 ALTER TABLE `materias` ENABLE KEYS */;

-- Volcando estructura para tabla edumind.observaciones
CREATE TABLE IF NOT EXISTS `observaciones` (
  `id_observacion` int NOT NULL AUTO_INCREMENT,
  `id_alumno` int NOT NULL,
  `id_docente` int NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_registro` date DEFAULT NULL,
  `prioridad` enum('Baja','Media','Alta') DEFAULT 'Media',
  PRIMARY KEY (`id_observacion`),
  KEY `fk_observacion_alumno` (`id_alumno`),
  KEY `fk_observacion_docente` (`id_docente`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla edumind.observaciones: 0 rows
/*!40000 ALTER TABLE `observaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `observaciones` ENABLE KEYS */;

-- Volcando estructura para tabla edumind.reportes
CREATE TABLE IF NOT EXISTS `reportes` (
  `id_reporte` int NOT NULL AUTO_INCREMENT,
  `id_docente` int NOT NULL,
  `tipo_reporte` varchar(100) NOT NULL,
  `fecha_generado` datetime DEFAULT CURRENT_TIMESTAMP,
  `descripcion` text,
  PRIMARY KEY (`id_reporte`),
  KEY `fk_reporte_docente` (`id_docente`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla edumind.reportes: 0 rows
/*!40000 ALTER TABLE `reportes` DISABLE KEYS */;
/*!40000 ALTER TABLE `reportes` ENABLE KEYS */;

-- Volcando estructura para tabla edumind.riesgo_academico
CREATE TABLE IF NOT EXISTS `riesgo_academico` (
  `id_riesgo` int NOT NULL AUTO_INCREMENT,
  `id_alumno` int NOT NULL,
  `nivel_riesgo` enum('Bajo','Medio','Alto') NOT NULL,
  `motivo` text NOT NULL,
  `fecha_registro` date DEFAULT NULL,
  `seguimiento` text,
  PRIMARY KEY (`id_riesgo`),
  KEY `fk_riesgo_alumno` (`id_alumno`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla edumind.riesgo_academico: 0 rows
/*!40000 ALTER TABLE `riesgo_academico` DISABLE KEYS */;
/*!40000 ALTER TABLE `riesgo_academico` ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
