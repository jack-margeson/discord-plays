# converts a queue of commands to inputs

import keyboard
import json
from collections import deque

# keyboard.press()
# keyboard.release()
# keyboard.call_later(fn, args=(), delay=0.001)


def load_controls_dict(filename):
    with open(filename) as json_file:
        return json.load(json_file)


def add_command(controlsDict, queue, command):
    print(queue, command)
    queue.append(controlsDict[command])


def controls_update(queue):
    if queue:
        action = queue.popleft()
        keyboard.press(action)
        keyboard.call_later(keyboard.release, args=(action), delay=1)
