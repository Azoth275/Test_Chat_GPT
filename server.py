from flask import Flask, jsonify, request
from plateau import Plateau
from rover import Rover

class RoverAPI:
    """Flask based API wrapper exposing rover commands."""

    def __init__(self, width=5, height=5, obstacles=None):
        self.app = Flask(__name__)
        self.plateau = Plateau(width, height, obstacles or [])
        self.rover = Rover(self.plateau, 0, 0, 'N')

        # register routes
        self.app.add_url_rule('/status', 'status', self.status, methods=['GET'])
        self.app.add_url_rule('/command', 'command', self.command, methods=['POST'])
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])

    def status(self):
        """Return current rover state."""
        return jsonify({
            'x': self.rover.x,
            'y': self.rover.y,
            'direction': self.rover.direction,
            'width': self.plateau.width,
            'height': self.plateau.height,
            'obstacles': sorted(list(self.plateau.obstacles))
        })

    def command(self):
        """Execute a sequence of rover commands."""
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
        """Serve a minimal HTML UI for manual control."""
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

# instantiate default API for module level access
api = RoverAPI()
app = api.app

if __name__ == '__main__':
    app.run()
