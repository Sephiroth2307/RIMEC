import sqlite3
import xlrd

# Cargar el archivo Excel
archivo = 'BAZZAR.xlsx'
wb = xlrd.open_workbook(archivo)
hoja = wb.sheet_by_name("TABLA.db")

# Conectar a la base de datos SQLite3
db = sqlite3.connect('database.db')
cursor = db.cursor()
        
        # Crear tabla de productos
cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
        ID_ARTICULO INTEGER,
        NOMBRE TEXT,
        C_Art_Proveedor TEXT,
        ID_MATERIAL INTEGER,
        DESCRIPCION_MAT TEXT,
        ID_NUEVO TEXT,
        ID_COLOR INTEGER,
        DESCRIPCION_COR TEXT,
        TALLA TEXT,
        CANTIDAD INTEGER,
        ID_MARCA INTEGER,
        DESCRIPCION_MARCA TEXT,
        ID_GRUPO_2 INTEGER,
        DESCRIPCION_GRUPO2 TEXT,
        IMAGEN TEXT,
        PRECIO INTEGER
        )
    ''')
db.commit()

# Iterar a través de las filas del archivo Excel y agregar a la base de datos
for fila in range(1, hoja.nrows):  # Empieza desde la segunda fila porque la primera fila son encabezados
    valores = hoja.row_values(fila)
    cursor.execute('''
        INSERT INTO productos(
            ID_ARTICULO, NOMBRE, C_Art_Proveedor, ID_MATERIAL, DESCRIPCION_MAT,
            ID_NUEVO, ID_COLOR, DESCRIPCION_COR, TALLA, CANTIDAD, ID_MARCA,
            DESCRIPCION_MARCA, ID_GRUPO_2, DESCRIPCION_GRUPO2, IMAGEN, PRECIO
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', valores)

cursor.execute('SELECT DISTINCT DESCRIPCION_GRUPO2 FROM productos')

db.commit()
db.close()

print("Datos importados exitosamente.")