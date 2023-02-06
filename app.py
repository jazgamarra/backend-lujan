from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
id_usuario_actual = None 
usuario_actual = None 

# Configurar la base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Crear el modelo de tabla en la base de datos 
class Paciente (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cedula = db.Column(db.Integer, unique = True)
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

@app.route('/index')
def index():
    return render_template('index.html', id_usuario_actual=id_usuario_actual, usuario_actual=usuario_actual) 

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
                id_usuario_actual = cedula 
                usuario_actual = paciente.__dict__
                return render_template('index.html', id_usuario_actual=id_usuario_actual, usuario_actual=usuario_actual)
            else:
                return 'La contrasenha es incorrecta. Intente de nuevo' 
        else:
            return 'El usuario no existe. Intente de nuevo' 

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
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
        id_usuario_actual = cedula 
        usuario_actual = paciente.__dict__
        return render_template('index.html', id_usuario_actual=id_usuario_actual, usuario_actual=usuario_actual)
    return render_template('register.html')



@app.route('/ficha_paciente')
def ficha_paciente(): 
    return render_template('ficha_paciente.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True) 