from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

# Variable global para guardar el usuario actual de la sesion 
usuario_actual = None 

# Configurar la base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Crear el modelo de tabla en la base de datos 
class Paciente (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cedula = db.Column(db.Integer)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    tipo_de_sangre = db.Column(db.String(10))
    alergia = db.Column(db.String(100))
    seguro_medico = db.Column(db.String(100))
    contacto_nombre = db.Column(db.String(100))
    contacto_telefono = db.Column(db.String(100))
    contacto_parentesco = db.Column(db.String(100))
    password = db.Column(db.String(100))

    # Constructor de la clase
    # Sirve para crear un objeto que se guardara en la base de datos
    def __init__ (self, cedula, nombre, apellido, tipo_de_sangre, alergia, seguro_medico, contacto_nombre, contacto_telefono, contacto_parentesco, password):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_de_sangre = tipo_de_sangre
        self.alergia = alergia
        self.seguro_medico = seguro_medico
        self.contacto_nombre = contacto_nombre
        self.contacto_telefono = contacto_telefono
        self.contacto_parentesco = contacto_parentesco
        self.password = password

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ficha_paciente',  methods=['GET', 'POST'])
def ficha_paciente():
    global usuario_actual 
    return render_template('ficha_paciente.html', usuario_actual=usuario_actual) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Acceder a los datos del formulario 
        cedula = request.form['cedula']
        password = request.form['password']

        # Buscar el usuario en la base de datos
        paciente = Paciente.query.filter_by(cedula=cedula).first()

        # Verificar si el usuario existe y la contraseña es correcta
        if paciente is not None: 
            if paciente.password == password:
                global usuario_actual 
                usuario_actual = paciente.__dict__
                print(f"INICIO SESION EL USUARIO {usuario_actual}")
                return redirect(url_for('ficha_paciente'))
            else:
                return 'La contrasenha es incorrecta. Intente de nuevo' 
        else:
            return 'El usuario no existe. Intente de nuevo' 

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global usuario_actual 
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo_de_sangre = request.form['tipo_de_sangre']
        alergia = request.form['alergia']
        seguro_medico = request.form['seguro_medico']
        contacto_nombre = request.form['contacto_nombre']
        contacto_telefono = request.form['contacto_telefono']
        contacto_parentesco = request.form['contacto_parentesco']
        password = request.form['password']

        paciente = Paciente(cedula, nombre, apellido, tipo_de_sangre, alergia, seguro_medico, contacto_nombre, contacto_telefono, contacto_parentesco, password)
        db.session.add(paciente)
        db.session.commit()

        # Modificamos la variable global
        usuario_actual = paciente.__dict__
        print(f"SE REGISTRO EL USUARIO {usuario_actual.nombre}")
        return redirect(url_for('ficha_paciente'))
    return render_template('register.html', usuario_actual=usuario_actual)

@app.route('/editar_ficha', methods=['GET', 'POST'])
def editar_ficha(): 
    if request.method == 'POST': 
        # Guardamos los datos del formulario 
        campo = request.form['campo']
        nuevo_valor = request.form['valor']

        # Buscamos el usuario en la base de datos
        global usuario_actual # aclaramos que nos referimos a la variable global
        paciente = Paciente.query.filter_by(cedula=usuario_actual['cedula']).first()

        # Editamos el campo que se haya seleccionado
        if campo == 'nombre':
            paciente.nombre = nuevo_valor
        elif campo == 'apellido':
            paciente.apellido = nuevo_valor
        elif campo == 'tipo_de_sangre':
            paciente.tipo_de_sangre = nuevo_valor
        elif campo == 'alergia':
            paciente.alergia = nuevo_valor
        elif campo == 'seguro_medico':
            paciente.seguro_medico = nuevo_valor
        elif campo == 'contacto_nombre':
            paciente.contacto_nombre = nuevo_valor
        elif campo == 'contacto_telefono':
            paciente.contacto_telefono = nuevo_valor
        elif campo == 'contacto_parentesco':
            paciente.contacto_parentesco = nuevo_valor
        elif campo == 'password':
            paciente.password = nuevo_valor
        elif campo == 'cedula':
            paciente.cedula = nuevo_valor 

        # Guardamos los cambios en la base de datos
        db.session.commit()

        # Actualizamos la variable usuario_actual
        usuario_actual = paciente.__dict__
        return redirect(url_for('ficha_paciente'))
    return render_template('editar_ficha.html')

@app.route('/logout')
def logout():
    global usuario_actual
    usuario_actual = None
    return render_template('home.html') 

@app.route('/borrar/<id>')
def borrar(id):
    paciente = Paciente.query.filter_by(id=id).first()
    db.session.delete(paciente)
    db.session.commit()
    return f'<h1> El paciente {id} se borro correctamente </h1>'
    
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8080) 