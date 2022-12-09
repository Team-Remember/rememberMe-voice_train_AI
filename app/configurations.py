import os
from logging import getLogger

logger = getLogger(__name__)


class APIConfigurations:
    title = os.getenv("API_TITLE", "REMEMBERME_VOICE_TRAIN")
    description = os.getenv("API_DESCRIPTION", "Remember You from your data")
    version = os.getenv("API_VERSION", "0.1")
