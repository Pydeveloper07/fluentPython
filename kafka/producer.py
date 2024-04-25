import asyncio
import json
import uuid

from aiokafka import AIOKafkaProducer


class Producer(object):
    def __init__(self):
        self.producer: AIOKafkaProducer = None

    async def __aenter__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers="localhost:9094",
            max_request_size=10485760
        )
        await self.producer.start()
        return self.producer

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.producer.stop()
        if exc_type:
            raise exc_type(exc_val)


async def produce(topic, records):
    async with Producer() as producer:
        for record in records:
            record = json.dumps(record).encode()
            await producer.send(topic, record)


async def main():
    topic = "kafka-python-test"
    # with open("data.json", "rb") as f:
    #     data = json.load(f)
    data = uuid.uuid4().hex
    await produce(topic, [data])


if __name__ == "__main__":
    asyncio.run(main())

