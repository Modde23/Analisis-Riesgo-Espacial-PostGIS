import random
import datetime

# ==========================================
# 1. LISTAS Y DATOS DE ENTRADA
# ==========================================

# Nombres reales de 13 municipios de la zona Norte/Noreste de Guanajuato
NOMBRES_MUNICIPIOS = [
    "San Luis de la Paz", "Xichu", "San Felipe", "Victoria", "Atarjea", 
    "San Diego de la Union", "Doctor Mora", "Santa Catarina", 
    "Dolores Hidalgo C.I.N.", "Tierra Blanca", "San Jose Iturbide", 
    "Comonfort", "San Miguel de Allende"
]

# Datos Personales
NOMBRES_HOMBRES = ["JUAN", "PEDRO", "LUIS", "CARLOS", "JOSE", "MIGUEL", "JORGE", "DAVID", "ALEJANDRO", "FERNANDO", "ALEXIS", "JOSUE", "ANGEL", "ADAN", "EDUARDO", "RICARDO", "MIGUEL"]
NOMBRES_MUJERES = ["MARIA", "ANA", "SOFIA", "LUCIA", "FERNANDA", "ELENA", "CLARA", "ISABEL", "DANIELA", "VALERIA", "SAMANTHA", "MICHELLE", "KARINA", "EVELIN", "TERESA", "GABRIELA", "MELANIE", "SANDRA"]
APELLIDOS = ["GARCIA", "MARTINEZ", "LOPEZ", "GONZALEZ", "RODRIGUEZ", "PEREZ", "SANCHEZ", "RAMIREZ", "CRUZ", "FLORES"]
ENTIDADES = ["AS", "BC", "BS", "CC", "CL", "CM", "CS", "CH", "DF", "DG", "GT", "GR", "HG", "JC", "MC", "MN", "MS", "NT", "NL", "OC", "PL", "QT", "QR", "SP", "SL", "SR", "TC", "TS", "TL", "VZ", "YN", "ZS"]

GRADOS_ESTUDIO = ['Licenciatura', 'No concluido']
PADECIMIENTOS = ['Resfriado comun', 'Alergia estacional', 'Dolor de cabeza tensional', 'Indigestion', 'Conjuntivitis leve']

# Datos Vehículos
MARCAS = ['Nissan', 'Toyota', 'Volkswagen', 'Chevrolet', 'Ford']
COLORES = ['Negro', 'Blanco']
ANIOS_AUTO = [2020, 2021, 2022, 2023, 2024, 2025] 

# Datos Infraestructura y Daños
TIPOS_INFRA = ['Hospital General', 'Centro de Salud', 'Banco Nacional', 'Banco del Bajio', 'Hotel Real', 'Hotel Mision', 'Refugio Temporal']
DAÑOS_CICLON = ['Inundacion en vivienda', 'Perdida total de vehiculo', 'Techo dañado', 'Sin suministro electrico', 'Filtracion de agua']
DAÑOS_SISMO = ['Grietas en muros', 'Vidrios rotos', 'Daño estructural severo', 'Caida de barda', 'Crisis nerviosa']

TOTAL_PERSONAS = 18000
TOTAL_VEHICULOS = 10000

# ==========================================
# 2. FUNCIONES PARA CURP REALISTA
# ==========================================

def buscar_vocal_interna(palabra):
    vocales = "AEIOU"
    for letra in palabra[1:]: 
        if letra in vocales: return letra
    return "X"

def buscar_consonante_interna(palabra):
    vocales = "AEIOU"
    for letra in palabra[1:]: 
        if letra not in vocales: return letra
    return "X"

def generar_curp_real(nombre, paterno, materno, fecha_nacimiento, genero, entidad):
    l1 = paterno[0]
    l2 = buscar_vocal_interna(paterno)
    l3 = materno[0]
    l4 = nombre[0]
    yy = str(fecha_nacimiento.year)[2:4]
    mm = f"{fecha_nacimiento.month:02d}"
    dd = f"{fecha_nacimiento.day:02d}"
    c1 = buscar_consonante_interna(paterno)
    c2 = buscar_consonante_interna(materno)
    c3 = buscar_consonante_interna(nombre)
    homo = str(random.randint(0, 9))
    verif = str(random.randint(0, 9))
    return f"{l1}{l2}{l3}{l4}{yy}{mm}{dd}{genero}{entidad}{c1}{c2}{c3}{homo}{verif}".upper()

