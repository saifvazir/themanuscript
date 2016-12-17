from wsgiref.handlers import CGIHandler
from TMS import app

CGIHandler().run(app)