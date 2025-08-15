# 代码生成时间: 2025-08-15 21:26:31
import os
import shutil
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from datetime import datetime

# 定义备份文件夹的名称
BACKUP_DIR_NAME = 'backups'

class BackupHandler(tornado.web.RequestHandler):
    """
    处理文件备份和同步的请求
    """
    def get(self):
        # 获取备份路径
        backup_path = os.path.join(os.getcwd(), BACKUP_DIR_NAME)
        # 获取当前时间作为备份的名称
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{now}'
        backup_dir = os.path.join(backup_path, backup_name)

        try:
            # 创建备份目录
            os.makedirs(backup_dir, exist_ok=True)
            # 遍历当前工作目录
            for root, dirs, files in os.walk(os.getcwd()):
                # 排除备份目录
                if root == backup_path:
                    continue
                # 同步文件到备份目录
                for file in files:
                    src_file_path = os.path.join(root, file)
                    dst_file_path = os.path.join(backup_dir, os.path.relpath(src_file_path, os.getcwd()))
                    os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
                    shutil.copy2(src_file_path, dst_file_path)
            self.write(f'Backup completed. Files backed up to {backup_dir}')
        except Exception as e:
            self.write(f'Error occurred: {e}')

    def write_error(self, status_code, **kwargs):
        """
        自定义错误处理
        """
        if status_code == 404:
            self.write('This resource does not exist')
        else:
            self.write('An unexpected error occurred')

def make_app():
    """
    创建Tornado应用
    """
    return tornado.web.Application([
        (r"/backup", BackupHandler),
    ])

if __name__ == "__main__":
    # 定义命令行参数
    define("port", default=8888, help="run on the given port", type=int)
    options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print(f"Server is running on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()