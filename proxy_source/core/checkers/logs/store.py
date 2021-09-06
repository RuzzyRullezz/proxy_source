from proxy_source.db.sessions import get_async_db_session
from proxy_source.vendors.rest_api.outgoing_request_log.context import LogContextOutgoing

from . import db_scheme


async def create_outgoing_request_log(log_context: LogContextOutgoing):
    async with get_async_db_session() as db_session, db_session.begin():
        log_record = db_scheme.TrackingOutgoingRequestIpService.from_log_context(log_context)
        db_session.add(log_record)
