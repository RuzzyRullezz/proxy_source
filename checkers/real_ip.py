from proxy_source.core.checkers import service as checkers_service

print(checkers_service.network.get_real_ip(use_cache=True))
