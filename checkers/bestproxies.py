from proxy_source.core.sources import BestProxiesSource

bestproxies_source = BestProxiesSource()
proxies_list = bestproxies_source.get_proxies()
print(proxies_list)
