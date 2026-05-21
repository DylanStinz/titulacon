CREATE DATABASE IF NOT EXISTS `edumind`
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

USE `edumind`;

CREATE TABLE `alumnos` (
    `id_alumno` INT NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(100) NOT NULL,
    `apellido_paterno` VARCHAR(100) NOT NULL,
    `apellido_materno` VARCHAR(100),
    `matricula` VARCHAR(30) NOT NULL UNIQUE,
    `grupo` VARCHAR(20) NOT NULL,
    `semestre` INT NOT NULL,
    `especialidad` VARCHAR(100),
    `fecha_nacimiento` DATE,
    `telefono` VARCHAR(20),
    `direccion` TEXT,
    `estatus` ENUM('Activo','Reprobado','Baja') DEFAULT 'Activo',
    PRIMARY KEY (`id_alumno`)
) ENGINE=InnoDB;

CREATE TABLE `docentes` (
    `id_docente` INT NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(100) NOT NULL,
    `apellido_paterno` VARCHAR(100) NOT NULL,
    `apellido_materno` VARCHAR(100),
    `correo` VARCHAR(150) NOT NULL UNIQUE,
    `usuario` VARCHAR(50) NOT NULL UNIQUE,
    `contraseña` VARCHAR(255) NOT NULL,
    `fecha_registro` DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id_docente`)
) ENGINE=InnoDB;

INSERT INTO `docentes`
(`nombre`, `apellido_paterno`, `apellido_materno`,
 `correo`, `usuario`, `contraseña`)
VALUES
('Admin', 'Principal', 'Sistema',
 'admin@cetis61.edu.mx', 'admin', '12345');

CREATE TABLE `materias` (
    `id_materia` INT NOT NULL AUTO_INCREMENT,
    `nombre_materia` VARCHAR(100) NOT NULL,
    `semestre` INT NOT NULL,
    `especialidad` VARCHAR(100),
    PRIMARY KEY (`id_materia`)
) ENGINE=InnoDB;

CREATE TABLE `asistencias` (
    `id_asistencia` INT NOT NULL AUTO_INCREMENT,
    `id_alumno` INT NOT NULL,
    `fecha` DATE NOT NULL,
    `estado` ENUM('Asistió','Falta','Retardo') NOT NULL,
    PRIMARY KEY (`id_asistencia`),
    FOREIGN KEY (`id_alumno`)
        REFERENCES `alumnos`(`id_alumno`)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE `calificaciones` (
    `id_calificacion` INT NOT NULL AUTO_INCREMENT,
    `id_alumno` INT NOT NULL,
    `id_materia` INT NOT NULL,
    `parcial` INT NOT NULL,
    `calificacion` DECIMAL(4,2) NOT NULL,
    `fecha_registro` DATE,
    PRIMARY KEY (`id_calificacion`),
    FOREIGN KEY (`id_alumno`)
        REFERENCES `alumnos`(`id_alumno`)
        ON DELETE CASCADE,
    FOREIGN KEY (`id_materia`)
        REFERENCES `materias`(`id_materia`)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE `observaciones` (
    `id_observacion` INT NOT NULL AUTO_INCREMENT,
    `id_alumno` INT NOT NULL,
    `id_docente` INT NOT NULL,
    `descripcion` TEXT NOT NULL,
    `fecha_registro` DATE,
    `prioridad` ENUM('Baja','Media','Alta') DEFAULT 'Media',
    PRIMARY KEY (`id_observacion`),
    FOREIGN KEY (`id_alumno`)
        REFERENCES `alumnos`(`id_alumno`),
    FOREIGN KEY (`id_docente`)
        REFERENCES `docentes`(`id_docente`)
) ENGINE=InnoDB;

CREATE TABLE `riesgo_academico` (
    `id_riesgo` INT NOT NULL AUTO_INCREMENT,
    `id_alumno` INT NOT NULL,
    `nivel_riesgo` ENUM('Bajo','Medio','Alto') NOT NULL,
    `motivo` TEXT NOT NULL,
    `fecha_registro` DATE,
    `seguimiento` TEXT,
    PRIMARY KEY (`id_riesgo`),
    FOREIGN KEY (`id_alumno`)
        REFERENCES `alumnos`(`id_alumno`)
) ENGINE=InnoDB;

CREATE TABLE `reportes` (
    `id_reporte` INT NOT NULL AUTO_INCREMENT,
    `id_docente` INT NOT NULL,
    `tipo_reporte` VARCHAR(100) NOT NULL,
    `fecha_generado` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `descripcion` TEXT,
    PRIMARY KEY (`id_reporte`),
    FOREIGN KEY (`id_docente`)
        REFERENCES `docentes`(`id_docente`)
) ENGINE=InnoDB;