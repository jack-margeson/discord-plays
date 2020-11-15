# converts a queue of commands to inputs

import keyboard
import json
from collections import deque

# keyboard.press()
# keyboard.release()
# keyboard.call_later(fn, args=(), delay=0.001)


def load_config(filename):
    with open(filename) as json_file:
        return json.load(json_file)


def add_command(controlsDict, queue, command):
    queue.append(controlsDict[command])


def controls_update(queue, delay, mode):
    if queue:
        print('Current queue:')
        print(queue)
        if mode == 'anarchy':
            action = queue.popleft()
        elif mode == 'democracy':
            actions = {}
            for action in queue:
                actions[action] = 0
            for action in queue:
                actions[action] += 1
            max = queue[0]
            for action, count in actions.items():
                if actions[max] > count:
                    max = action

            queue.clear()

        print('Current action:')
        print(action)
        keyboard.press(action)
        keyboard.call_later(keyboard.release, args=([action]), delay=delay)
