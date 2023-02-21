""" 
    A class that can be instantiated to interact with Kafka.
"""
from typing import List
from json import dumps
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic


class KafkaService:
    def __init__(self, servers: List[str], client_name: str) -> None:
        self.producer = None
        self.consumers = list()
        self.servers = servers
        self.client = KafkaAdminClient(
            bootstrap_servers=servers, 
            client_id=client_name
        )
    
    def add_new_topic(self, topic: str) -> bool:
        try:
            topic_list = []
            topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
            self.client.create_topics(new_topics=topic_list, validate_only=False)
            return True
        except:
            return False

    def _set_producer(self):
        self.producer = KafkaProducer(self.servers)

    async def produce_simple_message(self, topic: str, message: str) -> None:
        if self.producer is None:
            self._set_producer()
        bmsg = bytes(message)
        return await self.producer.send(topic, bmsg)
    
    async def produce_json_message(self, topic: str, message: dict) -> None:
        # TODO: serialize message
        jmsg = dumps(message)
        return await self.producer.send(topic, jmsg)