from flask import Flask, jsonify

from catalog_service import CatalogService
from models import Order
from utils import session

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
