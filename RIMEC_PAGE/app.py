import os
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import sqlite3

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'u ja ja ja')
app.permanent_session_lifetime = timedelta(days=1)
app.config['SESSION_PERMANENT'] = True

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv
    finally:
        con.close()

def format_guaranies(value):
    return "₲{:,.0f}".format(value)

def obtener_tipos_unicos():
    query = "SELECT DISTINCT DESCRIPCION_GRUPO2, IMAGEN FROM productos"
    tipos_con_imagen = query_db(query)
    tipos_calzado_con_imagen = {tipo['DESCRIPCION_GRUPO2']: tipo['IMAGEN'] for tipo in tipos_con_imagen}
    return tipos_calzado_con_imagen

def obtener_marcas_unicas():
    query = "SELECT DISTINCT DESCRIPCION_MARCA FROM productos"
    marcas = query_db(query)
    return [marca['DESCRIPCION_MARCA'] for marca in marcas]

def obtener_colores_unicos():
    query = "SELECT DISTINCT DESCRIPCION_COR FROM productos"
    colores = query_db(query)
    colores_unicos_acortados = set()

    for color in colores:
        color_original = color['DESCRIPCION_COR']

        # Omitir colores que comienzan con paréntesis
        if color_original.startswith('('):
            continue

        # Buscar la posición del espacio o la barra diagonal
        pos_espacio = color_original.find(' ')
        pos_barra = color_original.find('/')

        # Determinar hasta dónde acortar el nombre del color
        if 0 <= pos_espacio < 5:
            longitud = pos_espacio
        elif 0 <= pos_barra < 5:
            longitud = pos_barra
        else:
            longitud = min(5, len(color_original))

        # Acortar el nombre del color
        color_acortado = color_original[:longitud]
        colores_unicos_acortados.add(color_acortado)

    return list(colores_unicos_acortados)

def obtener_productos_por_tipo(tipo_calzado):
    query = "SELECT * FROM productos WHERE DESCRIPCION_GRUPO2 = ?"
    productos = query_db(query, [tipo_calzado])
    return [dict(producto) for producto in productos]

def obtener_marcas_por_tipo(tipos_calzado):
    marcas_por_tipo = {}
    for tipo in tipos_calzado:
        query = "SELECT DISTINCT DESCRIPCION_MARCA FROM productos WHERE DESCRIPCION_GRUPO2 = ?"
        marcas = query_db(query, [tipo])
        marcas_por_tipo[tipo] = [marca['DESCRIPCION_MARCA'] for marca in marcas]
    return marcas_por_tipo

app.jinja_env.filters['currency'] = format_guaranies

def obtener_items_del_carrito():
    return session.get('carrito', [])

def actualizar_carrito_sesion(carrito):
    session['carrito'] = carrito
    session.modified = True

def obtener_producto_por_id(producto_id):
    producto = query_db("SELECT * FROM productos WHERE ID_ARTICULO=?", [producto_id], one=True)
    if producto:
        producto_dict = dict(producto)
        tallas_cantidades = query_db("SELECT TALLA, CANTIDAD FROM productos WHERE NOMBRE=?", [producto_dict['NOMBRE']])
        producto_dict['TALLAS'] = [item['TALLA'] for item in tallas_cantidades]
        producto_dict['CANTIDADES'] = [item['CANTIDAD'] for item in tallas_cantidades]
        return producto_dict
    return None

def obtener_productos_relacionados(producto):
    return query_db("""SELECT * FROM productos WHERE 
                    DESCRIPCION_GRUPO2=? AND 
                    DESCRIPCION_MARCA=? AND 
                    DESCRIPCION_MAT=? AND 
                    C_Art_Proveedor=? AND
                    ID_MATERIAL=? AND
                    ID_ARTICULO != ?""", 
                    [producto['DESCRIPCION_GRUPO2'], producto['DESCRIPCION_MARCA'], producto['DESCRIPCION_MAT'], producto['C_Art_Proveedor'], producto['ID_MATERIAL'], producto['ID_ARTICULO']])

def actualizar_carrito_sesion(carrito):
    session['carrito'] = carrito
    session.modified = True

########################################### HTTP ###########################################

@app.route('/buscar')
def buscar_producto():
    codigo_buscado = request.args.get('codigo')
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM productos WHERE C_Art_Proveedor LIKE ?"
    cursor.execute(query, ['%' + codigo_buscado + '%'])
    productos_encontrados = cursor.fetchall()
    conn.close()

    # Suponiendo que tienes una plantilla para mostrar los resultados
    return render_template('resultados_busqueda.html', productos=productos_encontrados)


tipos_calzado_con_imagen = {
    'CARTERAS': 'images/1184-1101-26631-430.jpg',
    'SANDALIA': 'images/1184-1101-26631-430.jpg',
    'ZAPATO': 'images/1184-1101-26631-430.jpg',
    'TAMANCO': 'images/1184-1101-26631-430.jpg',
    'RASTRERA': 'images/1184-1101-26631-430.jpg',
    'TENIS': 'images/1184-1101-26631-430.jpg',
    'ZAPATILLA': 'images/1184-1101-26631-430.jpg',
    'STILETTO': 'images/1184-1101-26631-430.jpg',
    'CHATITA': 'images/1184-1101-26631-430.jpg',
}

@app.route('/')
def inicio():
    return render_template('inicio.html', tipos_calzado=tipos_calzado_con_imagen)

