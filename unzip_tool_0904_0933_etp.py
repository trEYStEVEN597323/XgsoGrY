# 代码生成时间: 2025-09-04 09:33:25
import zipfile
import os
import tornado.ioloop
import tornado.web
import tornado.options
import json

"""
Unzip Tool Application using Tornado Framework
This application provides a simple REST API endpoint to decompress zip files.
"""

# Define settings for Tornado application
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

class UnzipHandler(tornado.web.RequestHandler):
    """
    Request handler for unzipping files.
    """
    def post(self):
        # Get the zip file from the request
        zip_file = self.get_argument('file')
        
        try:
            # Check if the file is a valid zip file
            if not zipfile.is_zipfile(zip_file):
                self.set_status(400)
                self.write(json.dumps({'error': 'The provided file is not a valid zip file.'}))
                return

            # Unzip the file to a designated directory
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall('unzipped')

            # Respond with success message and unzipped file details
            self.write(json.dumps({'message': 'File unzipped successfully.'}))
        except Exception as e:
            # Handle any exceptions that occur during the unzip process
            self.set_status(500)
            self.write(json.dumps({'error': 'An error occurred while unzipping the file.', 'details': str(e)}))

# Define the Tornado application
def make_app():
    return tornado.web.Application([
        (r"/unzip", UnzipHandler),
    ], **settings)

# Run the Tornado application if this script is executed directly
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()