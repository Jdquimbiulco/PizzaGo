from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId

app = Flask(__name__)
CORS(app)
# Conexión a MongoDB
mongo_uri = "mongodb+srv://pobando:patricio7@cluster0.f3tc9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(mongo_uri)
    db = client['Pizzeria']  # Nombre de la base de datos
    usuarios_collection = db['usuarios']
    productos_collection = db['productos']
    carritos_collection = db['carrito']
    pedidos_collection = db['pedidos']
    pagos_collection = db['ventas']
    print("Conexión exitosa a MongoDB!")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    exit()

# ---------------------- Rutas para Usuarios ----------------------
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
# Agregar un usuario (puede ser administrador o cliente)
@app.route('/agregar-usuario', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    
    # Aseguramos que todos los campos necesarios estén presentes
    if not all(k in data for k in ("nombre", "correo", "telefono", "direccion", "rol", "contraseña")):
        return jsonify({'message': 'Faltan datos necesarios'}), 400
    
    # Creamos el usuario en la colección
    usuario = {
        "nombre": data['nombre'],
        "correo": data['correo'],
        "telefono": data['telefono'],
        "direccion": data['direccion'],
        "rol": data['rol'],  # Puede ser 'administrador' o 'cliente'
        "contraseña": data['contraseña']
    }
    usuarios_collection.insert_one(usuario)
    return jsonify({'message': 'Usuario agregado exitosamente'}), 201

# Obtener todos los usuarios (administradores y clientes)
@app.route('/get-usuarios', methods=['GET'])
def get_usuarios():
    usuarios = list(usuarios_collection.find())
    for usuario in usuarios:
        usuario['_id'] = str(usuario['_id'])  # Convertir ObjectId a string para JSON
    return jsonify(usuarios)

# Modificar un usuario existente
@app.route('/modificar-usuario', methods=['PUT'])
def modificar_usuario():
    data = request.get_json()
    usuario_id = data.get('id')
    
    if not usuario_id:
        return jsonify({'message': 'Falta el ID del usuario'}), 400

    usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    # Actualizamos los datos del usuario
    usuarios_collection.update_one(
        {"_id": ObjectId(usuario_id)},
        {"$set": {
            "nombre": data['nombre'],
            "telefono": data['telefono'],
            "correo": data['correo'],
            "direccion": data['direccion'],
            "rol": data['rol'],  # Puede ser 'administrador' o 'cliente'
            "contraseña": data['contraseña']
        }}
    )
    return jsonify({'message': 'Usuario modificado exitosamente'}), 200

# Eliminar un usuario
@app.route('/eliminar-usuario', methods=['DELETE'])
def eliminar_usuario():
    data = request.get_json()
    usuario_id = data.get('id')
    
    if not usuario_id:
        return jsonify({'message': 'Falta el ID del usuario'}), 400

    usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    usuarios_collection.delete_one({"_id": ObjectId(usuario_id)})
    return jsonify({'message': 'Usuario eliminado exitosamente'}), 200

# ---------------------- Rutas para Productos ----------------------

@app.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    if not all(k in data for k in ("nombre", "descripcion", "tipo", "precio", "imagen_url")):
        return jsonify({'message': 'Faltan datos necesarios'}), 400
    
    producto = {
        "nombre": data['nombre'],
        "descripcion": data['descripcion'],
        "tipo": data['tipo'],
        "precio": data['precio'],
        "imagen_url": data['imagen_url']
    }
    productos_collection.insert_one(producto)
    return jsonify({'message': 'Producto agregado exitosamente'}), 201

@app.route('/get-productos', methods=['GET'])
def get_productos():
    productos = list(productos_collection.find())
    for producto in productos:
        producto['_id'] = str(producto['_id'])
    return jsonify(productos)

@app.route('/modificar-producto', methods=['PUT'])
def modificar_producto():
    data = request.get_json()
    producto_id = data.get('id')
    
    if not producto_id:
        return jsonify({'message': 'Falta el ID del producto'}), 400

    producto = productos_collection.find_one({"_id": ObjectId(producto_id)})
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
    # Actualizamos los datos del producto
    productos_collection.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": {
            "nombre": data['nombre'],
            "descripcion": data['descripcion'],
            "tipo": data['tipo'],
            "precio": data['precio'],
            "imagen_url": data['imagen_url']
        }}
    )
    return jsonify({'message': 'Producto modificado exitosamente'}), 200

