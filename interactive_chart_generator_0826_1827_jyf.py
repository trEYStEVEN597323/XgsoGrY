# 代码生成时间: 2025-08-26 18:27:35
import tornado.ioloop
import tornado.web
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, CustomJS
import numpy as np

# InteractiveChartHandler handles the generation of interactive charts
class InteractiveChartHandler(tornado.web.RequestHandler):
    def get(self):
        # Create a sample data source
        x = np.linspace(0, 4 * np.pi, 100)
        y = np.sin(x)
        source = ColumnDataSource(data=dict(x=x, y=y))

        # Create a figure
        p = figure(plot_width=400, plot_height=400)
        p.line('x', 'y', source=source)
        p.add_tools(HoverTool(tooltips=[("x", "@x"), ("y", "@y")]))

        # Add a CustomJS callback to update the chart
        callback = CustomJS(args=dict(source=source), code="""
            const data = source.data;
            const x = data['x'];
            const y = data['y'];
            y = y.map((y, idx) => Math.sin(x[idx] + 2));
            source.change.emit();
        """)
        p.js_on_change('left_button', callback)

        # Output the HTML file with the chart
        output_file("chart.html")
        show(p)
        # Get the HTML and JavaScript components
        script, div = components(p)
        self.write("""<html><head></head><body>""" + div + """</body></html><script>""" + script + """</script>""")

# Define the URL routes
def make_app():
    return tornado.web.Application(
        handlers=[
            (r"/chart", InteractiveChartHandler),
        ],
        debug=True,
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Interactive chart generator is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()