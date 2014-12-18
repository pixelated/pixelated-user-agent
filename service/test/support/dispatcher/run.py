from test.support.dispatcher.proxy import Proxy

if __name__ in ('main', '__main__'):
    proxy = Proxy(proxy_port='8888', app_port='3333')
    try:
        proxy.serve_forever()
    except Exception, e:
        proxy.shutdown()