from app import app
from views import *

app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run(host='0.0.0.0')