# ==========================================
# 3. LÓGICA DE DISTRIBUCIÓN (Regla 10%)
# ==========================================
ids_municipios = list(range(1, len(NOMBRES_MUNICIPIOS) + 1))
poblacion_por_municipio = {m: 20 for m in ids_municipios} 
personas_restantes = TOTAL_PERSONAS - (20 * len(ids_municipios))

for _ in range(personas_restantes):
    muni = random.choice(ids_municipios)
    while poblacion_por_municipio[muni] >= 1800:
        muni = random.choice(ids_municipios)
    poblacion_por_municipio[muni] += 1

asignacion_municipios = []
for m_id, cantidad in poblacion_por_municipio.items():
    asignacion_municipios.extend([m_id] * cantidad)
random.shuffle(asignacion_municipios)

# ==========================================
# 4. GENERACIÓN DEL SQL
# ==========================================
sql = []
sql.append("BEGIN TRANSACTION;")

# --- A. MUNICIPIOS ---
sql.append("\n-- MUNICIPIOS")
for i, nombre_real in enumerate(NOMBRES_MUNICIPIOS):
    es_pueblo_magico = 'TRUE' if i in [0, 8, 12] else 'FALSE'
    sql.append(f"INSERT INTO municipio (id_municipio, nombre, entidad_federativa, pueblo_magico, uso_suelo) VALUES ({i+1}, '{nombre_real}', 'Guanajuato', {es_pueblo_magico}, 'Mixto/Habitacional');")

# --- B. FENOMENOS ---
sql.append("\n-- FENOMENOS")
fenomenos_data = [
    (1, 'Hidrometeorologico', 'Ciclon h2', '2024-09-01'),
    (2, 'Geologico', 'Sismo Mag 7.6', '2022-09-19'),
    (3, 'Geologico', 'Sismo Mag 6.9', '2022-09-22'),
    (4, 'Quimico-Tecnologico', 'Incendio Forestal', '2024-03-15'),
    (5, 'Quimico-Tecnologico', 'Incendio Forestal', '2019-05-10')
]
for f in fenomenos_data:
    sql.append(f"INSERT INTO fenomeno (id_fenomeno, tipo, nombre_fenomeno, fecha) VALUES ({f[0]}, 1, '{f[2]}', '{f[3]}');")

# --- C. PERSONAS ---
sql.append("\n-- PERSONAS")
personas_ids = []

for i in range(TOTAL_PERSONAS):
    if random.choice([True, False]):
        genero = 'H'; nombre = random.choice(NOMBRES_HOMBRES)
    else:
        genero = 'M'; nombre = random.choice(NOMBRES_MUJERES)
    
    app = random.choice(APELLIDOS); apm = random.choice(APELLIDOS)
    anio_nac = random.randint(1960, 2005)
    fecha_nac = datetime.date(anio_nac, random.randint(1,12), random.randint(1,28))
    curp = generar_curp_real(nombre, app, apm, fecha_nac, genero, random.choice(ENTIDADES))
    personas_ids.append(curp)
    
    tel = f"55{random.randint(10000000, 99999999)}"
    mail = f"user{i}@mail.com"
    mun_id = asignacion_municipios[i]
    
    sql.append(f"INSERT INTO persona (curp, nombre, ap_paterno, ap_materno, edad, telefono, correo_electronico, grado_estudios, padecimientos_medicos, municipio_id) VALUES ('{curp}', '{nombre}', '{apm}', '{app}', {2025-anio_nac}, '{tel}', '{mail}', '{random.choice(GRADOS_ESTUDIO)}', '{random.choice(PADECIMIENTOS)}', {mun_id});")

