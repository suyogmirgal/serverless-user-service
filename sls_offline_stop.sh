
#stop local SQS
echo 'stop -> local SQS'
container_id=$(docker ps | grep alpine-sqs | awk '{ print $1 }')
echo "SQS container id is ${container_id}"
docker stop ${container_id}
docker rm ${container_id}
echo 'local SQS stopped'

echo ''
echo ''

kill $(lsof -ti:8000)

echo 'stop -> serverless offline'
kill `cat .offline.pid`
rm .offline.pid
echo 'serverless offline stopped'

