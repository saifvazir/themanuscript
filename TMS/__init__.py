
from flask import Flask

app = Flask(__name__)
# CORS(app)

from TMS.api.Users import views
# from k_app.api.Inventory import views
# from k_app.api.Vendors import views
# from k_app.api.Misc import views
# from k_app.api.Orders import views
# from k_app.api.Customers import views
# from k_app.api.Pricing import views
# from k_app.api.Products import views
# from k_app.api.Vendors import views