@app.route('/productos/tipo/<tipo_calzado>')
def productos_por_tipo(tipo_calzado):
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM productos WHERE DESCRIPCION_GRUPO2 = ?"
    cursor.execute(query, [tipo_calzado])
    productos = cursor.fetchall()
    conn.close()

    colores = obtener_colores_unicos()
    marcas = obtener_marcas_unicas()

    # Filtrar productos con imágenes duplicadas
    imagenes_vistas = set()
    productos_filtrados = []
    for producto in productos:
        if producto['IMAGEN'] not in imagenes_vistas:
            imagenes_vistas.add(producto['IMAGEN'])
            productos_filtrados.append(producto)
    return render_template('productos_por_tipo.html', productos=productos_filtrados, tipo_calzado=tipo_calzado, colores=colores, marcas=marcas)

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/productos')
def productos():
    marcas_list = [
        {
            "nombre": "VIZZANO",
            "imagen": "static/images/banner_vz.jpg"
        },

        {
            "nombre": "MOLEKINHO",
            "imagen": "static/images/banner_mlo.jpg"
        },

        {
            "nombre": "MOLEKINHA",
            "imagen": "static/images/banner_mlk.jpg"
        },

        {
            "nombre": "MOLECA",
            "imagen": "static/images/banner_ml.jpg"
        },

        {
            "nombre": "MODARE",
            "imagen": "static/images/banner_md.jpg"
        }
    ]
    return render_template('marcas.html', marcas=marcas_list) 

@app.route('/productos/<marca>')
def productos_por_marca(marca):
    tipos_calzado = obtener_tipos_unicos()
    colores_disponibles = obtener_colores_unicos()
    marcas_por_tipo = obtener_marcas_por_tipo(tipos_calzado)
    tipos_unicos = obtener_tipos_unicos()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_ARTICULO, NOMBRE, IMAGEN, DESCRIPCION_GRUPO2, DESCRIPCION_COR FROM productos WHERE DESCRIPCION_MARCA=?", (marca, ))
    productos = cursor.fetchall()
    conn.close()

    imagenes_vistas = set()
    productos_filtrados = []
    for producto in productos:
        if producto['IMAGEN'] not in imagenes_vistas:
            imagenes_vistas.add(producto['IMAGEN'])
            productos_filtrados.append(producto)

    return render_template('listado_productos.html', productos=productos_filtrados, tipos=tipos_unicos, marca=marca, tipos_calzado=tipos_calzado, marcas_por_tipo=marcas_por_tipo, colores_disponibles=colores_disponibles)



@app.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)
    productos_relacionados_raw = obtener_productos_relacionados(producto)
    
    # Filtrar productos relacionados con imágenes duplicadas
    imagenes_vistas = set()
    productos_relacionados = []
    for relacionado in productos_relacionados_raw:
        if relacionado['IMAGEN'] not in imagenes_vistas and relacionado['ID_ARTICULO'] != producto_id:
            imagenes_vistas.add(relacionado['IMAGEN'])
            productos_relacionados.append(relacionado)

    return render_template('detalle_producto.html', producto=producto, productos_relacionados=productos_relacionados)

@app.route('/compra')
def compra():
    # Lógica para manejar el proceso de compra.

    return render_template('compra.html')

@app.route('/carrito')
def carrito():
    carrito_items = obtener_items_del_carrito()
    total = 0
    carrito_items_actualizados = []

    for item in carrito_items:
        producto = obtener_producto_por_id(item['ID_ARTICULO'])
        if producto:
            item['producto'] = producto
            item['subtotal'] = item['CANTIDAD'] * producto['PRECIO']
            total += item['subtotal']
            carrito_items_actualizados.append(item)

    actualizar_carrito_sesion(carrito_items_actualizados)

    return render_template('carrito.html', carrito=carrito_items_actualizados, total=total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    producto_id = data.get('producto_id')
    talla_solicitada = data.get('talla')
    cantidad_solicitada = data.get('cantidad', 1)

    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    if talla_solicitada not in producto['TALLAS']:
        return jsonify({'error': 'Talla no disponible'}), 404

    talla_index = producto['TALLAS'].index(talla_solicitada)
    if cantidad_solicitada > producto['CANTIDADES'][talla_index]:
        return jsonify({'error': 'Cantidad solicitada excede el stock disponible'}), 400

    carrito = obtener_items_del_carrito()
    producto_en_carrito = False

    for item in carrito:
        if item['ID_ARTICULO'] == producto_id and item.get('talla') == talla_solicitada:
            nueva_cantidad = item.get('CANTIDAD', 0) + cantidad_solicitada
            if nueva_cantidad <= producto['CANTIDADES'][talla_index]:
                item['CANTIDAD'] = nueva_cantidad
                producto_en_carrito = True
                break
            else:
                return jsonify({'error': 'No se puede añadir más del producto al carrito'}), 400

    if not producto_en_carrito:
        carrito.append({
            'ID_ARTICULO': producto_id,
            'talla': talla_solicitada,
            'CANTIDAD': cantidad_solicitada
        })

    actualizar_carrito_sesion(carrito)

    return jsonify({'mensaje': 'Producto añadido al carrito'}), 200

@app.route('/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    carrito_items = session.get('carrito', [])
    carrito_items = [item for item in carrito_items if item['ID_ARTICULO'] != producto_id]
    session['carrito'] = carrito_items
    session.modified = True
    # Si la petición es AJAX, devuelve un JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'mensaje': 'Producto eliminado del carrito.'})
    # Si no, redirige al carrito
    return redirect(url_for('carrito'))

if __name__ == "__main__":
    app.run(debug=True)