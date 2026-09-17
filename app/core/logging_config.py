import logging
import os
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("smart_water")


def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s"
    )

    # Root application logger
    logger.setLevel(logging.INFO)

    # Console Handler
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

    # File handlers (wrapped in try-except for read-only serverless platforms like Vercel)
    try:
        os.makedirs(log_dir, exist_ok=True)
        app_log_file = os.path.join(log_dir, "application.log")
        if not any(isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "").endswith("application.log") for h in logger.handlers):
            file_handler = RotatingFileHandler(
                app_log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(log_format)
            logger.addHandler(file_handler)

        err_log_file = os.path.join(log_dir, "errors.log")
        if not any(isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "").endswith("errors.log") for h in logger.handlers):
            err_handler = RotatingFileHandler(
                err_log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
            )
            err_handler.setLevel(logging.ERROR)
            err_handler.setFormatter(log_format)
            logger.addHandler(err_handler)
    except Exception as e:
        # On Vercel / serverless, filesystem is read-only, stream to console only
        logger.info(f"File logging skipped on serverless platform: {e}")

    logger.info("Logging infrastructure initialized.")
    return logger
