import asyncio
from typing import List, Callable, Awaitable, Union, cast, Generator

from ..proxies import Proxy
from .service import check_proxy, Report


StopUnit = None
InQueueElementType = Union[Proxy, StopUnit]
OutQueueElementType = Union[Proxy, Exception, StopUnit]
MAX_WORKERS = 150


async def proxy_check_worker(
        in_queue: asyncio.Queue[InQueueElementType],
        out_queue: asyncio.Queue[OutQueueElementType],
):
    while True:
        element: InQueueElementType = await in_queue.get()
        try:
            if element is StopUnit:
                break
            proxy = element
            report = await check_proxy(proxy)
            await out_queue.put(cast(OutQueueElementType, report))
        finally:
            in_queue.task_done()


async def report_read_worker(
        queue: asyncio.Queue[OutQueueElementType],
) -> Generator[Report, None, None]:
    while True:
        element: OutQueueElementType = await queue.get()
        if element is StopUnit:
            queue.task_done()
            break
        if isinstance(element, Exception):
            exc = element
            raise exc
        report = element
        yield report


class Master:
    in_queue: asyncio.Queue
    out_queue: asyncio.Queue
    workers: List[asyncio.Task]
    finish_notify_task: asyncio.Task

    @staticmethod
    def create_workers(
            in_queue: asyncio.Queue,
            out_queue: asyncio.Queue,
            max_workers: int,
            worker: Callable[[asyncio.Queue, asyncio.Queue], Awaitable[None]],
    ) -> List[asyncio.Task]:
        tasks: List[asyncio.Task] = []
        for i in range(max_workers):
            task = asyncio.create_task(worker(in_queue, out_queue))
            tasks.append(task)
        return tasks

    @staticmethod
    async def finish_notify(
            workers: List[asyncio.Task],
            queue: asyncio.Queue[OutQueueElementType],
    ):
        try:
            await asyncio.gather(*workers)
            await queue.put(StopUnit)
        except Exception as exc:
            await queue.put(exc)
            raise

    def __init__(self, max_workers: int = MAX_WORKERS):
        self.in_queue = asyncio.Queue()
        self.out_queue = asyncio.Queue()
        self.workers = self.create_workers(self.in_queue, self.out_queue, max_workers, proxy_check_worker)
        self.finish_notify_task = asyncio.create_task(self.finish_notify(self.workers, self.out_queue))

    async def run(self, proxies_list: List[Proxy]) -> Generator[Report, None, None]:
        for proxy in proxies_list:
            await self.in_queue.put(proxy)
        for _ in self.workers:
            await self.in_queue.put(StopUnit)
        # yield from ... doesn't work in coroutines
        async for report in report_read_worker(self.out_queue):
            yield report


async def get_proxy_reports_gen(
        proxies_list: List[Proxy],
        parallels_cnt: int = MAX_WORKERS,
) -> Generator[Report, None, None]:
    # yield from ... doesn't work in coroutines
    async for report in Master(max_workers=parallels_cnt).run(proxies_list):
        yield report
