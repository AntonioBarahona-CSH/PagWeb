from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

# Crea la base de datos si no existe
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS formulario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO formulario 
        (Tunombre, Numid, Escuela, Edad, Maestro, Correo, sexo, Numtel, Nacimiento, Direccion, aceptar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()

    return render_template('confirm.html')

@app.route('/ver-datos')
def ver_datos():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM formulario')
    datos = c.fetchall()
    conn.close()
    return render_template('ver_datos.html', datos=datos)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

