import asyncio
from aiokafka import AIOKafkaConsumer


class Consumer(object):
    def __init__(self, topic: str):
        self.topic = topic
        self.consumer: AIOKafkaConsumer = None

    async def __aenter__(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers="localhost:9094",
            group_id="test-group",
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
        await self.consumer.start()
        return self.consumer

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.consumer.stop()
        if exc_type:
            raise exc_type(exc_val)


async def main():
    topic = "kafka-python-test"
    async with Consumer(topic) as consumer:
        while True:
            batch = await consumer.getmany(max_records=7, timeout_ms=1000)
            for tp, messages in batch.items():
                for message in messages:
                    print(message)


if __name__ == "__main__":
    asyncio.run(main())
