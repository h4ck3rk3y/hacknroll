#usr/bin/bash

killall -9 'twistd'
killall -9 'python'
rq empty
rq suspend
