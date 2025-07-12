from flask import Flask, request, render_template
import psycopg2
import os

app = Flask(__name__)

# Obtener URL de conexión de Render (usa variable de entorno)
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Crear tabla si no existe
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS formulario (
            id SERIAL PRIMARY KEY,
            Tunombre TEXT,
            Numid TEXT,
            Escuela TEXT,
            Edad INTEGER,
            Maestro TEXT,
            Correo TEXT,
            sexo TEXT,
            Numtel TEXT,
            Nacimiento TEXT,
            Direccion TEXT,
            aceptar TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = (
        request.form['Tunombre'],
        request.form['Numid'],
        request.form['Escuela'],
        request.form['Edad'],
        request.form['Maestro'],
        request.form['Correo'],
        request.form['sexo'],
        request.form['Numtel'],
        request.form['Nacimiento'],
        request.form['Direccion'],
        request.form['aceptar']
    )

    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO formulario 
        (Tunombre, Numid, Escuela, Edad, Maestro, Correo, sexo, Numtel, Nacimiento, Direccion, aceptar)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', data)
    conn.commit()
    conn.close()

    return render_template('confirm.html')

@app.route('/ver-datos')
def ver_datos():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM formulario')
    datos = c.fetchall()
    conn.close()
    return render_template('ver_datos.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
