# Test_Chat_GPT

This repository contains a minimal Mars Rover simulation. The rover moves on a
rectangular plateau and avoids obstacles. When an obstacle is directly in front
of the rover, a subsequent left or right turn followed immediately by a forward
movement is ignored so that the rover cannot slip past the obstacle diagonally.

## Running the tests

Execute the unit tests with:
```bash
python3 -m unittest discover
```

## Running the REST API

Install Flask if it is not already available and start the server:
```bash
python3 -m pip install Flask
python3 server.py
```
Open `http://localhost:5000` in a browser to see the simple UI and control the rover.
