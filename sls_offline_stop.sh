echo 'stop -> serverless offline'
kill `cat .offline.pid`
rm .offline.pid
echo 'serverless offline stopped'

