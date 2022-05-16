from celery import Celery
from celery.result import AsyncResult
from utils.ffmpeg_helper import convert_to_mp4

backend_url = 'redis://redis:6379/0'
broker_url = 'pyamqp://guest@rabbit//'

celery = Celery('workers',
                backend=backend_url,
                broker=broker_url)
celery.conf.accept_content = ['json', 'msgpack']
celery.conf.result_serializer = 'msgpack'


def get_job(job_id):
    return AsyncResult(job_id, app=celery)


@celery.task()
def task_convert_to_mp4(filename, file_id):
    convert_to_mp4(filename, file_id)
