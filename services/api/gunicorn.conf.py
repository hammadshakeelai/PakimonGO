"""Gunicorn production configuration for PakimonGO API."""

import os

# Render (and most PaaS hosts) inject the port to listen on via $PORT.
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
graceful_timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
loglevel = "info"
