from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:contraseña@localhost/dbuser'
db = SQLAlchemy(app)


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cedula_identidad = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    primer_apellido = db.Column(db.String(50), nullable=False)
    segundo_apellido = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'cedula_identidad': self.cedula_identidad,
            'nombre': self.nombre,
            'primer_apellido': self.primer_apellido,
            'segundo_apellido': self.segundo_apellido,
            'fecha_nacimiento': self.fecha_nacimiento.strftime('%Y-%m-%d')
        }

# Endpoint para crear un usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo_usuario = Usuarios(
        cedula_identidad=data['cedula_identidad'],
        nombre=data['nombre'],
        primer_apellido=data['primer_apellido'],
        segundo_apellido=data.get('segundo_apellido'),
        fecha_nacimiento=data['fecha_nacimiento']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

# Endpoint para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuarios.query.all()
    usuarios_dict = [usuario.to_dict() for usuario in usuarios]
    return jsonify(usuarios_dict)

# Endpoint para obtener el usuario por id
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    usuario = Usuarios.query.get(id_usuario)
    if usuario:
        return jsonify(usuario.to_dict())
    return jsonify({'message': 'Usuario no encontrado'}), 404


# Endpoint para actualizar los datos de un usuario
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    usuario = Usuarios.query.get(id_usuario)
    if usuario:
        data = request.get_json()
        # Actualiza los campos del usuario según los datos proporcionados
        usuario.cedula_identidad = data.get('cedula_identidad', usuario.cedula_identidad)
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.primer_apellido = data.get('primer_apellido', usuario.primer_apellido)
        usuario.segundo_apellido = data.get('segundo_apellido', usuario.segundo_apellido)
        usuario.fecha_nacimiento = data.get('fecha_nacimiento', usuario.fecha_nacimiento)
        # Actualiza aquí los demás campos del usuario según corresponda

        db.session.commit()
        return jsonify({'message': 'Usuario actualizado correctamente'})
    else:
        return jsonify({'message': 'Usuario no encontrado'})

# Endpoint para eliminar a un usuario por su ID
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    usuario = Usuarios.query.get(id_usuario)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'})
    else:
        return jsonify({'message': 'Usuario no encontrado'})
    

# Ruta para calcular el promedio de edades de los usuarios
@app.route('/usuarios/promedio-edad', methods=['GET'])
def calcular_promedio_edades():
    usuarios = Usuarios.query.all()
    edades = []
    today = date.today()

    for usuario in usuarios:
        edad = today.year - usuario.fecha_nacimiento.year
        if today.month < usuario.fecha_nacimiento.month or (today.month == usuario.fecha_nacimiento.month and today.day < usuario.fecha_nacimiento.day):
            edad -= 1
        edades.append(edad)

    if len(edades) > 0:
        promedio = sum(edades) / len(edades)
        return jsonify({'promedio_edades': promedio})
    else:
        return jsonify({'message': 'No hay usuarios registrados'})
    

# Endpoint para obtener la versión
@app.route('/version', methods=['GET'])
def obtener_version():
    return jsonify(
        {
            "nameSystem": "api-users",
            "version": "0.0.1",
            "developer": "Sergio Ruiz Sanjines",
            "email": "sergioruizs.srs@gmail.com"
        }
    )    

if __name__ == '__main__':
    app.run(debug=True)