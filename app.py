from includes.index import *

@app.route('/createdb')
def create_db():
    Base.metadata.create_all(bind=engine)
    return 'db created'

app.debug = True

server = Server(app.wsgi_app)
server.serve(port=3000)
