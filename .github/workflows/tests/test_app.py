from app import app

def test_home():
    # Prueba que la página principal responda correctamente
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_book_route():
    # Prueba que la ruta de libros funcione
    client = app.test_client()
    response = client.get('/book?title=quijote')
    assert response.status_code == 200