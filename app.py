from includes.index import *
from car import *
from schema import schema

app.add_url_rule(
        '/cars',
        view_func=GraphQLView.as_view(
            'cars',
            schema=schema,
            graphiql=True   # for having the GraphiQL interface
        )
    )

@app.route('/createdb')
def create_db():
    Base.metadata.create_all(bind=engine)
    return 'db created'

app.debug = True

server = Server(app.wsgi_app)

if __name__ == "__main__":
    server.serve(port=3000)