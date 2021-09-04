from proxy_source.core.sources import BestProxiesSource
from proxy_source.core.checkers import service as checkers_service

bestproxies_source = BestProxiesSource()
proxies_list = bestproxies_source.get_proxies()
for proxy in proxies_list:
    print(checkers_service.check_proxy(proxy))
