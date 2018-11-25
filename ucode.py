import img2cloud
import os
from utils import *


log_dump(LOG_FILENAME,'ucode started!')
print('write ucode pid')
writefile('ucode.pid', str(os.getpid()))   
img2cloud.main_loop('ucode.txt')
