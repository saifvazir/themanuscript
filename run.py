from TMS import app

import os
import sys
sys.path.insert(0, '/home/themanuscript/public_html/cgi-bin/myenv/lib/python2.6/site-packages') 
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
