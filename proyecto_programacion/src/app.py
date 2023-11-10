# Johanca Santos/2022-1772

# Formulario crud utilizando flask y mysql 

# Importamos las librerias y el módulo flash
from flask import Flask, render_template, request, redirect, url_for
import os
import database as db
import flash

# Definimos el directorio del proyecto y el directorio de plantillas.
directorio_proyecto = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
directorio_plantillas = os.path.join(directorio_proyecto, 'src', 'templates')

# Creamos una instancia en flask
app = Flask(__name__, template_folder = directorio_plantillas)



##### Rutas de la aplicación #####

# Ruta principal que va a obtener y mostrar todos los usuarios

@app.route('/')
def Obtener_usuarios():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuarios")
    mi_resultado = cursor.fetchall()


    # Conviertimos los datos a un formato de diccionario 
    insertar_objetos = []
    nombre_columnas = [column[0] for column in cursor.description]
    for record in mi_resultado:
        insertar_objetos.append(dict(zip(nombre_columnas, record)))
    cursor.close()
    return render_template('index.html', data=insertar_objetos)



#### Ruta para guardar usuarios en la base de datos ####

@app.route('/usuarios', methods=['POST'])
def Agregar_usuario():
    id = request.form['id']
    nombreusuario = request.form['nombreusuario']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']


    # Establecemos un bucle if para verificar si tenemos los datos necesarios 

    if id and nombreusuario and nombre and apellido and telefono:
        cursor = db.database.cursor()

        # Corregiremos la consulta utilizando el campo 'id' como marcador 
        sql = "INSERT INTO usuarios (id, nombreusuario, nombre, apellido, telefono) VALUES (%s, %s, %s, %s, %s)" 

        data = (id, nombreusuario, nombre, apellido, telefono)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()

    return redirect(url_for('Obtener_usuarios'))


# Ruta para eliminar un usuario según su ID.

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM usuarios WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('Obtener_usuarios'))


# Ruta para editar la información de un usuario según su ID.

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombreusuario = request.form.get('nombreusuario')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    telefono = request.form.get('telefono')

    # Establecemos un bucle para verificar si tenemos los datos necesarios 

    if nombreusuario and nombre and apellido and telefono:
        cursor = db.database.cursor()

        # Actualiza la información del usuario en la base de datos.
        sql = "UPDATE usuarios SET nombreusuario = %s, nombre = %s, apellido = %s, telefono = %s WHERE id = %s" 

        data = (nombreusuario, nombre, apellido, telefono, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('Obtener_usuarios'))
    else:
        flash('Inserte todos los datos.')
        return redirect(url_for('Obtener_usuarios'))
    

# Para inicializar la aplicacion
if __name__ == '__main__':
    app.run(debug=True, port=4000)