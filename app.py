from flask import Flask, render_template_string
import psycopg2

app = Flask(__name__)

# Configuración de PostgreSQL (cambia estos valores)
DB_CONFIG = {
    "host": "db.internal",  # Usará el Hybrid Connection para redirigir a tu máquina
    "port": 5432,
    "database": "productosdb",
    "user": "admin",
    "password": "password123"
}

@app.route('/')
def mostrar_productos():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conn.close()
        
        # HTML para mostrar los datos
        html = """
        <h1>Productos desde PostgreSQL local</h1>
        <table border="1">
            <tr><th>ID</th><th>Nombre</th><th>Precio</th></tr>
            {% for producto in productos %}
            <tr><td>{{ producto[0] }}</td><td>{{ producto[1] }}</td><td>{{ producto[2] }}</td></tr>
            {% endfor %}
        </table>
        """
        return render_template_string(html, productos=productos)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
