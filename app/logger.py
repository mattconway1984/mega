import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from app import app


def configure_logfile_logger():
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/latest.log",
        maxBytes=10240,
        backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Website Startup')


def configure_email_logger():
    auth = None
    if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
        auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
    secure = None
    if app.config["MAIL_USE_TLS"]:
        secure = ()
    mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-reply@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"], subject="Website Failure",
            credentials=auth,
            secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


# Only enable logger when not running in debug mode.
if not app.debug:
    configure_logfile_logger()
    if app.config["MAIL_SERVER"]:
        configure_email_logger()
