from kafka import KafkaProducer as kp, KafkaConsumer as kc
BOOTSTRAP_SERVERS = ['broker:29092']
producer = kp(bootstrap_servers=BOOTSTRAP_SERVERS)

consumer = kc(group_id=None, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset='earliest')
consumer.subscribe(topics=['nutopic'])

def add(msg: str):
    msg = bytes(msg)
    producer.send('nutopic', msg)

def pull():
    m = consumer.poll()
    if m:
        m = list(m.values())[0]
        for msg in m:
            decoded = msg.value.decode('utf-8')
            print(decoded)

