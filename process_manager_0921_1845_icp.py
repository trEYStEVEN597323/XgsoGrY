# 代码生成时间: 2025-09-21 18:45:17
import os
import signal
import subprocess
import tornado.ioloop
import tornado.web
from tornado.options import define, options

# Define command line options
define("port", default=8888, help="Port to run the server on", type=int)

class ProcessManager(tornado.web.RequestHandler):
    """
    A Tornado RequestHandler that allows to start and kill processes.
    """
    def get(self):
        """
        GET request handler to list current processes.
        """
        processes = subprocess.check_output(["ps", "aux"]).decode("utf-8\)
        self.write(processes)

    def post(self):
        """
        POST request handler to start a new process.
        """
        try:
            command = self.get_argument("command")
            process = subprocess.Popen(command, shell=True)
            self.write(f"Process started with PID {process.pid}")
        except Exception as e:
            self.write(f"Failed to start process: {e}")
            self.set_status(400)

    def delete(self, pid):
        """
        DELETE request handler to kill a process by its PID.
        """
        try:
            os.kill(int(pid), signal.SIGTERM)
            self.write(f"Process {pid} terminated")
        except ProcessLookupError:
            self.write(f"No process found with PID {pid}")
            self.set_status(404)
        except Exception as e:
            self.write(f"Failed to terminate process {pid}: {e}")
            self.set_status(500)

def make_app():
    """
    Creates a Tornado application with one ProcessManager handler.
    """
    return tornado.web.Application(
        [
            (r"/", ProcessManager),
            (r"/(\d+)", ProcessManager),
        ]
    )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print(f"Process manager server running on port {options.port}")
    tornado.ioloop.IOLoop.current().start()