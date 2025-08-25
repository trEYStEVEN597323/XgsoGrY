# 代码生成时间: 2025-08-25 22:37:13
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import logging
from alembic.config import Config as AlembicConfig
from alembic import command
from alembic.util.exc import CommandError
import os

# Define command-line options
define("migrations_directory", default="migrations", help="Directory containing migration scripts")
define("url", default="sqlite:///database.db", help="Database URL")
define("revision", default="head", help="Revision to migrate to. Default is 'head'.")
define("message", default="", help="Message to include in the revision log")
define("sql", default=False, help="Don't emit SQL to db, just print to stdout")
define("tag", default="", help="Arbitrary 'tag' name - can be used by custom env.py scripts")

class MigrationHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            # Perform the migration
            command.upgrade(self.alembic_config, options.revision)
            self.write({"status": "Migration successful"})
        except CommandError as ce:
            self.set_status(500)
            self.write({"status": "Migration failed", "error": str(ce)})
        except Exception as e:
            self.set_status(500)
            self.write({"status": "Migration failed", "error": str(e)})

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    @property
    def alembic_config(self):
        c = AlembicConfig()
        c.set_main_option("script_location", options.migrations_directory)
        c.set_main_option("sqlalchemy.url", options.url)
        c
        return c

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"message": "Database Migration Tool is running"})

def make_app():
    return tornado.web.Application([
        (r"/migrate", MigrationHandler),
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    # Parse command-line options
    tornado.options.parse_command_line()

    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Run the app
    app = make_app()
    app.listen(8888)
    logging.info("Database Migration Tool is starting on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()