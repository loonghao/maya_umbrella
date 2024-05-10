# encoding: utf-8
import sys
import os
import time

import maya_umbrella_rs

ROOT = sys.argv[1] if sys.argv >= 2 else os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

files = list(map(lambda x: os.path.join(ROOT, x), os.listdir(ROOT)))
signs = ['import vaccine', 'cmds.evalDeferred.*leukocyte.+', 'python(.*);.+exec.+(pyCode).+;']
print('Files Count: {}'.format(len(files)))

start_time = time.time()
maya_umbrella_rs.check_virus_from_files(files, signs)
end_time = time.time()
print('{}s'.format(round(end_time - start_time, 2)))
