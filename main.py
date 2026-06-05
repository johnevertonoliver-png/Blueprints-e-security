from dotenv import load_dotenv

load_dotenv()                 # Carrega o .env antes de criar a app

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)