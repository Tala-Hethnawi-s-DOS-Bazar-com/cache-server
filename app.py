from flask import Flask, jsonify, request
from cache import cache
from catalog_service import CatalogService
from order_service import OrderService

app = Flask(__name__)


@app.route('/cache/<book_id>', methods=["DELETE"])
def delete_cache(book_id):
    try:
        cache.delete(f"/info/{book_id}")
    except:
        pass
    return jsonify({"message": "Cache deleted successfully"})


@app.route('/purchase/<book_id>', methods=["POST"])
def purchase(book_id):
    try:
        return jsonify(OrderService().purchase(book_id=book_id))
    except Exception:
        return jsonify({"error": "Sorry!, we were unable to process your order"}), 500

@app.route('/search/<topic>', methods=["GET"])
@cache.cached(key_prefix="%s")
def search(topic):
    try:
        return jsonify(CatalogService().searchBooks(topic=topic))
    except:
        return jsonify({"error": "Failed to get results"}), 500


@app.route('/info/<book_id>', methods=["GET"])
@cache.cached(key_prefix="%s")
def info(book_id):
    # get the book with the requested id
    try:
        return jsonify(CatalogService().getBookInfo(book_id=book_id))
    except:
        return jsonify({"error": "Failed to get results"}), 500


@app.route('/update/<book_id>', methods=["PUT"])
def update(book_id):
    # get the book with the requested id
    request_body = request.json
    try:
        return jsonify(CatalogService().updateBookQuantity(book_id=book_id, quantity=request_body["quantity"]))
    except:
        return jsonify({"error": "Failed to update book"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    cache.init_app(app)
    cache.set("catalog_server", 0)
    cache.set("order_server", 0)
