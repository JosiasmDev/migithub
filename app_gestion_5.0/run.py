from app import create_app

# Crea la aplicación utilizando la función create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
