# coding:utf-8
from sanic import response, request
from sanic import Blueprint
from jinja2 import Environment, PackageLoader, select_autoescape
from .api import get_jobs  # import_job

from src.config import Settings

settings = Settings()

bp_page = Blueprint('page')
bp_page.static('/static', settings.Dagobahd.BASE_DIR + '/src/static')

""" Views for Dagobah daemon. """
dagobah = ''


@bp_page.listener('before_server_start')
async def init_global_variable(app, loop):
    global dagobah
    dagobah = app.config['dagobah']


# jinjia2 config
env = Environment(
    loader=PackageLoader('src.views.page', '../templates'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return response.html(template.render(kwargs))


@bp_page.route('/favicon.ico')
async def favicon_redirect(request):
    base_dir = settings.Dagobahd.BASE_DIR + '/src/static/' + 'img/favicon.ico'
    return response.file(base_dir, headers={'mimetype': 'image/vnd.microsoft.icon'})


@bp_page.route('/', methods=['GET'])
async def index_route(request):
    """ Redirect to the dashboard. """
    return response.redirect('/jobs')


@bp_page.route('/jobs', methods=['GET'])
async def jobs(request):
    """ Show information on all known Jobs. """

    job_list = await get_jobs(request)
    return template('jobs.html',
                    jobs=job_list)


@bp_page.route('/jobs/import', methods=['POST'])
def jobs_import_view():
    """ Import a Job and redirect to the Jobs page. """
    import_job()
    return response.redirect(request.app.url_for('jobs'))


@bp_page.route('/job/<job_id>', methods=['GET'])
async def job_detail(request, job_id=None):
    """ Show a detailed description of a Job's status. """
    current_jobs = dagobah._serialize().get('jobs', {})
    jobs = [job for job in current_jobs if str(job['job_id']) == job_id]
    if not jobs:
        raise ValueError('not find any jobs')
    return template('job_detail.html', job=jobs[0], hosts=dagobah.get_hosts())


@bp_page.route('/job/<job_id>/<task_name>', methods=['GET'])
async def task_detail(request, job_id=None, task_name=None):
    """ Show a detailed description of a specific task. """
    jobs = dagobah._serialize().get('jobs', {})
    job = [job for job in jobs if str(job['job_id']) == job_id][0]
    return template('task_detail.html',
                    job=job,
                    task_name=task_name,
                    task=[task for task in job['tasks']
                          if task['name'] == task_name][0])


@bp_page.route('/job/<job_id>/<task_name>/<log_id>', methods=['GET'])
async def log_detail(request, job_id=None, task_name=None, log_id=None):
    """ Show a detailed description of a specific log. """
    jobs = dagobah._serialize().get('jobs', {})
    job = [job for job in jobs if str(job['job_id']) == job_id][0]
    return template('log_detail.html',
                    job=job,
                    task_name=task_name,
                    task=[task for task in job['tasks']
                          if task['name'] == task_name][0],
                    log_id=log_id)


@bp_page.route('/settings', methods=['GET'])
def settings_view():
    """ View for managing app-wide configuration. """
    return template('settings.html')
