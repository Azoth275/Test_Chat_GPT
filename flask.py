class _Request:
    def __init__(self):
        self._json = None

    def get_json(self, force=False):
        return self._json

request = _Request()


def jsonify(obj):
    return obj


class Response:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status

    def get_json(self):
        return self._data


class Flask:
    def __init__(self, name):
        self.routes = {}

    def add_url_rule(self, rule, endpoint, view_func, methods=None):
        for m in methods or ['GET']:
            self.routes.setdefault(rule, {})[m.upper()] = view_func

    def test_client(self):
        return _TestClient(self)

    def run(self, host='127.0.0.1', port=5000):
        # no-op for tests
        pass


class _TestClient:
    def __init__(self, app):
        self.app = app

    def _call(self, path, method, json=None):
        view = self.app.routes[path][method]
        request._json = json
        result = view()
        request._json = None
        if isinstance(result, tuple):
            data, status = result
        else:
            data, status = result, 200
        return Response(data, status)

    def get(self, path):
        return self._call(path, 'GET')

    def post(self, path, json=None):
        return self._call(path, 'POST', json=json)
