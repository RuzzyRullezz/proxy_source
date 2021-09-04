from proxy_source.db.sessions import SessionLocal
from proxy_source.utils.database import create_in_storage
from proxy_source.vendors.rest_api.outgoing_request_log.context import LogContextOutgoing

from . import db_scheme


def create_outgoing_request_log(log_context: LogContextOutgoing):
    with SessionLocal() as db_session, db_session.begin():
        log_record = db_scheme.TrackingOutgoingRequestBestProxies.from_log_context(log_context)
        create_in_storage(db_session, log_record)
