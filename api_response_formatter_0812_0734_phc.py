# 代码生成时间: 2025-08-12 07:34:51
import tornado.ioloop
import tornado.web
import json


class ApiResponseFormatter:
    """
    A utility class to format API responses with consistent structure.
    """

    def __init__(self):
        pass

    def format_response(self, data, status_code=200):
        """
        Formats the API response with a consistent structure.
        
        Args:
            data (dict): The data to be included in the response body.
            status_code (int): The HTTP status code of the response. Defaults to 200.
        
        Returns:
            dict: A formatted API response.
        """
        return {
            "status": "success" if status_code < 400 else "error",
            "code": status_code,
            "data": data,
        }

    def format_error(self, error_message, status_code=400):
        """
        Formats an API error response with a consistent structure.
        
        Args:
            error_message (str): The error message to be included in the response body.
            status_code (int): The HTTP status code of the response. Defaults to 400.
        
        Returns:
            dict: A formatted API error response.
        """
        return {
            "status": "error",
            "code": status_code,
            "error": error_message,
        }


class MainHandler(tornado.web.RequestHandler):
    """
    The main request handler for the API.
    """
    def get(self):
        """
        Handles GET requests and returns a formatted response.
        """
        try:
            data = {"message": "Hello, world!"}
            response = ApiResponseFormatter().format_response(data)
            self.write(json.dumps(response))
        except Exception as e:
            error_response = ApiResponseFormatter().format_error(str(e))
            self.set_status(500)
            self.write(json.dumps(error_response))


def make_app():
    """
    Create the Tornado application.
    """
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()