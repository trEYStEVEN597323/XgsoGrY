# 代码生成时间: 2025-08-16 07:02:26
import os
import json
from tornado import web, ioloop, options
from tornado.web import RequestHandler, Application, asynchronous
from tornado.options import define, options
from docx import Document

# Define the command line options
define("port", default=8888, help="run on the given port", type=int)

class DocumentConverterHandler(RequestHandler):
    """ Handles HTTP requests to convert documents. """

    @asynchronous
    def post(self):
        """ Converts a document from one format to another. """
        try:
            # Get the document file from the request
            file_info = self.request.files['document'][0]
            file_data = file_info.body
            file_name = file_info['filename']

            # Convert file name to .txt format
            doc = Document(file_data)
            doc.save(file_name.split('.')[0] + '.txt')

            # Prepare the response
            response = {
                "message": "Document converted successfully",
                "file_name": file_name.split('.')[0] + '.txt'
            }

            # Send the response as JSON
            self.write(json.dumps(response))
            self.finish()
        except Exception as e:
            # Handle any errors that occur during the conversion process
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))
            self.finish()

def make_app():
    "