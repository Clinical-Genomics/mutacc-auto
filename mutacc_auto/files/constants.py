import datetime

def get_timestamp():

    return str(datetime.datetime.now()).replace(' ','_').replace('.','_')

SHEBANG = '#!/bin/bash'

HEADER_PREFIX = '#SBATCH'

JOBNAME = 'mutacc_' + get_timestamp()
ACCOUNT = 'prod001'
NODES = '1'
TIME = '4:00:00'
PRIORITY = 'low'
MAIL_FAIL = 'FAIL'
MAIL_END = 'END'

#SOME DEFAULT SBATCH OPTIONS
# (OPTION, VALUE)
HEADER_OPTIONS = (
    ('A', ACCOUNT),
    ('n', NODES),
    ('t', TIME),
    ('J', JOBNAME),
    ('qos', PRIORITY),
    ('mail-type', MAIL_FAIL),
    ('mail-type', MAIL_END)
)

SOURCE_ACTIVATE = "source activate"
CONDA_ACTIVATE = "conda activate"

STDERR_SUFFIX = "err"
STDOUT_SUFFIX = "out"

NEWLINE = "\n"
