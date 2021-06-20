from dynaconf import Dynaconf
import logging
import os


settings = Dynaconf(
    environments=True,
    settings_files=[os.getenv('CONFIG_FILE', 'settings.json')]
)


def set_log_level(log_level="INFO"):
    log_format = '%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] %(message)s'

    logging.basicConfig(
        datefmt='%Y-%m-%dT%H:%M:%S%z',
        format=log_format,
        level=log_level
    )
