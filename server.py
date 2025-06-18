from flask import Flask, jsonify, request
from plateau import Plateau
from rover import Rover

app = Flask(__name__)

# Initial plateau and rover setup
plateau = Plateau(5, 5, obstacles={(2, 2)})
rover = Rover(plateau, 0, 0, 'N')

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'x': rover.x,
        'y': rover.y,
        'direction': rover.direction,
        'width': plateau.width,
        'height': plateau.height,
        'obstacles': sorted(list(plateau.obstacles))
    })

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json(force=True)
    commands = data.get('commands')
    if not commands:
        return jsonify({'error': 'commands field required'}), 400
    try:
        rover.execute_commands(commands)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    return status()

@app.route('/')
def index():
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

if __name__ == '__main__':
    app.run()
