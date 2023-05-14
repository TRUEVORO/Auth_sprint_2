from flask import Flask, request
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from core import settings

tracer = trace.get_tracer(__name__)


def read_x_request_id_header(app: Flask) -> None:
    """Middleware function to read 'X-Request-Id' header from the incoming request."""

    @app.before_request
    def before_request():
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            raise RuntimeError('request id is required')


def configure_tracer(app: Flask) -> None:
    """Configures OpenTelemetry tracer for the given Flask app."""

    read_x_request_id_header(app)

    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.jaeger_dsn.host,
                agent_port=int(settings.jaeger_dsn.port),
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    FlaskInstrumentor().instrument_app(app)
