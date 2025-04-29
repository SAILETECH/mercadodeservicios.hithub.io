from flask import Flask, render_template, request, redirect, flash
import requests

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'  # Necesario para usar flash (mensajes rápidos)

# Configura tu API de Sightengine
API_USER = 'TU_API_USER'
API_SECRET = 'TU_API_SECRET'

# Palabras prohibidas
palabras_prohibidas = ["sexo", "droga", "violencia", "arma", "asesinato", "desnudo"]

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/publicar-servicio', methods=['GET', 'POST'])
def publicar_servicio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_servicio = request.form['tipo']
        imagen = request.files['imagen']

        # Verificar palabras prohibidas
        nombre_lower = nombre.lower()
        for palabra in palabras_prohibidas:
            if palabra in nombre_lower:
                flash('El nombre del servicio contiene palabras prohibidas.')
                return redirect('/publicar-servicio')

        # Verificar imagen usando Sightengine
        response = requests.post(
            'https://api.sightengine.com/1.0/check.json',
            files={'media': imagen},
            data={
                'models': 'nudity,weapon,alcohol,drugs',
                'api_user': API_USER,
                'api_secret': API_SECRET
            }
        )
        result = response.json()

        if (result['nudity']['safe'] < 0.8 or 
            result.get('weapon', 0) > 0.2 or
            result.get('alcohol', 0) > 0.2 or
            result.get('drugs', 0) > 0.2):
            flash('La imagen subida no es apropiada.')
            return redirect('/publicar-servicio')

        # Si pasa todas las verificaciones
        flash('¡Servicio publicado exitosamente!')
        return redirect('/')

    return render_template('publicar-servicio.html')

@app.route('/mi-cuenta')
def mi_cuenta():
    return render_template('mi-cuenta.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)
