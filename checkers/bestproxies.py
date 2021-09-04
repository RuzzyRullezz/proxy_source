from proxy_source.core.sources.base import BestProxiesSource

bestproxies_source = BestProxiesSource()
proxies_list = bestproxies_source.get_proxies()
print(proxies_list)
