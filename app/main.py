import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from typing import Any


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.
    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#E18F9B"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print("\n\n\nMove \n")
    print(json.dumps(data))
    json_string = json.dumps(data)
    game_data = json.loads(json_string)
    height = game_data["board"]["height"]
    width = game_data["board"]["width"]

    # to get my position
    my_position_x = []
    my_position_y = []
    my_length = 0


    for i in range(0, len(game_data["you"]["body"])):
        my_position_x.append(int(game_data["you"]["body"][i]["x"]))
        my_position_y.append(int(game_data["you"]["body"][i]["y"]))
        my_length+=1


    print("x =", my_position_x[0])
    print("y = ", my_position_y[0])
    print("height =", height)
    print("width =", width)
    print("length = ", my_length)

    #the 4 direction we can go

    left_x = my_position_x[0] - 1
    print("left is ", left_x)

    right_x = my_position_x[0] + 1
    print("right is", right_x)

    down_y = my_position_y[0] + 1

    up_y = my_position_y[0] - 1

    print("up is ", up_y)
    print("down is", down_y)

    # Truth value of four direction

    is_left = True
    is_right = True
    is_up = True
    is_down = True


    # Determine if its close to the wall

    is_left = (my_position_x[0] != 0)

    is_right = (my_position_x[0] != (width - 1))

    is_up = (my_position_y[0] != 0)

    is_down = (my_position_y[0] != (height - 1))

    # Determine if its close to own body

    for i in range(1, my_length - 1):
        if my_position_x[i] == my_position_x[0] and my_position_y[i] == up_y:
               is_up = False

        if my_position_x[i] == my_position_x[0] and my_position_y[i] == down_y :
                is_down = False

        if my_position_x[i] == left_x and my_position_y[0] == my_position_y[i]:
                is_left = False

        if my_position_x[i] == right_x and my_position_y[0] == my_position_y[i]:
                is_right = False

    directions = []

    print("right", is_right)
    print("left", is_left)
    print("up", is_up)
    print("down", is_down)

    #now that we know which direction we "cannot" go, let's find which direction we favor

    if is_right:
        directions.append('right')

    if is_left:
        directions.append('left')

    if is_up:
        directions.append('up')

    if is_down:
        directions.append('down')

    direction = random.choice(directions)

    print("Final decision", direction)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )