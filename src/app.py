# -*- coding: utf-8 -*-
import yaml
from pkg_resources import resource_string
from sanic import Sanic
from src.views.api import bp_api
from src.views.page import bp_page
import os
import sys

from src.bus.log.config import logger
from src.bus.core.dagobah import Dagobah
from src.bus.core.components import EventHandler
from src.bus.email import get_email_handler

location = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))


def return_standard_conf():
    """ Return the sample config file. """
    result = resource_string(__name__, 'daemon/dagobahd.yml')
    result = result % {'app_secret': os.urandom(24).encode('hex')}
    return result


def replace_nones(dict_or_list):
    """Update a dict or list in place to replace
    'none' string values with Python None."""

    def replace_none_in_value(value):
        if isinstance(value, str) and value.lower() == "none":
            return None
        return value

    items = dict_or_list.items() if isinstance(dict_or_list, dict) else enumerate(dict_or_list)

    for accessor, value in items:
        if isinstance(value, (dict, list)):
            replace_nones(value)
        else:
            dict_or_list[accessor] = replace_none_in_value(value)


def get_config_file():
    config_yaml = location + '/config.yml'

    config_io = open(config_yaml, 'r')
    config = yaml.load(config_io.read())
    print(config)
    config_io.close()
    replace_nones(config)
    return config


def get_conf(config, path, default=None):
    current = config
    for level in path.split('.'):
        if level not in current:
            msg = 'Defaulting missing config key %s to %s' % (path, default)
            print(msg)
            logger.warning(msg)
            return default
        current = current[level]
    return current


def init_dagobah(config, testing=False):
    backend = get_backend(config)
    event_handler = configure_event_hooks(config)
    ssh_config = get_conf(config, 'Dagobahd.ssh_config', '~/.ssh/config')

    if not os.path.isfile(os.path.expanduser(ssh_config)):
        logger.warn("SSH config doesn't exist, no remote hosts will be listed")

    dagobah = Dagobah(backend, event_handler, ssh_config)
    known_ids = [id for id in backend.get_known_dagobah_ids()
                 if id != dagobah.dagobah_id]
    if len(known_ids) > 1:
        # need a way to handle this intelligently through config
        raise ValueError('could not infer dagobah ID, ' +
                         'multiple available in backend')

    if known_ids:
        dagobah.from_backend(known_ids[0])

    return dagobah


def configure_event_hooks(config):
    """ Returns an EventHandler instance with registered hooks. """

    def print_event_info(**kwargs):
        print(kwargs.get('event_params', {}))

    def job_complete_email(email_handler, **kwargs):
        email_handler.send_job_completed(kwargs['event_params'])

    def job_failed_email(email_handler, **kwargs):
        email_handler.send_job_failed(kwargs['event_params'])

    def task_failed_email(email_handler, **kwargs):
        email_handler.send_task_failed(kwargs['event_params'])

    handler = EventHandler()

    email_handler = get_email_handler(get_conf(config, 'Dagobahd.email', None),
                                      get_conf(config, 'Email', {}))

    if (email_handler and
                get_conf(config, 'Email.send_on_success', False) == True):
        handler.register('job_complete', job_complete_email, email_handler)

    if (email_handler and
                get_conf(config, 'Email.send_on_failure', False) == True):
        handler.register('job_failed', job_failed_email, email_handler)
        handler.register('task_failed', task_failed_email, email_handler)

    return handler


def get_backend(config):
    """ Returns a backend instance based on the Daemon config file. """

    backend_string = get_conf(config, 'Dagobahd.backend', None)

    if backend_string is None:
        from src.bus.backend.base import BaseBackend
        return BaseBackend()

    elif backend_string.lower() == 'mongo':
        backend_kwargs = {}
        for conf_kwarg in ['host', 'port', 'db',
                           'dagobah_collection', 'job_collection',
                           'log_collection']:
            backend_kwargs[conf_kwarg] = get_conf(config,
                                                  'MongoBackend.%s' % conf_kwarg)
        backend_kwargs['port'] = int(backend_kwargs['port'])

        try:
            from src.bus.backend.mongo import MongoBackend
        except:
            raise ImportError('Could not initialize the MongoDB Backend. Are you sure' +
                              ' the optional drivers are installed? If not, try running ' +
                              '"pip install pymongo" to install them.')
        return MongoBackend(**backend_kwargs)

    raise ValueError('unknown backend type specified in conf')


def create_app():
    # TODO: should consider the env prod or test ,or default

    app = Sanic(__name__)
    config = get_config_file()

    dagobah = init_dagobah(config)
    app.config['dagobah'] = dagobah

    app.blueprint(bp_page)
    app.blueprint(bp_api)

    # app.config.from_object(settings)
    return app
