import argparse
import os
import logging


logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO').upper(),
)

logger = logging.getLogger('demo_app.web')


def http_server(args: argparse.Namespace, unknown_args: list[str] | None) -> None:
    import uvicorn
    dev_mode = args.dev
    log_level = args.log_level
    workers = 1 if dev_mode else int(args.workers)
    port = int(args.port)

    logger.info(f"Starting server on port {port} using {workers} workers (dev mode: {dev_mode})...")
    uvicorn.run(
        "demo_app.http_server:app",
        host="0.0.0.0",
        port=port,
        reload=dev_mode,
        access_log=True,
        log_level=log_level,
        workers=workers,
        proxy_headers=True,
        loop="uvloop",
        http="httptools",
    )


argparser = argparse.ArgumentParser(prog="python demo app")
argsubparsers = argparser.add_subparsers(required=True)

argparser_http = argsubparsers.add_parser("http", help="Start the HTTP server")
argparser_http.set_defaults(func=http_server)
argparser_http.add_argument("--port", help="Port to listen to", default=os.environ.get("PORT", 8000))
argparser_http.add_argument("--workers", help="Number of uvicorn workers", default=10)
argparser_http.add_argument("--log-level", help="Log Level", default="debug")
argparser_http.add_argument("--dev", help="Run in devevelopment mode", action="store_true")

arguments, unknown_arguments = argparser.parse_known_args()
arguments.func(arguments, unknown_arguments)
