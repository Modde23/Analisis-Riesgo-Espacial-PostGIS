# Análisis de Factibilidad de Préstamos en Zonas de Riesgo 🌍🏦
**Proyecto Final - Introducción a Bases de Datos Espaciales | Facultad de Ingeniería, UNAM**

Este proyecto implementa un sistema de análisis geoespacial para determinar la viabilidad de otorgar préstamos bancarios en función de indicadores de vulnerabilidad y riesgo ambiental. Utiliza una arquitectura basada en **PostGIS**, **QGIS** y automatización con **Python**.

## 🛠️ Tecnologías Utilizadas
* **Base de Datos:** PostgreSQL con extensión **PostGIS**.
* **GIS:** QGIS (Visualización de capas, buffers y análisis espacial).
* **Lenguajes:** * **SQL:** Diseño de tablas, triggers y consultas espaciales complejas.
    * **Python:** Scripting para la generación masiva de datos (10,000+ registros).

## 🚀 Características Principales
1.  **Modelo Entidad-Relación:** Diseño robusto que gestiona clientes, sucursales bancarias, historial de préstamos y datos académicos.
2.  **Generación de Datos Masivos:** Desarrollo de un script en Python para poblar la base de datos con más de 10,000 registros mediante bloques controlados para asegurar la integridad de los datos.
3.  **Análisis Geoespacial:**
    * Uso de funciones `ST_Buffer` para crear áreas de influencia de 1 KM.
    * Análisis de intersección con polígonos de incidencia (capa `indi_pv`).
4.  **Lógica de Negocio Automática:** Implementación de lógica SQL para clasificar solicitudes como **"Factible"** o **"No Factible"** basándose en la suma de indicadores (granizo, temperatura, red eléctrica).
5.  **Cálculo de Rutas:** Determinación de trayectorias óptimas entre coordenadas geográficas específicas.

## 📁 Estructura del Repositorio
* `/sql`: Contiene los scripts de creación de tablas (`DDL`) y las consultas de análisis (`DML`).
* `/scripts`: Script de Python utilizado para la inserción masiva de datos.
* `/docs`: Documentación detallada del proyecto (PDF).
* `/data`: Archivos GeoJSON y capas utilizadas en el análisis.

## 📊 Ejemplo de Consulta Espacial
```sql
-- Ejemplo de cómo determinamos la factibilidad técnica
SELECT id_solicitud, 
       ST_Intersection(geom_solicitud, geom_riesgo) as zona_afectada
FROM solicitudes
WHERE (indicador_granizo + indicador_temp + indicador_red) > 5;