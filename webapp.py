from wsgiref.simple_server import make_server
from web import app

httpd = make_server('', 3031, app)
print "Serving on port 3031..."
httpd.serve_forever()
