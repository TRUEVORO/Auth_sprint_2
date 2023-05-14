from datetime import datetime
from http import HTTPStatus

from flask import Flask, Response, jsonify, request

from core import settings

from .redis import redis_storage


def configure_rate_limit(app: Flask) -> None:
    """Configures a rate limiter for the given Flask app."""

    @app.before_request
    def before_request() -> None | tuple[Response, HTTPStatus]:
        pipe = redis_storage.redis.connection.pipeline()
        now = datetime.now()

        key = f'{request.remote_addr}:{now.minute}'

        pipe.incr(key, 1)
        pipe.expire(key, 59)

        result = pipe.execute()

        request_number = result[0]
        if request_number > settings.request_limit_per_minute:
            return jsonify({'error': 'Too many requests per minute'}), HTTPStatus.TOO_MANY_REQUESTS
