from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la conexión a la base de datos en XAMPP
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'       # Usuario por defecto en XAMPP
app.config['MYSQL_PASSWORD'] = ''       # Contraseña por defecto en XAMPP (vacía)
app.config['MYSQL_DB'] = 'prueba_crud'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

# 1. READ (Leer) - Mostrar todas las notas
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, texto FROM notas")
    todas_las_notas = cur.fetchall()
    cur.close()
    return render_template('index.html', notas=todas_las_notas)

# 2. CREATE (Crear) - Insertar una nueva nota
@app.route('/agregar', methods=['POST'])
def agregar_nota():
    if request.method == 'POST':
        texto_nota = request.form['contenido_nota']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notas (texto) VALUES (%s)", (texto_nota,))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))

# 3. DELETE (Eliminar) - Borrar una nota por su ID
@app.route('/eliminar/<int:id>')
def eliminar_nota(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notas WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

# 4. UPDATE - PASO A: Buscar la nota por ID y cargarla en la pantalla
@app.route('/editar/<int:id>')
def editar_nota(id):
    cur = mysql.connection.cursor()
    # Buscamos únicamente la nota que el usuario seleccionó
    cur.execute("SELECT id, texto FROM notas WHERE id = %s", (id,))
    nota_a_editar = cur.fetchone() 
    
    # Traemos también toda la lista para que no se vacíe la pantalla al editar
    cur.execute("SELECT id, texto FROM notas")
    todas_las_notas = cur.fetchall()
    cur.close()
    
    # Enviamos la lista completa Y la nota específica al HTML
    return render_template('index.html', notas=todas_las_notas, nota_actual=nota_a_editar)

# 5. UPDATE - PASO B: Guardar los cambios editados en MySQL
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_nota(id):
    if request.method == 'POST':
        nuevo_texto = request.form['contenido_nota']
        
        cur = mysql.connection.cursor()
        # Modificamos el registro que coincida con el ID usando la cláusula WHERE
        cur.execute("UPDATE notas SET texto = %s WHERE id = %s", (nuevo_texto, id))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
