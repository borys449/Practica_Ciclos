from flask import Flask, request, render_template_string
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Se lee desde el entorno. Este ejemplo no usa el token en ninguna ruta.
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")


@app.after_request
def agregar_cabeceras_seguridad(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' https://cdn.jsdelivr.net; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'"
    )
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Librería de Pruebas</title>
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

LIBROS = {
    "quijote": {
        "title": "Don Quijote de la Mancha",
        "author": "Miguel de Cervantes",
        "desc": "Una de las obras más destacadas de la literatura española y universal."
    },
    "cien_anos": {
        "title": "Cien años de soledad",
        "author": "Gabriel García Márquez",
        "desc": "La novela fundamental del realismo mágico latinoamericano."
    },
    "principito": {
        "title": "El Principito",
        "author": "Antoine de Saint-Exupéry",
        "desc": "Un cuento poético y filosófico sobre la vida y la amistad."
    },
    "metamorfosis": {
        "title": "La metamorfosis",
        "author": "Franz Kafka",
        "desc": "Una obra maestra de la literatura del absurdo y la incomunicación."
    },
    "libro_extra": {
        "title": "Libro Extra de Prueba",
        "author": "Autor Anónimo",
        "desc": "Un libro ficticio añadido para completar el catálogo de prueba."
    }
}


@app.route("/")
def home():
    logger.info("Acceso a la página principal de la librería.")
    content = """
        <h1 class="text-primary mb-3">📖 Librería de Pruebas</h1>
        <p class="text-muted">Selecciona un libro para ver su información:</p>
        <ul class="list-group mb-3">
            <li class="list-group-item"><a href="/book?title=quijote">Ver El Quijote</a></li>
            <li class="list-group-item"><a href="/book?title=cien_anos">Ver Cien años de soledad</a></li>
            <li class="list-group-item"><a href="/book?title=principito">Ver El Principito</a></li>
            <li class="list-group-item"><a href="/book?title=metamorfosis">Ver La metamorfosis</a></li>
            <li class="list-group-item"><a href="/book?title=libro_extra">Ver Libro Extra</a></li>
        </ul>
    """
    return render_template_string(BASE_TEMPLATE, content=content)


@app.route("/book")
def view_book():
    logger.info("Solicitud para consultar un libro.")
    book_key = request.args.get("title", "default")
    book = LIBROS.get(book_key)

    if book is None:
        content = """
            <h2 class="text-danger">¡Libro no encontrado!</h2>
            <p class="text-muted">El libro que buscas no existe en este catálogo.</p>
            <a href="/" class="btn btn-secondary mt-3">Volver al inicio</a>
        """
    else:
        # Los datos interpolados vienen del catálogo fijo del servidor.
        content = f"""
            <h2 class="text-success">{book["title"]}</h2>
            <h5 class="text-secondary">Autor: {book["author"]}</h5>
            <p class="mt-3">{book["desc"]}</p>
            <a href="/" class="btn btn-secondary mt-3">Volver al inicio</a>
        """

    return render_template_string(BASE_TEMPLATE, content=content)


if __name__ == "__main__":
    # Solo para desarrollo local; no usar el servidor de desarrollo en producción.
    app.run(debug=False, host="127.0.0.1", port=5000)
