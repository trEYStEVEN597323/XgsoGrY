# 代码生成时间: 2025-08-02 18:11:38
import os
import tornado.ioloop
import tornado.web
from PIL import Image, ImageOps
from io import BytesIO

# 定义一个异常类，用于处理图片尺寸调整过程中的错误
class ResizeError(Exception):
    pass

class ImageResizeHandler(tornado.web.RequestHandler):
    """
    处理图片尺寸调整请求的Handler
    """
    def post(self):
        # 获取上传的图片文件
        file = self.request.files['file'][0]
        target_size = self.get_argument('size', None)

        try:
            # 读取图片文件
            image = Image.open(BytesIO(file.body))
            resized_image = self.resize_image(image, target_size)
            self.write(resized_image)
        except ResizeError as e:
            self.set_status(400)
            self.write({'error': str(e)})
        except Exception as e:
            self.set_status(500)
            self.write({'error': 'Internal Server Error'})

    def resize_image(self, image, size):
        """
        调整图片尺寸
        :param image: PIL Image对象
        :param size: 目标尺寸，格式为'widthxheight'
        :return: 调整尺寸后的图片的二进制数据
        """
        try:
            width, height = map(int, size.split('x'))
            if width <= 0 or height <= 0:
                raise ResizeError('Invalid size')

            # 调整图片尺寸
            resized_image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
            buffered = BytesIO()
            resized_image.save(buffered, format="JPEG")
            return buffered.getvalue()
        except ValueError as e:
            raise ResizeError('Invalid size format')

    def set_default_headers(self):
        """
        设置默认响应头
        """
        self.set_header("Access-Control-Allow-Origin