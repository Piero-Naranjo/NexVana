from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask (__name__)
app.secret_key = 'cairocoders-ednalan'

DB_HOST = "localhost"
DB_NAME = "PruebaLogin"
DB_USER = "postgres"
DB_PASS = "12345"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)



def get_common_data():
    return {
            'ruta_css': url_for('static', filename='css/style.css'),
            
            'ruta_menu_img': url_for('static', filename='img/menu.png'),    
            
            'ruta_flash_img': url_for('static', filename='img/flash.png'),
            
            'ruta_play_img': url_for('static', filename='img/play.png'),
            #bloque 1
            'ruta_1_img': url_for('static', filename='img/1.jpg'),
            
            'ruta_2_img': url_for('static', filename='img/2.jpg'),
            
            'ruta_3_img': url_for('static', filename='img/3.jpg'),
            
            'ruta_4_img': url_for('static', filename='img/4.jpg'),
            # 4 mas
            'ruta_5_img': url_for('static', filename='img/5.jpg'),
            
            'ruta_6_img': url_for('static', filename='img/6.jpg'),
            
            'ruta_7_img': url_for('static', filename='img/7.jpg'),
            
            'ruta_8_img': url_for('static', filename='img/8.jpg'),
            #bloque 2
            'ruta_9_img': url_for('static', filename='img/9.jpg'),
            
            'ruta_10_img': url_for('static', filename='img/10.jpg'),
            
            'ruta_11_img': url_for('static', filename='img/11.jpg'),
            
            'ruta_12_img': url_for('static', filename='img/12.jpg'),
            # 4 mas 
            'ruta_13_img': url_for('static', filename='img/13.jpg'),
            
            'ruta_14_img': url_for('static', filename='img/14.jpg'),
            
            'ruta_15_img': url_for('static', filename='img/15.jpg'),
            
            'ruta_16_img': url_for('static', filename='img/16.jpg'),
            #bloque 3
            'ruta_17_img': url_for('static', filename='img/17.jpg'),
            
            'ruta_18_img': url_for('static', filename='img/18.jpg'),
            
            'ruta_19_img': url_for('static', filename='img/19.jpg'),
            
            'ruta_20_img': url_for('static', filename='img/20.jpg'),
            # 4 mas
            'ruta_21_img': url_for('static', filename='img/21.jpg'),
            
            'ruta_22_img': url_for('static', filename='img/22.jpg'),
            
            'ruta_23_img': url_for('static', filename='img/23.jpg'),
            
            'ruta_24_img': url_for('static', filename='img/24.jpg'),
            
            
            #perfiles foto
            'ruta_piero_img': url_for('static', filename='img/perfil_piero.jpg'),
            
            'ruta_daniel_img': url_for('static', filename='img/perfil_daniel.jpg'),
            
            'ruta_andres_img': url_for('static', filename='img/perfil_andres.jpg'),
            
            'nosotros_css': url_for('static', filename='css/nosotros.css'),
            
            #estilopeliculas
            'ruta_css_pelicula': url_for('static', filename='css/peliculaEstilo.css'),
            
            
            #contacto
            'contacto_css': url_for('static', filename='css/contacto.css'),
            
            #login
            'ruta_login': url_for('static', filename='css/estilos.css'),
            
            #ruta boton arriba
            'ruta_b_img': url_for('static', filename='img/b.png'),
            #ruta del js
            'ruta_js': url_for('static', filename='js/script.js'),
    }
    
