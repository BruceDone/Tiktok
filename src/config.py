# -*- coding: utf-8 -*-
import os


class Settings(object):
    class Dagobahd(object):
        DEBUG = False
        HOST = '127.0.0.1'
        PORT = 9000

        # the app's secret key, used for maintaining user sessions
        APP_SECRET = '%(app_secret)s'

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        # credentials for single-user auth
        AUTH_DISABLED = False
        PASSWORD = 'dagobah'

        # choose one of the available backends
        # None: Dagobah will not use a backend to permanently store data
        # mongo: store results in MongoDB. see the MongoBackend section in this file
        BACKEND = None

        # choose one of the available email templates
        # None: Dagobah won't send you emails when a job finishes or fails
        # text: Simple text format
        # basic: Simple, tabular HTML email
        EMAIL = 'basic'

        # SSH config file for remote host authentication.
        # If you don't plan on executing tasks on remote servers, leaving this
        # default is fine. If you need to create an ssh config, the default
        # location is sugested
        SSH_CONFIG = '~ /.ssh / config'

    class Logging(object):
        # Logging settings for everything other than Flask requests, e.g.
        # jobs starting and stopping, database logging, SSH problems
        class Core(object):
            ENABLED = 'True'

            # specify a full path to the log file
            # alternatively, specify "default" to log to a file in the dagobahd directory
            # You can also specify None to disable logging to a file
            LOGFILE = 'default'

            # if True, also log to stdout
            LOG_TO_STDOUT = 'False'

            # specify the log level to use
            # choose one of [debug, info, warning, error, critical]
            LOGLEVEL = 'info'

        # Logging settings for web requests through the Flask app
        class Requests(object):
            ENABLED = 'False'

            # specify a full path to the log file
            # alternatively, specify "default" to log to a file in the dagobahd directory
            # You can also specify None to disable logging to a file
            LOGFILE = 'default'

            # if True, also log to stdout
            LOG_TO_STDOUT = False

            # specify the log level to use.
            # choose one of [debug, info, warning, error, critical]
            # If Dagobahd.debug is True, this will always be debug
            LOGLEVEL = 'info'

    class Email(object):
        # set host and port of the SMTP server to use to send mail
        # e.g. host: smtp.gmail.com   port: 587
        HOST = 'smtp.gmail.com'
        PORT = '587'

        # email server authentication
        AUTH_REQUIRED = True
        USER = None
        PASSWORD = None

        # tls is required for some mail servers, specifically Gmail
        USE_TLS = True

        # from address in the emails from Dagobah.
        # supports the following special variables within curly brackets {}
        # {HOSTNAME}: the machine's hostname
        FROM_ADDRESS = 'dagobah @ {HOSTNAME}'

        # list of email addresses to send reports to, e.g. ['myemail@gmail.com']
        RECIPIENTS = []

        # sets whether Dagobah sends you emails on successful job completion
        SEND_ON_SUCCESS = True

        # sets whether Dagobah sends you emails on job and task failures
        SEND_ON_FAILURE = True

    class MongoBackend(object):
        # connection details to a mongo database
        HOST = 'localhost'
        PORT = 27017
        DB = 'dagobah'

        # names of collections within the db specified above
        DAGOBAH_COLLECTION = 'dagobah'
        JOB_COLLECTION = 'dagobah_job'
        LOG_COLLECTION = 'dagobah_log'
