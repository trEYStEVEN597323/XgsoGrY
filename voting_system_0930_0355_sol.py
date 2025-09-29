# 代码生成时间: 2025-09-30 03:55:21
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado.web import RequestHandler
import json

# 定义全局投票选项
VOTES = {}

class MainHandler(RequestHandler):
    # GET请求处理，返回当前投票结果
    def get(self):
        self.write(json.dumps(VOTES))

    # POST请求处理，提交新的投票
    def post(self):
        try:
            # 解析请求体中的JSON数据
            vote_data = json.loads(self.request.body)
            # 获取投票选项和票数
            option = vote_data.get('option')
            count = vote_data.get('count')
            if option and count:
                # 更新全局投票选项
                if option in VOTES:
                    VOTES[option] += count
                else:
                    VOTES[option] = count
                self.write(json.dumps({'status': 'success'}))
            else:
                raise ValueError('Invalid vote data')
        except ValueError as e:
            self.write(json.dumps({'status': 'error', 'message': str(e)}))
        except json.JSONDecodeError:
            self.write(json.dumps({'status': 'error', 'message': 'Invalid JSON'}))

class VoteApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        super(VoteApplication, self).__init__(handlers)

if __name__ == '__main__':
    define('port', default=8888, help='run on the given port', type=int)
    define('debug', default=True, help='run in debug mode')
    options.parse_command_line()

    app = VoteApplication()
    app.listen(options.port)
    print(f'Server started on port {options.port}')
    tornado.ioloop.IOLoop.current().start()