from Photo import database, app
from Photo.models import Usuario, Foto

with app.app_context():
    database.create_all()

