# 代码生成时间: 2025-09-23 01:18:27
import os
import zipfile
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

# DecompressionHandler handles the decompression of uploaded zip files
class DecompressionHandler(RequestHandler):
    def post(self):
        # Get the uploaded file from the request
        uploaded_file = self.request.files['file'][0]

        # Get the file name and path
        file_name = uploaded_file['filename']
        file_path = os.path.join('uploads', file_name)

        try:
            # Save the uploaded file to the server
            with open(file_path, 'wb') as f:
                f.write(uploaded_file['body'])

            # Decompress the file
            self.decompress(file_path)

            # Remove the uploaded file
            os.remove(file_path)

            # Respond to the client
            self.write({'status': 'success', 'message': 'File decompressed successfully'})
        except Exception as e:
            # Handle any exceptions that occur during the process
            self.write({'status': 'error', 'message': str(e)})

    def decompress(self, file_path):
        # Ensure the file is a zip file
        if not file_path.endswith('.zip'):
            raise ValueError('The provided file is not a zip file')

        # Extract the contents of the zip file to the current directory
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall()

# Create the Tornado application
def make_app():
    return Application([
        (r'/decompress', DecompressionHandler),
    ])

if __name__ == '__main__':
    # Create the application and run it on port 8888
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

# The following are example HTTP requests and responses
# Note: These are not part of the actual code and should be executed separately
# curl -X POST -F 'file=@path_to_zip_file.zip' http://localhost:8888/decompress
# Response: {"status": "success", "message": "File decompressed successfully"}
