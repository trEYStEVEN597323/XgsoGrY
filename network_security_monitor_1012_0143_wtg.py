# 代码生成时间: 2025-10-12 01:43:22
import json
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
import psutil
import socket

# 网络安全监控Handler
class SecurityMonitorHandler(RequestHandler):
    """
    处理网络安全监控请求
    """
    async def get(self):
        try:
            # 获取网络信息
            net_info = self.get_network_info()
            # 将网络信息以JSON格式返回
            self.write(json.dumps(net_info))
        except Exception as e:
            # 异常处理
            self.write(json.dumps({'error': str(e)}))

    def get_network_info(self):
        """
        获取网络信息
        """
        net_info = {}
        # 获取网络接口信息
        interfaces = psutil.net_if_stats()
        for interface, stats in interfaces.items():
            net_info[interface] = {
                'is_up': stats.isup,
                'speed': stats.speed,
                'duplex': stats.duplex,
                'mtu': stats.mtu,
                'promisc': stats.promisc,
                'flags': stats.flags
            }
        # 获取网络流量信息
        traffic_info = psutil.net_io_counters(pernic=True)
        for interface, stats in traffic_info.items():
            net_info[interface]['bytes_sent'] = stats.bytes_sent
            net_info[interface]['bytes_recv'] = stats.bytes_recv
            net_info[interface]['packets_sent'] = stats.packets_sent
            net_info[interface]['packets_recv'] = stats.packets_recv
            net_info[interface]['errin'] = stats.errin
            net_info[interface]['errout'] = stats.errout
            net_info[interface]['dropin'] = stats.dropin
            net_info[interface]['dropout'] = stats.dropout
        return net_info

# 定义Tornado应用
def make_app():
    return Application([
        (r"/monitor", SecurityMonitorHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Security Monitor is running on http://localhost:8888/monitor")
    IOLoop.current().start()