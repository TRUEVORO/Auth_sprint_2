from flask import Flask
from pydantic import PostgresDsn

from api.v1 import admin_routes, auth_routes
from core import settings
from extensions import configure_rate_limit, configure_tracer, db, init_db, init_jwt, init_migrate, init_swagger


def create_app(postgres_dsn: PostgresDsn, testing: bool = False) -> Flask:
    app = Flask(__name__)  # noqa

    if testing:
        app.config['TESTING'] = testing
        settings.enable_tracing = False

    app.secret_key = settings.secret_key
    app.register_blueprint(admin_routes)
    app.register_blueprint(auth_routes)

    init_db(app, postgres_dsn)
    init_jwt(app)
    init_migrate(app, db)
    init_swagger(app)

    configure_rate_limit(app)

    if settings.enable_tracer:
        configure_tracer(app)

    return app


app = create_app(settings.postgres_dsn)


if __name__ == '__main__':
    app.run(debug=True)
