from fastapi import FastAPI
from fastapi.logger import logger
import logging
import google.cloud.logging

from app.logging.google.filter import GoogleCloudLogFilter


def setup_google_logging(app: FastAPI):
    client = google.cloud.logging.Client()
    handler = client.get_default_handler()
    handler.setLevel(logging.DEBUG)
    handler.filters = []
    handler.addFilter(GoogleCloudLogFilter(project=client.project))
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
