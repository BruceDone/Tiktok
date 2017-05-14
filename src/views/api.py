# coding:utf-8
""" HTTP API methods for Dagobah daemon. """
import json
from src.bus.common.util import validate_dict
from sanic import Blueprint
from src.bus.func.api import api_call
from sanic import response
from io import StringIO

bp_api = Blueprint('api')
dagobah = ''


@bp_api.listener('before_server_start')
async def init_global_variable(app, loop):
    global dagobah
    dagobah = app.config['dagobah']


@bp_api.route('/api/jobs', methods=['GET'])
@api_call
async def get_jobs(request):
    return dagobah._serialize().get('jobs', {})


@bp_api.route('/api/job', methods=['GET'])
@api_call
async def get_job(request):
    args = dict(request.args)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate info')

    job = dagobah.get_job(args['job_name'])
    if not job:
        raise ValueError('not find any job')

    return job._serialize()


@bp_api.route('/api/logs', methods=['GET'])
@api_call
async def get_run_log_history(request):
    args = dict(request.args)
    if not validate_dict(args,
                         required=['job_name', 'task_name'],
                         job_name=str,
                         task_name=str):
        raise ValueError('not validate json object')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate task')
    return task.get_run_log_history()


@bp_api.route('/api/log', methods=['GET'])
@api_call
async def get_log(request):
    args = dict(request.args)
    if not validate_dict(args,
                         required=['job_name', 'task_name', 'log_id'],
                         job_name=str,
                         task_name=str,
                         log_id=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate task')
    return task.get_run_log(args['log_id'])


@bp_api.route('/api/head', methods=['GET'])
@api_call
async def head_task(request):
    args = dict(request.args)
    if not validate_dict(args,
                         required=['job_name', 'task_name'],
                         job_name=str,
                         task_name=str,
                         stream=str,
                         num_lines=int):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate task')

    call_args = {}
    for key in ['stream', 'num_lines']:
        if key in args:
            call_args[key] = args[key]
    return task.head(**call_args)


@bp_api.route('/api/tail', methods=['GET'])
@api_call
async def tail_task(request):
    args = dict(request.args)
    if not validate_dict(args,
                         required=['job_name', 'task_name'],
                         job_name=str,
                         task_name=str,
                         stream=str,
                         num_lines=int):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate task')

    call_args = {}
    for key in ['stream', 'num_lines']:
        if key in args:
            call_args[key] = args[key]
    return task.tail(**call_args)


#
@bp_api.route('/api/add_job', methods=['POST'])
@api_call
async def add_job(request):
    args = dict(request.form)

    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate args')

    app = request.app.config['dagobah']
    app.add_job(args['job_name'])


@bp_api.route('/api/delete_job', methods=['POST'])
@api_call
async def delete_job(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate args')

    dagobah.delete_job(args['job_name'])


@bp_api.route('/api/start_job', methods=['POST'])
@api_call
async def start_job(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    job.start()


@bp_api.route('/api/retry_job', methods=['POST'])
@api_call
async def retry_job(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    job.retry()


@bp_api.route('/api/add_task_to_job', methods=['POST'])
@api_call
async def add_task_to_job(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name', 'task_command', 'task_name'],
                         job_name=str,
                         task_command=str,
                         task_name=str,
                         task_target=str):
        raise ValueError('not validate args')

    dagobah.add_task_to_job(args['job_name'],
                            args['task_command'],
                            args['task_name'],
                            hostname=args.get("task_target", None))


@bp_api.route('/api/delete_task', methods=['POST'])
@api_call
async def delete_task(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name', 'task_name'],
                         job_name=str,
                         task_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    job.delete_task(args['task_name'])


@bp_api.route('/api/add_dependency', methods=['POST'])
@api_call
async def add_dependency(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name',
                                   'from_task_name',
                                   'to_task_name'],
                         job_name=str,
                         from_task_name=str,
                         to_task_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    job.add_dependency(args['from_task_name'], args['to_task_name'])


#
@bp_api.route('/api/delete_dependency', methods=['POST'])
@api_call
async def delete_dependency(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name',
                                   'from_task_name',
                                   'to_task_name'],
                         job_name=str,
                         from_task_name=str,
                         to_task_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    job.delete_dependency(args['from_task_name'], args['to_task_name'])


@bp_api.route('/api/schedule_job', methods=['POST'])
@api_call
async def schedule_job(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate args')

    if not args.get('cron_schedule', None):
        args['cron_schedule'] = None

    job = dagobah.get_job(args['job_name'])
    cron_schedule = args.get('cron_schedule', None)
    if not cron_schedule:
        cron_schedule = None
    if isinstance(cron_schedule, list) and len(cron_schedule) > 0:
        cron_schedule = cron_schedule[0]

    job.schedule(cron_schedule)


#
#
@bp_api.route('/api/stop_scheduler', methods=['POST'])
@api_call
async def stop_scheduler(request):
    dagobah.scheduler.stop()


#
#
@bp_api.route('/api/restart_scheduler', methods=['POST'])
@api_call
async def restart_scheduler(request):
    dagobah.scheduler.restart()


@bp_api.route('/api/terminate_all_tasks', methods=['POST'])
@api_call
async def terminate_all_tasks(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    job.terminate_all()


@bp_api.route('/api/kill_all_tasks', methods=['POST'])
@api_call
async def kill_all_tasks(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    job.kill_all()


@bp_api.route('/api/terminate_task', methods=['POST'])
@api_call
def terminate_task(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name', 'task_name'],
                         job_name=str,
                         task_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate tasks')
    task.terminate()


@bp_api.route('/api/kill_task', methods=['POST'])
@api_call
def kill_task(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name', 'task_name'],
                         job_name=str,
                         task_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate tasks')
    task.kill()


@bp_api.route('/api/edit_job', methods=['POST'])
@api_call
async def edit_job(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str,
                         name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    del args['job_name']
    job.edit(**args)
    return 'success'


@bp_api.route('/api/update_job_notes', methods=['POST'])
@api_call
async def update_job_notes(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name', 'notes'],
                         job_name=str,
                         notes=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    job.update_job_notes(args['notes'])


@bp_api.route('/api/edit_task', methods=['POST'])
@api_call
async def edit_task(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name', 'task_name'],
                         job_name=str,
                         task_name=str,
                         name=str,
                         command=str,
                         soft_timeout=int,
                         hard_timeout=int,
                         hostname=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate task')

    # validate host
    if 'hostname' in args and args.get('hostname') not in dagobah.get_hosts():
        # Check for empty host, if so then task is no longer remote
        if not args.get('hostname'):
            args['hostname'] = None
        else:
            raise ValueError('not validate host')

    del args['job_name']
    del args['task_name']
    job.edit_task(task.name, **args)


@bp_api.route('/api/set_soft_timeout', methods=['POST'])
@api_call
async def set_soft_timeout(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name', 'task_name', 'soft_timeout'],
                         job_name=str,
                         task_name=str,
                         soft_timeout=int):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate task')

    task.set_soft_timeout(args['soft_timeout'])


@bp_api.route('/api/set_hard_timeout', methods=['POST'])
@api_call
async def set_hard_timeout(request):
    args = dict(request.form)
    if not validate_dict(args,
                         required=['job_name', 'task_name', 'hard_timeout'],
                         job_name=str,
                         task_name=str,
                         hard_timeout=int):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])
    task = job.tasks.get(args['task_name'], None)
    if not task:
        raise ValueError('not validate task')

    task.set_hard_timeout(args['hard_timeout'])


@bp_api.route('/api/export_job', methods=['GET'])
async def export_job(request):
    args = dict(request.args)
    if not validate_dict(args,
                         required=['job_name'],
                         job_name=str):
        raise ValueError('not validate args')

    job = dagobah.get_job(args['job_name'])

    to_send = StringIO()
    to_send.write(json.dumps(job._serialize(strict_json=True)))
    to_send.write('\n')
    to_send.seek(0)

    return response.file(to_send,
                         attachment_filename='%s.json' % job.name,
                         as_attachment=True)


@bp_api.route('/api/import_job', methods=['POST'])
@api_call
def import_job(request):
    file = request.files['file']
    if (file and allowed_file(file.filename, ['json'])):
        dagobah.add_job_from_json(file.read(), destructive=True)


@bp_api.route('/api/hosts', methods=['GET'])
@api_call
async def get_hosts():
    return dagobah.get_hosts()
