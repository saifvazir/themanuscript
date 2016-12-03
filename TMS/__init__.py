from k_app.imports import *
from k_app.functions import *
from k_app.constants import * 

app = Flask(__name__)
CORS(app)

from k_app.api.Procurements import views
from k_app.api.Inventory import views
from k_app.api.Vendors import views
from k_app.api.Misc import views
from k_app.api.Orders import views
from k_app.api.Customers import views
from k_app.api.Pricing import views
from k_app.api.Products import views
from k_app.api.Vendors import views

