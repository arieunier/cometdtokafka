APPNAME=$1
export PYTHONPATH=.:./libs/:./appsrc/:./pyutils
# logs
export LOG_LEVEL=DEBUG

export KAFKA_CLIENT_CERT=`heroku config:get KAFKA_CLIENT_CERT  --app $APPNAME`
export KAFKA_CLIENT_CERT_KEY=`heroku config:get KAFKA_CLIENT_CERT_KEY  --app $APPNAME`
export KAFKA_PREFIX=`heroku config:get KAFKA_PREFIX  --app $APPNAME`
export KAFKA_TRUSTED_CERT=`heroku config:get KAFKA_TRUSTED_CERT  --app $APPNAME`
export KAFKA_URL=`heroku config:get KAFKA_URL  --app $APPNAME`

#heroku kafka:consumer-groups:create my-consumer-group --app connect-events-arieunier
#heroku kafka:topics:create topicRead --app connect-events-arieunier
#heroku kafka:topics:create topicWrite --app connect-events-arieunier
