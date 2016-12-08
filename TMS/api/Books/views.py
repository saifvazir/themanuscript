
from TMS import app


@app.route('/api/v1.0/protected')
# @login_required
def protected():
	return "logged in"