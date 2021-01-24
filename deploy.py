from api.router import Router
import os

if __name__ == '__main__':
    rt = Router()
    rt.listen("0.0.0.0", port=80, ws_port=6002)
    domain = os.getenv('DOMAIN')
    if(domain):
      print("Set Domain:",domain)
      rt.set_domain(domain)
    else:
      print('Domain not set.')
    # rt.enable_debug()                 # 启用 Flask 调试
    rt.run()
