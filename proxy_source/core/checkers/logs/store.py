from proxy_source.db.sessions import create_transaction_session
from proxy_source.vendors.logs.outgoing_request_log.context import LogContextOutgoing

from . import db_scheme


async def create_outgoing_request_log(log_context: LogContextOutgoing):
    async with create_transaction_session() as db_session:
        log_record = db_scheme.TrackingOutgoingRequestIpService.from_log_context(log_context)
        db_session.add(log_record)
