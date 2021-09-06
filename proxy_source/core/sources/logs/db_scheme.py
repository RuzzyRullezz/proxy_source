from proxy_source.db.base import Base
from proxy_source.vendors.logs.outgoing_request_log.models import OutgoingRequestBase


class TrackingOutgoingRequestBestProxies(OutgoingRequestBase, Base):  # type: ignore
    __tablename__ = 'tracking_outgoing_request_best_proxies'
