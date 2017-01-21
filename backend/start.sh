#usr/bin/bash
rq resume
rq worker r1 &
rq worker r2 &
rq worker r3 &
rq worker r4 &
rq worker r5 &
rq worker r6 &
rq worker r7 &
rq worker r8 &

twistd web --wsgi app.app -p 8080