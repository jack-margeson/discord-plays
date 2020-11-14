# converts a queue of commands to inputs

import keyboard
import json

# keyboard.press()
# keyboard.release()
# keyboard.call_later(fn, args=(), delay=0.001)


def load_controls_dict(filename):
    with open(filename) as json_file:
        return json.load(json_file)


def add_command(controlsDict, queue, command):
    queue.append(controlsDict(command))
    return queue


def update(queue):
    keyboard.release(queue[0])
    queue.popleft()
    keyboard.press(queue[0])
    return queue