@app.route('/')
def index():
    data = get_common_data()
    if 'loggedin' in session:
        # User is logged in, show them the home page with logout button
        return render_template('index.html', username=session['username'], data=data, is_logged_in=True)
    return render_template('index.html', data=data, is_logged_in=False)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
    
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
    
        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('index'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Nombre de usuario/contraseña incorrectos')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Nombre de usuario/contraseña incorrectos')
    
    return render_template('secondary_templates/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('¡La cuenta ya existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('¡Dirección de correo electrónico no válida!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('¡El nombre de usuario debe contener solo caracteres y números!')
        elif not username or not password or not email:
            flash('¡Por favor rellena el formulario!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
            conn.commit()
            flash('¡Se ha registrado exitosamente!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('¡Por favor rellena el formulario!')
    # Show registration form with message (if any)
    return render_template('secondary_templates/register.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to home page
    return redirect(url_for('index'))

@app.route('/contacto')
def contacto():
    data = get_common_data()
    return render_template('secondary_templates/contacto.html',data=data)

@app.route('/nosotros')
def nosotros():
    data = get_common_data()
    return render_template('secondary_templates/nosotros.html',data = data)


#peliculas blqoeu 1
@app.route('/pelicula_Miles2')
def pelicula_Miles2():
    data = get_common_data()
    return render_template('movie_templates/pelicula_spidermanMiles2.html', data=data)


@app.route('/pelicula_flash')
def pelicula_flash():
    data = get_common_data()
    return render_template('movie_templates/pelicula_flash.html', data=data)


@app.route('/pelicula_mario')
def pelicula_mario():
    data = get_common_data()
    return render_template('movie_templates/pelicula_mario.html', data=data)

@app.route('/pelicula_avatar2')
def pelicula_avatar2():
    data = get_common_data()
    return render_template('movie_templates/pelicula_avatar2.html', data=data)
############# 4 mas
@app.route('/pelicula_transformers')
def pelicula_transformers():
    data = get_common_data()
    return render_template('movie_templates/pelicula_transformers.html', data=data)

@app.route('/pelicula_oppenheimer')
def pelicula_oppenheimer():
    data = get_common_data()
    return render_template('movie_templates/pelicula_oppenheimer.html', data=data)

@app.route('/pelicula_barbie')
def pelicula_barbie():
    data = get_common_data()
    return render_template('movie_templates/pelicula_barbie.html', data=data)

@app.route('/pelicula_guardianes3')
def pelicula_guardianes3():
    data = get_common_data()
    return render_template('movie_templates/pelicula_guardianes3.html', data=data)


#peliculas bloque 2
@app.route('/pelicula_dampyr')
def pelicula_dampyr():
    data = get_common_data()
    return render_template('movie_templates/pelicula_dampyr.html', data=data)

@app.route('/pelicula_break_Even')
def pelicula_break_Even():
    data = get_common_data()
    return render_template('movie_templates/pelicula_break_Even.html', data=data)

@app.route('/pelicula_La_Huésped')
def pelicula_La_Huésped():
    data = get_common_data()
    return render_template('movie_templates/pelicula_La_Huésped.html', data=data)

@app.route('/pelicula_Hobbit_5ejercitos')
def pelicula_Hobbit_5ejercitos():
    data = get_common_data()
    return render_template('movie_templates/pelicula_Hobbit_5ejercitos.html', data=data)

############# 4 mas

@app.route('/pelicula_elysium')
def pelicula_elysium():
    data = get_common_data()
    return render_template('movie_templates/pelicula_elysium.html', data=data)

@app.route('/pelicula_paradise')
def pelicula_paradise():
    data = get_common_data()
    return render_template('movie_templates/pelicula_paradise.html', data=data)

@app.route('/pelicula_megalodon')
def pelicula_megalodon():
    data = get_common_data()
    return render_template('movie_templates/pelicula_megalodon.html', data=data)

@app.route('/pelicula_Island_Escape')
def pelicula_Island_Escape():
    data = get_common_data()
    return render_template('movie_templates/pelicula_Island_Escape.html', data=data)

#pelicula bloque 3
@app.route('/pelicula_gran_turismo')
def pelicula_gran_turismo():
    data = get_common_data()
    return render_template('movie_templates/pelicula_gran_turismo.html', data=data)

@app.route('/pelicula_Agente_Stone')
def pelicula_Agente_Stone():
    data = get_common_data()
    return render_template('movie_templates/pelicula_Agente_Stone.html', data=data)

@app.route('/pelicula_tristan')
def pelicula_tristan():
    data = get_common_data()
    return render_template('movie_templates/pelicula_tristan.html', data=data)

@app.route('/pelicula_Warrior')
def pelicula_Warrior():
    data = get_common_data()
    return render_template('movie_templates/', data=data)

############# 4 mas
@app.route('/pelicula_Football')
def pelicula_Football():
    data = get_common_data()
    return render_template('movie_templates/pelicula_Football.html', data=data)

@app.route('/pelicula_Señal')
def pelicula_Señal():
    data = get_common_data()
    return render_template('movie_templates/pelicula_Señal.html', data=data)

@app.route('/pelicula_Frente')
def pelicula_Frente():
    data = get_common_data()
    return render_template('movie_templates/pelicula_Frente.html', data=data)

@app.route('/pelicula_tortugas')
def pelicula_tortugas():
    data = get_common_data()
    return render_template('movie_templates/pelicula_tortugas.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)