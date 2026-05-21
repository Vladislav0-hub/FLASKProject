from app import create_app, db
from app.models import User, Game, Listing

app = create_app()

#Интересный декоратор нашел можно попробовать
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Game': Game, 'Listing': Listing}

if __name__ == '__main__':
    app.run(debug=True)