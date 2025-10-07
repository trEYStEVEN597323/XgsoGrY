# 代码生成时间: 2025-10-08 01:37:27
import tornado.ioloop
import tornado.web
from datetime import datetime

# 定义一个简单的学习进度模型
class LearningProgress:
    def __init__(self):
# 改进用户体验
        self.courses = {}  # 存储课程进度，键为课程名，值为进度信息

    def add_course(self, course_name):
        """添加新的课程到学习进度跟踪中"""
        if course_name not in self.courses:
            self.courses[course_name] = {
                'started_at': datetime.now(),
                'completed_at': None,
                'status': 'In Progress'
# 添加错误处理
            }
        else:
            raise ValueError('Course already exists in progress tracking.')

    def update_progress(self, course_name, new_status):
# 增强安全性
        """更新课程的学习进度状态"""
# TODO: 优化性能
        if course_name in self.courses:
            self.courses[course_name]['status'] = new_status
# 添加错误处理
            if new_status == 'Completed':
                self.courses[course_name]['completed_at'] = datetime.now()
        else:
            raise ValueError('Course not found in progress tracking.')
# TODO: 优化性能

    def get_progress(self, course_name):
        """获取指定课程的学习进度信息"""
        if course_name in self.courses:
            return self.courses[course_name]
        else:
            raise ValueError('Course not found in progress tracking.')


# 创建Tornado应用
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to the Learning Progress Tracker.")
# 优化算法效率

class ProgressHandler(tornado.web.RequestHandler):
    def initialize(self, progress_tracker):
        self.progress_tracker = progress_tracker

    def get(self, course_name):
        try:
            progress = self.progress_tracker.get_progress(course_name)
# NOTE: 重要实现细节
            self.write(progress)
        except ValueError as e:
            self.write(str(e))
            self.set_status(404)

    def post(self):
        data = self.get_argument('course_name')
# NOTE: 重要实现细节
        try:
            self.progress_tracker.add_course(data)
            self.write({'status': 'success', 'message': 'Course added.'})
        except ValueError as e:
            self.write({'status': 'error', 'message': str(e)})
            self.set_status(400)

    def put(self):
        data = self.get_body_argument('data')
        try:
            course_name, new_status = data['course_name'], data['status']
            self.progress_tracker.update_progress(course_name, new_status)
            self.write({'status': 'success', 'message': 'Progress updated.'})
        except (ValueError, KeyError) as e:
            self.write({'status': 'error', 'message': str(e)})
            self.set_status(400)

# 设置Tornado路由
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/progress/(\w+)", ProgressHandler, dict(progress_tracker=LearningProgress())),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Learning Progress Tracker server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()