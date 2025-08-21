# 代码生成时间: 2025-08-22 03:32:03
import tornado.ioloop
import tornado.web
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.models import ColumnDataSource
import numpy as np
import json

"""
Interactive Chart Generator using Python and Tornado framework.
This application allows users to interactively create charts by providing data and chart settings.
"""

class MainHandler(tornado.web.RequestHandler):
    """
    Tornado request handler for the main page.
    Displays the interactive chart generator interface.
    """
    def get(self):
        self.render('index.html')

    def post(self):
        try:
            # Get data from request
            data = json.loads(self.get_argument('data'))
            chart_type = self.get_argument('chart_type')
            width = int(self.get_argument('width'))
            height = int(self.get_argument('height'))

            # Generate chart based on data and chart settings
            chart = generate_chart(data, chart_type, width, height)

            # Get the HTML and script components of the chart
            html, script = components(chart)

            # Return the chart components in the response
            self.write({'html': html, 'script': script})
        except Exception as e:
            # Handle any errors and return an error message
            self.write({'error': str(e)})

def generate_chart(data, chart_type, width, height):
    """
    Generate a chart based on the provided data and chart settings.

    Args:
        data (dict): A dictionary containing the data for the chart.
        chart_type (str): The type of chart to generate (e.g., 'line', 'bar', etc.).
        width (int): The width of the chart.
        height (int): The height of the chart.

    Returns:
        figure: The generated chart.
    """
    # Create a ColumnDataSource from the data
    source = ColumnDataSource(data)

    # Create a new figure
    p = figure(title='Interactive Chart', x_axis_label='X', y_axis_label='Y', width=width, height=height)

    # Add a renderer to the plot based on the chart type
    if chart_type == 'line':
        p.line(x='x', y='y', source=source)
    elif chart_type == 'bar':
        p.vbar(x='x', top='y', width=0.5, source=source)
    elif chart_type == 'scatter':
        p.scatter(x='x', y='y', source=source)
    else:
        raise ValueError('Unsupported chart type')

    return p


# Define the Tornado application and routes
application = tornado.web.Application([
    (r'/', MainHandler),
])

if __name__ == '__main__':
    # Start the Tornado IOLoop
    application.listen(8888)
    print('Starting server on http://localhost:8888/')
    tornado.ioloop.IOLoop.current().start()