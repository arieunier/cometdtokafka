from kafka import KafkaProducer,KafkaConsumer, KafkaClient
from kafka.errors import KafkaError
#Consumer, KafkaError, Producer
import ujson 
import datetime
from libs import logs
import os 

LOGGER = logs.LOGGER

KAFKA_URL=  os.getenv('KAFKA_URL','')
KAFKA_CLIENT_CERT=  os.getenv('KAFKA_CLIENT_CERT','')
file = open('static/kafka_client_cert', "w")
data = file.write(KAFKA_CLIENT_CERT)
file.close()


KAFKA_CLIENT_CERT_KEY=  os.getenv('KAFKA_CLIENT_CERT_KEY','')
file = open('static/kafka_client_key', "w")
data = file.write(KAFKA_CLIENT_CERT_KEY)
file.close()


KAFKA_TRUSTED_CERT=  os.getenv('KAFKA_TRUSTED_CERT','')
file = open('static/kafka_ca', "w")
data = file.write(KAFKA_TRUSTED_CERT)
file.close()

KAFKA_PREFIX=  os.getenv('KAFKA_PREFIX')
KAFKA_TOPIC_READ= os.getenv('KAFKA_TOPIC_READ', "topicRead") 
KAFKA_TOPIC_WRITE= os.getenv('KAFKA_TOPIC_WRITE', "topicWrite") 
KAFKA_GROUP_ID=os.getenv('KAFKA_CONSUMERGRP', KAFKA_PREFIX + 'my-consumer-group')

LOGGER.debug("KAFKA_PREFIX="+KAFKA_PREFIX)
LOGGER.debug("KAFKA_GROUP_ID="+KAFKA_GROUP_ID)

"""
    All the variable names here match the heroku env variable names.
    Just pass the env values straight in and it will work.
"""
producer = None

def init():
    global producer

    producer = KafkaProducer(
            bootstrap_servers =KAFKA_URL.replace('kafka+ssl://','').split(','),
            security_protocol ='SSL',
            ssl_check_hostname=False,
            ssl_cafile ='static/kafka_ca',
            ssl_certfile ='static/kafka_client_cert',
            ssl_keyfile= 'static/kafka_client_key'
            )

def createTopic(topicName):
    from kafka import KafkaClient
    client = KafkaClient(bootstrap_servers =KAFKA_URL.replace('kafka+ssl://','').split(','),
            security_protocol ='SSL',
            ssl_check_hostname=False,
            ssl_cafile ='static/kafka_ca',
            ssl_certfile ='static/kafka_client_cert',
            ssl_keyfile= 'static/kafka_client_key')
    client.add_topic(topicName)
    #topic_list = []
    #topic_list.append(NewTopic(name="example_topic", num_partitions=1, replication_factor=1))
    #admin_client.create_topics(new_topics=topic_list, validate_only=False)


def sendToKafka(data, topic=None):
    global producer
    """
    The .send method will automatically prefix your topic with the KAFKA_PREFIX
    NOTE: If the message doesn't seem to be sending try `producer.flush()` to force send.
    """

    if topic==None:
        sndTopic=KAFKA_PREFIX +  KAFKA_TOPIC_WRITE
    else:
        sndTopic=KAFKA_PREFIX +  topic

    LOGGER.debug("about to send {} to topic {}".format(data, sndTopic))
    producer.send(sndTopic, ujson.dumps(data).encode("UTF-8"))
    producer.flush()
    #producer.flush()
    LOGGER.debug("done")



