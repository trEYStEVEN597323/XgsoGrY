# 代码生成时间: 2025-08-04 00:49:26
import psutil
import json
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application


# MemoryAnalysisHandler class handles memory usage analysis requests
class MemoryAnalysisHandler(RequestHandler):
    def get(self):
        try:
            # Get the current process memory info
            process_memory = psutil.Process().memory_info()
            
            # Prepare the response data in JSON format
            response_data = {
                "rss": process_memory.rss,  # Resident Set Size
                "vms": process_memory.vms,  # Virtual Memory Size
                "pfaults": process_memory.pagefaults,
                "pmajfaults": process_memory.maj_faults,
                "user_time": process_memory.user_time,
                "system_time": process_memory.system_time
            }
            
            # Set the content type to JSON and write the response
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(response_data))
        except Exception as e:
            # Handle any exceptions and return an error message
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))


# Create the Tornado web application with a single route
def make_app():
    return Application([
        (r"/memory", MemoryAnalysisHandler),
    ])


# Main function to run the application
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # Set the port to listen on
    print("Server is running on http://localhost:8888")
    IOLoop.current().start()