# --- D. VEHICULOS ---
sql.append("\n-- VEHICULOS")
autos_por_persona = {p: 0 for p in personas_ids}
autos_generados = 0
while autos_generados < TOTAL_VEHICULOS:
    dueno = random.choice(personas_ids)
    if autos_por_persona[dueno] < 3:
        placa = f"GTO{autos_generados:04d}"
        sql.append(f"INSERT INTO vehiculo (placa, curp_propietario, marca, modelo, ano_fabricacion, color) VALUES ('{placa}', '{dueno}', '{random.choice(MARCAS)}', 'Aveo', {random.choice(ANIOS_AUTO)}, '{random.choice(COLORES)}');")
        autos_por_persona[dueno] += 1; autos_generados += 1

# --- E. AFECTACIONES MUNICIPIO (Genera IDs 1 al 13) ---
sql.append("\n-- AFECTACIONES MUNICIPIO")
id_afect_mun = 1
# IDs 1-5: Municipios afectados por Ciclon (Id Fenomeno 1)
for m in range(1, 6): 
    sql.append(f"INSERT INTO afectacion_municipio (id_afect_mun, municipio_id, fenomeno_id, grado_peligro) VALUES ({id_afect_mun}, {m}, 1, {random.randint(2,3)});")
    id_afect_mun += 1
# IDs 6-13: Municipios afectados por Sismo (Id Fenomeno 2)
for m in range(6, 14): 
    sql.append(f"INSERT INTO afectacion_municipio (id_afect_mun, municipio_id, fenomeno_id, grado_peligro) VALUES ({id_afect_mun}, {m}, 2, {random.randint(1,2)});")
    id_afect_mun += 1

# --- F. NUEVO: INFRAESTRUCTURA ---
sql.append("\n-- INFRAESTRUCTURA")
id_infra = 1
for m_id in range(1, 14): # Para cada municipio
    # Generamos entre 3 y 5 establecimientos por municipio
    num_establecimientos = random.randint(3, 5)
    nombre_mun = NOMBRES_MUNICIPIOS[m_id-1]
    
    for _ in range(num_establecimientos):
        tipo = random.choice(TIPOS_INFRA)
        # Nombre compuesto ej: "Hospital General de Xichú"
        nombre_est = f"{tipo} de {nombre_mun}"
        
        sql.append(f"INSERT INTO infraestructura (id_infraestructura, municipio_id, tipo_infraestructura, nombre_establecimiento) VALUES ({id_infra}, {m_id}, '{tipo}', '{nombre_est}');")
        id_infra += 1

# --- G. NUEVO: AFECTACION PERSONA ---
sql.append("\n-- AFECTACION PERSONA")
id_afect_pers = 1

# Recorremos a todas las personas y decidimos si fueron afectadas por el desastre de SU municipio
for i, curp in enumerate(personas_ids):
    mun_id = asignacion_municipios[i] # Municipio donde vive la persona
    
    # 20% de probabilidad de ser afectado
    if random.random() < 0.20:
        # Determinamos qué pasó en su municipio basado en la lógica de la sección E
        if mun_id <= 5: 
            # Zona de Ciclones
            fenomeno_id = 1
            afect_mun_id = mun_id # Porque generamos los IDs en orden en la seccion E
            desc = random.choice(DAÑOS_CICLON)
        else:
            # Zona de Sismos
            fenomeno_id = 2
            afect_mun_id = mun_id # Idem, coinciden ID municipio y ID afectacion en este script
            desc = random.choice(DAÑOS_SISMO)
            
        sql.append(f"INSERT INTO afectacion_persona (id_afectacion, afect_mun_id, curp_persona, fenomeno_id, descripcion_danos) VALUES ({id_afect_pers}, {afect_mun_id}, '{curp}', {fenomeno_id}, '{desc}');")
        id_afect_pers += 1

sql.append("COMMIT;")

# Guardar
with open("insert_script_final_completo.sql", "w") as f:
    f.write("\n".join(sql))

print("¡Archivo 'insert_script_final_completo.sql' generado con TODAS las tablas!")