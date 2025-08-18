# 代码生成时间: 2025-08-18 21:11:42
import os
import xlsxwriter
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options
from datetime import datetime

# 定义选项参数
define('port', default=8888, help='Port to listen on', type=int)

class ExcelGeneratorHandler(RequestHandler):
    """
    用于生成Excel文件的处理程序。
    """
    def get(self):
        # 获取请求的查询参数
        title = self.get_query_argument('title', 'Default Title')
        sheet_name = self.get_query_argument('sheet_name', 'Sheet1')
        
        # 创建Excel文件
        filename = f'{title}_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet(sheet_name)
        
        try:
            # 添加标题行
            worksheet.write('A1', 'Column 1')
            worksheet.write('B1', 'Column 2')
            
            # 添加一些示例数据
            worksheet.write('A2', 'Data 1')
            worksheet.write('B2', 'Data 2')
            
            # 关闭Workbook，保存Excel文件
            workbook.close()
            
            # 设置文件下载响应头
            self.set_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            self.set_header('Content-Disposition', f'attachment; filename={filename}')
            self.write(open(filename, 'rb').read())
        except Exception as e:
            # 错误处理
            self.write(f'An error occurred: {e}')
        finally:
            # 确保文件被删除
            if os.path.exists(filename):
                os.remove(filename)

def make_app():
    """
    创建并返回Tornado应用。
    """
    return Application([
        (r'/generate_excel', ExcelGeneratorHandler),
    ])

if __name__ == '__main__':
    # 启动Tornado应用程序
    app = make_app()
    app.listen(options.port)
    print(f'Server is running at http://localhost:{options.port}')
    IOLoop.current().start()