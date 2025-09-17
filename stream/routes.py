from flask import render_template_string, Response
from . import helpers, streamer

HTML_PAGE = """
<html>
  <head>
    <title>Screen Stream</title>
    <meta charset="utf-8"/>
  </head>
  <body style="background:#111; color:#eee; text-align:center;">
      <img src="{{ stream_url }}" />
  </body>
</html>
"""

def init_routes(app):
    @app.route('/')
    def index():
        return render_template_string(HTML_PAGE, stream_url="/stream")

    @app.route('/stream')
    def stream():
        return Response(streamer.generate_mjpeg(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
