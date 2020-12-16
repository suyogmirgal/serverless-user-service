TMPFILE=.offline$$.log

#start local SQS
echo 'Start -> Local SQS'
docker run --name alpine-sqs -p 9324:9324 -p 9325:9325 -d roribio16/alpine-sqs:latest
sleep 5
echo 'local SQS started'


echo ''
echo ''

#start serverless offline
echo 'start -> serverless offline offline'

serverless offline start 2>1 > $TMPFILE &
PID=$!
echo $PID > .offline.pid

while ! grep "server ready" $TMPFILE
do
echo 'starting ...'
sleep 1; done

echo 'serverless offline started'

rm $TMPFILE
rm 1