TMPFILE=.offline$$.log

echo 'start -> serverless offline offline'

serverless offline 2>1 > $TMPFILE &
PID=$!
echo $PID > .offline.pid

while ! grep "server ready" $TMPFILE
do
echo 'starting ...'
echo `cat 1`
sleep 1; done

echo 'serverless offline started'

rm $TMPFILE
rm 1