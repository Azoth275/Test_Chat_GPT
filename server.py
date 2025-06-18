from flask import Flask, jsonify, request
from plateau import Plateau
from rover import Rover


class RoverServer:
    """Encapsulates the Flask app and rover state."""

    def __init__(self, width=5, height=5, obstacles=None):
        self.app = Flask(__name__)
        self.plateau = Plateau(width, height, obstacles=obstacles or {(2, 2)})
        self.rover = Rover(self.plateau, 0, 0, 'N')
        self._register_routes()

    # ------------------------------------------------------------------
    # route registration
    def _register_routes(self):
        self.app.add_url_rule('/status', view_func=self.status)
        self.app.add_url_rule('/command', methods=['POST'], view_func=self.command)
        self.app.add_url_rule('/', view_func=self.index)

    # ------------------------------------------------------------------
    # endpoints
    def status(self):
        return jsonify({
            'x': self.rover.x,
            'y': self.rover.y,
            'direction': self.rover.direction,
            'width': self.plateau.width,
            'height': self.plateau.height,
            'obstacles': sorted(list(self.plateau.obstacles)),
        })

    def command(self):
        data = request.get_json(force=True)
        commands = data.get('commands')
        if not commands:
            return jsonify({'error': 'commands field required'}), 400
        try:
            self.rover.execute_commands(commands)
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 400
        return self.status()

    def index(self):
        return '''<html><head>
<script>
async function sendCmd(){
  const cmd = document.getElementById("cmd").value;
  await fetch('/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({commands:cmd})});
  load();
}
async function load(){
  const res = await fetch('/status');
  const data = await res.json();
  document.getElementById('pos').textContent = `Position: (${data.x},${data.y})`;
  document.getElementById('dir').textContent = `Direction: ${data.direction}`;
  document.getElementById('ob').textContent = JSON.stringify(data.obstacles);
}
window.onload=load;
</script></head>
<body>
<div id='pos'></div>
<div id='dir'></div>
<div>Obstacles: <span id='ob'></span></div>
<input id='cmd'/>
<button onclick='sendCmd()'>Send</button>
</body></html>'''

    # ------------------------------------------------------------------
    def reset(self):
        """Reset rover state to the origin facing north."""
        self.rover.x = 0
        self.rover.y = 0
        self.rover.direction = 'N'


def create_server(width=5, height=5, obstacles=None):
    """Factory returning a configured :class:`RoverServer`."""
    return RoverServer(width, height, obstacles)


def create_app(width=5, height=5, obstacles=None):
    """Factory returning a Flask app for external use."""
    return create_server(width, height, obstacles).app


if __name__ == '__main__':
    # Run a standalone server instance for manual testing
    create_app().run()
