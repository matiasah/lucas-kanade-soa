
from __future__ import print_function

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import logging
import os
import re
import sys
import time
import pprint
from datetime import datetime

import mimetypes
from flask import render_template, Response
from flask import send_file
from flask import request, Blueprint

LOG = logging.getLogger(__name__)

mod = Blueprint('procesado', __name__)

MB = 1 << 20
BUFF_SIZE = 10 * MB
VIDEO_PATH = '/video'
videoPath = ''

@mod.route("/procesado/<video_name>", methods=['GET'])
def procesado(video_name):

    videoPath = 'output/' + video_name
    
    LOG.info('Rendering home page')
    response = render_template(
        'index.html',        
        video=VIDEO_PATH,
    )
    return response

@mod.route("/video/<video>", methods=['GET'])
def video(video):
    path = 'output/' + video

    start, end = get_range(request)
    return partial_response(path, start, end)

def partial_response(path, start, end=None):
    LOG.info('Requested: %s, %s', start, end)
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    LOG.info('Response: %s', response)
    LOG.info('Response: %s', response.headers)
    return response

def get_range(request):
    range = request.headers.get('Range')
    LOG.info('Requested: %s', range)
    try:
        m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
        if m:
            start = m.group('start')
            end = m.group('end')
            start = int(start)
            if end is not None:
                end = int(end)
            return start, end
        else:
            return 0, None    
    except (Exception):
        return 0, None