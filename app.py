from flask import Flask, request, render_template_string
import json
import os
import sqlite3   # Code Smell: Importación no utilizada
import hashlib   # Code Smell: Otra importación no utilizada

app = Flask(__name__)

# Security Hotspot / Code Smell: Credencial hardcodeada en texto plano
ADMIN_TOKEN = "super_secret_admin_token_999"

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Librería con Alertas para Sonar</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="card shadow p-4">
            {{ content | safe }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Code Smell: Uso de print() en lugar del módulo logging
    print("DEBUG: Acceso detectado a la página principal de la librería.")
    
    content = """
        <h1 class="text-primary mb-3">📖 Librería de Pruebas SonarQube</h1>
        <p class="text-muted">Selecciona un libro para ver su contenido estático:</p>
        <ul class="list-group mb-3">
            <li class="list-group-item"><a href="/book?title=quijote">Ver El Quijote</a></li>
            <li class="list-group-item"><a href="/book?title=cien_anos">Ver Cien años de soledad</a></li>
            <li class="list-group-item"><a href="/book?title=principito">Ver El Principito</a></li>
            <li class="list-group-item"><a href="/book?title=metamorfosis">Ver La metamorfosis</a></li>
            <li class="list-group-item"><a href="/book?title=libro_extra">Ver Libro Extra</a></li>
        </ul>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/book')
def view_book():
    # Code Smell: Uso de print() repetido
    print("DEBUG: Procesando solicitud de visualización de libro...")
    book_title = request.args.get('title', 'default')
    
    # 🚨 ALERTA DE SONAR: Complejidad Cognitiva alta y Código Duplicado masivo
    if book_title == "quijote":
        title = "Don Quijote de la Mancha"
        author = "Miguel de Cervantes"
        desc = "Una de las obras más destacadas de la literatura española y universal."
        content = f"""
            <h2 class="text-success">{title}</h2>
            <h5 class="text-secondary">Autor: {author}</h5>
            <p class="mt-3">{desc}</p>
            <a href="/" class="btn btn-secondary mt-3">Volver al inicio</a>
        """
        return render_template_string(BASE_TEMPLATE, content=content)
        
    elif book_title == "cien_anos":
        title = "Cien años de soledad"
        author = "Gabriel García Márquez"
        desc = "La novela fundamental del realismo mágico latinoamericano."
        content = f"""
            <h2 class="text-success">{title}</h2>
            <h5 class="text-secondary">Autor: {author}</h5>
            <p class="mt-3">{desc}</p>
            <a href="/" class="btn btn-secondary mt-3">Volver al inicio</a>
        """
        return render_template_string(BASE_TEMPLATE, content=content)
        
    elif book_title == "principito":
        title = "El Principito"
        author = "Antoine de Saint-Exupéry"
        desc = "Un cuento poético y filosófico sobre la vida y la amistad."
        content = f"""
            <h2 class="text-success">{title}</h2>
            <h5 class="text-secondary">Autor: {author}</h5>
            <p class="mt-3">{desc}</p>
            <a href="/" class="btn btn-secondary mt-3">Volver al inicio</a>
        """
        return render_template_string(BASE_TEMPLATE, content=content)
        
    elif book_title == "metamorfosis":
        title = "La metamorfosis"
        author = "Franz Kafka"
        desc = "Una obra maestra de la literatura del absurdo y la incomunicación."
        content = f"""
            <h2 class="text-success">{title}</h2>
            <h5 class="text-secondary">Autor: {author}</h5>
            <p class="mt-3">{desc}</p>
            <a href="/" class="btn btn-secondary mt-3">Volver al inicio</a>
        """
        return render_template_string(BASE_TEMPLATE, content=content)
        
    elif book_title == "libro_extra":
        title = "Libro Extra de Prueba"
        author = "Autor Anónimo"
        desc = "Un libro ficticio añadido únicamente para inflar el código duplicado."
        content = f"""
            <h2 class="text-success">{title}</h2>
            <h5 class="text-secondary">Autor: {author}</h5>
            <p class="mt-3">{desc}</p>
            <a href="/" class="btn btn-secondary mt-3">Volver al inicio</a>
        """
        return render_template_string(BASE_TEMPLATE, content=content)
        
    else:
        error_content = """
            <h2 class="text-danger">¡Libro no encontrado!</h2>
            <p class="text-muted">El libro que buscas no existe en este catálogo rígido.</p>
            <a href="/" class="btn btn-secondary mt-3">Volver al inicio</a>
        """
        return render_template_string(BASE_TEMPLATE, content=error_content)

if __name__ == '__main__':
    # Security Hotspot: Servidor Flask en modo debug activo para producción
    app.run(debug=True, host='0.0.0.0', port=5000)