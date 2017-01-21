#usr/bin/bash
rq resume
rq worker 1 &
rq worker 2 &
rq worker 3 &
rq worker 4 &
rq worker 5 &
rq worker 6 &
rq worker 7 &
rq worker 8 &

twistd web --wsgi app.app -p 80