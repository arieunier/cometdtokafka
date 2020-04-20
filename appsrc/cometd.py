import asyncio
import os 
from aiosfstream import SalesforceStreamingClient
from libs import logs
import kafka_utils


LOGGER = logs.LOGGER


CONSUMER_KEY=os.environ.get('CONSUMER_KEY','')
CONSUMER_SECRET=os.environ.get('CONSUMER_SECRET','')
USERNAME=os.environ.get('USERNAME','')
PASSWORD=os.environ.get('PASSWORD','')
TOPICS=os.environ.get('TOPICS','')

async def stream_events():
    # connect to Streaming API
    async with SalesforceStreamingClient(

            sandbox=False,
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            username=USERNAME,
            password=PASSWORD) as client:

        kafka_topics=[]
        for topic in TOPICS.split(";"):
        
            LOGGER.debug("Subscribing to {}".format(topic))
            kafka_topics.append(topic[1:len(topic)].replace('/','_'))
            await client.subscribe(topic)
        #
        LOGGER.warn("Before receiving any messages, MAKE SURE TO CREATE THE FOLLOWING TOPICS ON KAFKA")
        LOGGER.warn(kafka_topics)

        # listen for incoming messages
        async for message in client:
            LOGGER.debug("Message Received => {} ".format(message))
            topic = message["channel"]
            data = message["data"]
            #print(f"{topic}: {data}")
            # topic start with a / ,  let's remove that one
            newTopicName = topic[1:len(topic)].replace('/','_')
            LOGGER.debug("New Topic Name -> {}".format(newTopicName))
            kafka_utils.sendToKafka(data, topic=newTopicName)

if __name__ == "__main__":
    kafka_utils.init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream_events())