@app.route('/eliminar-producto', methods=['DELETE'])
def eliminar_producto():
    data = request.get_json()
    producto_id = data.get('id')
    
    if not producto_id:
        return jsonify({'message': 'Falta el ID del producto'}), 400

    producto = productos_collection.find_one({"_id": ObjectId(producto_id)})
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404

    productos_collection.delete_one({"_id": ObjectId(producto_id)})
    return jsonify({'message': 'Producto eliminado exitosamente'}), 200



# Obtener todos los pedidos
@app.route('/get-pedidos', methods=['GET'])
def get_pedidos():
    pedidos = list(pedidos_collection.find())
    for pedido in pedidos:
        pedido['_id'] = str(pedido['_id'])
        pedido['usuario_id'] = str(pedido['usuario_id'])
    return jsonify(pedidos)

# Obtener todas las ventas
@app.route('/get-ventas', methods=['GET'])
def get_ventas():
    ventas = list(pedidos_collection.find())
    for venta in ventas:
        venta['_id'] = str(venta['_id'])  # Convertir ObjectId a string para JSON
        venta['usuario_id'] = str(venta['usuario_id'])  # Convertir ObjectId a string
        venta['fecha_pedido'] = venta['fecha_pedido'].isoformat()  # Convertir fecha a formato legible
    return jsonify(ventas)

# ---------------------- Rutas para Carrito ----------------------

@app.route('/agregar-al-carrito', methods=['POST'])
def agregar_al_carrito():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    opciones = data.get('opciones', {})  # Opciones adicionales del producto

    if not all([usuario_id, producto_id, cantidad]):
        return jsonify({'message': 'Faltan datos necesarios'}), 400
    
    # Buscar el producto en la base de datos
    producto = productos_collection.find_one({"_id": ObjectId(producto_id)})
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
    nombre = producto['nombre']
    precio_unitario = float(producto['precio'])  # Convertir a float

    # Obtener el costo adicional de las opciones
    costo_opciones = float(opciones.get("total", 0))  # Convertir a float
    
    # Calcular el subtotal incluyendo el costo de las opciones
    subtotal = float(cantidad) * (precio_unitario + costo_opciones)  # Convertir a float

    # Verificar si el usuario ya tiene un carrito
    carrito = carritos_collection.find_one({"usuario_id": ObjectId(usuario_id)})
    
    if carrito:
        # Verificar si el producto ya está en el carrito con las mismas opciones
        for producto in carrito['productos']:
            if producto['producto_id'] == ObjectId(producto_id) and producto.get('opciones') == opciones:
                producto['cantidad'] += int(cantidad)  # Convertir a int
                producto['subtotal'] += float(subtotal)  # Convertir a float
                carritos_collection.update_one(
                    {"_id": carrito['_id']},
                    {"$set": {"productos": carrito['productos'], "total": float(carrito['total']) + subtotal}}
                )
                return jsonify({'message': 'Producto actualizado en el carrito'}), 200
        
        # Si el producto no estaba en el carrito, lo añadimos
        carritos_collection.update_one(
            {"_id": carrito['_id']},
            {"$push": {"productos": {
                "producto_id": ObjectId(producto_id),
                "nombre": nombre,
                "cantidad": int(cantidad),  # Convertir a int
                "precio_unitario": precio_unitario,
                "subtotal": subtotal,  # Ya es float
                "opciones": opciones  # Guardar opciones seleccionadas
            }}, "$set": {"total": float(carrito['total']) + subtotal}}  # Convertir a float
        )
    else:
        # Crear un nuevo carrito
        nuevo_carrito = {
            "usuario_id": ObjectId(usuario_id),
            "productos": [{
                "producto_id": ObjectId(producto_id),
                "nombre": nombre,
                "cantidad": int(cantidad),  # Convertir a int
                "precio_unitario": precio_unitario,
                "subtotal": subtotal,  # Ya es float
                "opciones": opciones  # Guardar opciones seleccionadas
            }],
            "total": subtotal  # Ya es float
        }
        carritos_collection.insert_one(nuevo_carrito)
    
    return jsonify({'message': 'Producto agregado al carrito'}), 201
