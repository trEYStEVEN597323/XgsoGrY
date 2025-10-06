# 代码生成时间: 2025-10-07 02:31:29
import tornado.ioloop
import tornado.web
import tornado.options
import json

# Define the Content class to store content data
class Content:
    def __init__(self, content_id, title, author, content):
        self.content_id = content_id
        self.title = title
        self.author = author
        self.content = content

# Define the ContentManager class to handle content operations
class ContentManager:
    def __init__(self):
        self.contents = {}

    def add_content(self, content):
        self.contents[content.content_id] = content

    def get_content(self, content_id):
        return self.contents.get(content_id)

    def update_content(self, content_id, title, author, content):
        if content_id in self.contents:
            self.contents[content_id].title = title
            self.contents[content_id].author = author
            self.contents[content_id].content = content
            return True
        return False

    def delete_content(self, content_id):
        if content_id in self.contents:
            del self.contents[content_id]
            return True
        return False

# Define the Tornado RequestHandler for managing content
class ContentHandler(tornado.web.RequestHandler):
    def initialize(self, content_manager):
        self.content_manager = content_manager

    def get(self, content_id=None):
        if content_id:
            content = self.content_manager.get_content(content_id)
            if content:
                self.write(json.dumps({'status': 'success', 'content': vars(content)}))
            else:
                self.set_status(404)
                self.write(json.dumps({'status': 'error', 'message': 'Content not found'}))
        else:
            self.set_status(400)
            self.write(json.dumps({'status': 'error', 'message': 'Content ID is required'}))

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        content = Content(data['content_id'], data['title'], data['author'], data['content'])
        self.content_manager.add_content(content)
        self.write(json.dumps({'status': 'success', 'message': 'Content added'}))

    def put(self, content_id):
        data = tornado.escape.json_decode(self.request.body)
        if self.content_manager.update_content(content_id, data['title'], data['author'], data['content']):
            self.write(json.dumps({'status': 'success', 'message': 'Content updated'}))
        else:
            self.set_status(404)
            self.write(json.dumps({'status': 'error', 'message': 'Content not found'}))

    def delete(self, content_id):
        if self.content_manager.delete_content(content_id):
            self.write(json.dumps({'status': 'success', 'message': 'Content deleted'}))
        else:
            self.set_status(404)
            self.write(json.dumps({'status': 'error', 'message': 'Content not found'}))

# Define the Tornado Application
class ContentManagementApplication(tornado.web.Application):
    def __init__(self):
        self.content_manager = ContentManager()
        handlers = [
            (r"/(\d+)", ContentHandler, dict(content_manager=self.content_manager)),
            (r"/", ContentHandler, dict(content_manager=self.content_manager)),
        ]
        tornado.web.Application.__init__(self, handlers)

# Define the main function to run the Tornado application
def main():
    tornado.options.parse_command_line()
    app = ContentManagementApplication()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