# Eliminar producto del carrito
@app.route('/eliminar-del-carrito', methods=['DELETE'])
def eliminar_del_carrito():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    producto_id = data.get('producto_id')
    
    if not all([usuario_id, producto_id]):
        return jsonify({'message': 'Faltan datos necesarios'}), 400
    
    carrito = carritos_collection.find_one({"usuario_id": ObjectId(usuario_id)})
    if not carrito:
        return jsonify({'message': 'Carrito no encontrado'}), 404
    
    productos_actualizados = [p for p in carrito['productos'] if p['producto_id'] != ObjectId(producto_id)]
    nuevo_total = sum(p['subtotal'] for p in productos_actualizados)
    
    carritos_collection.update_one(
        {"_id": carrito['_id']},
        {"$set": {"productos": productos_actualizados, "total": nuevo_total}}
    )
    
    return jsonify({'message': 'Producto eliminado del carrito'}), 200

@app.route("/carrito/<usuario_id>", methods=["GET"])
def obtener_carrito(usuario_id):
    try:
        # Verificar si `usuario_id` es un ObjectId válido
        if not ObjectId.is_valid(usuario_id):
            return jsonify({"error": "ID de usuario no válido"}), 400

        # Buscar el carrito del usuario en la base de datos
        carrito = carritos_collection.find_one({"usuario_id": ObjectId(usuario_id)})

        # Si el usuario no tiene carrito, devolver estructura vacía
        if not carrito:
            return jsonify({"productos": []}), 200

        # Convertir `_id` y `producto_id` a cadenas para evitar errores en JSON
        carrito["_id"] = str(carrito["_id"])
        carrito["usuario_id"] = str(carrito["usuario_id"])
        for producto in carrito.get("productos", []):
            producto["producto_id"] = str(producto["producto_id"])

        return jsonify(carrito), 200

    except Exception as e:
        return jsonify({"error": f"Error al obtener el carrito: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True, port=5000)


"""
# ---------------------- Rutas para Pedidos ----------------------

# Crear un pedido con productos identificados por nombre
@app.route('/realizar-pedido', methods=['POST'])
def realizar_pedido():
    data = request.get_json()
    
    if not all(k in data for k in ("usuario_id", "productos", "total", "metodo_pago", "estado", "direccion_entrega")):
        return jsonify({'message': 'Faltan datos necesarios'}), 400

    # Reemplazar los nombres de productos con sus detalles completos (precio, descripción, etc.)
    productos_completos = []
    for producto_nombre in data['productos']:
        producto = productos_collection.find_one({"nombre": producto_nombre})
        if producto:
            # Solo guardamos la información básica necesaria, como nombre y precio
            productos_completos.append({
                "nombre": producto['nombre'],
                "descripcion": producto['descripcion'],
                "precio": producto['precio'],
                "tipo": producto['tipo'],
                "imagen_url": producto['imagen_url']
            })
        else:
            return jsonify({'message': f'Producto {producto_nombre} no encontrado en el inventario'}), 404

    pedido = {
        "usuario_id": ObjectId(data['usuario_id']),
        "productos": productos_completos,
        "total": data['total'],
        "metodo_pago": data['metodo_pago'],
        "estado": data['estado'],
        "direccion_entrega": data['direccion_entrega'],
        "fecha_pedido": pd.to_datetime('today')
    }
    
    pedidos_collection.insert_one(pedido)
    return jsonify({'message': 'Pedido registrado exitosamente'}), 201

# Modificar un pedido existente con productos identificados por nombre
@app.route('/modificar-pedido/<string:id_pedido>', methods=['PUT'])
def modificar_pedido(id_pedido):
    try:
        pedido_id = ObjectId(id_pedido)
    except Exception as e:
        return jsonify({'message': 'ID de pedido inválido'}), 400

    # Buscar el pedido existente
    pedido = pedidos_collection.find_one({"_id": pedido_id})
    if not pedido:
        return jsonify({'message': 'Pedido no encontrado'}), 404
    
    # Obtener los nuevos datos del pedido
    data = request.get_json()

    # Modificar los productos por su nombre
    updated_data = {}
    if 'productos' in data:
        productos_completos = []
        for producto_nombre in data['productos']:
            producto = productos_collection.find_one({"nombre": producto_nombre})
            if producto:
                productos_completos.append({
                    "nombre": producto['nombre'],
                    "descripcion": producto['descripcion'],
                    "precio": producto['precio'],
                    "tipo": producto['tipo'],
                    "imagen_url": producto['imagen_url']
                })
            else:
                return jsonify({'message': f'Producto {producto_nombre} no encontrado en el inventario'}), 404
        updated_data["productos"] = productos_completos
    if 'total' in data:
        updated_data["total"] = data['total']
    if 'metodo_pago' in data:
        updated_data["metodo_pago"] = data['metodo_pago']
    if 'estado' in data:
        updated_data["estado"] = data['estado']
    if 'direccion_entrega' in data:
        updated_data["direccion_entrega"] = data['direccion_entrega']

    # Actualizar el pedido
    pedidos_collection.update_one({"_id": pedido_id}, {"$set": updated_data})
    
    return jsonify({'message': 'Pedido modificado exitosamente'}), 200


# Buscar venta por ID de usuario
@app.route('/buscar-venta/<string:id_usuario>', methods=['GET'])
def buscar_venta(id_usuario):
    # Convertir el id_usuario a ObjectId
    try:
        usuario_id = ObjectId(id_usuario)
    except Exception as e:
        return jsonify({'message': 'ID de usuario inválido'}), 400

    # Buscar las ventas relacionadas con el usuario
    ventas = list(pedidos_collection.find({"usuario_id": usuario_id}))

    if not ventas:
        return jsonify({'message': 'No se encontraron ventas para este usuario'}), 404

    # Suponiendo que hay una venta única que deseas devolver
    venta = ventas[0]  # Si deseas manejar varias ventas, este paso debe ajustarse

    # Transformar cada venta para poder enviarla como JSON
    venta['_id'] = str(venta['_id'])  # Convertir ObjectId a string
    venta['usuario_id'] = str(venta['usuario_id'])  # Convertir ObjectId a string
    
    return jsonify({'venta': venta}), 200

# Eliminar ventas de un usuario
@app.route('/eliminar-venta/<string:id_usuario>', methods=['DELETE'])
def eliminar_venta(id_usuario):
    # Convertir el id_usuario a ObjectId
    try:
        usuario_id = ObjectId(id_usuario)
    except Exception as e:
        return jsonify({'message': 'ID de usuario inválido'}), 400

    # Buscar y eliminar todas las ventas relacionadas con el usuario
    result = pedidos_collection.delete_many({"usuario_id": usuario_id})

    if result.deleted_count == 0:
        return jsonify({'message': 'No se encontraron ventas para eliminar'}), 404

    return jsonify({'message': f'Se eliminaron {result.deleted_count} ventas del usuario'}), 200

@app.route('/eliminar-pedido/<string:id_pedido>', methods=['DELETE'])
def eliminar_pedido(id_pedido):
    try:
        pedido_id = ObjectId(id_pedido)
    except Exception as e:
        return jsonify({'message': 'ID de pedido inválido'}), 400

    pedido = pedidos_collection.find_one({"_id": pedido_id})
    if not pedido:
        return jsonify({'message': 'Pedido no encontrado'}), 404

    pedidos_collection.delete_one({"_id": pedido_id})
    return jsonify({'message': 'Pedido eliminado exitosamente'}), 200
"""