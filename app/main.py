import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
# from typing import Any


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
    headTpye = "pixel"
    tailType = "pixel"

    return start_response(color, headTpye, tailType)


@bottle.post('/move')
def move():
    data = bottle.request.json

    print("heroku testing")
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

    distinctsnakexy = []
    snakexy = []
    snakehead_x = []
    snakehead_y = []
    snake_num = 0
    snake_len = []
    food_x = []
    food_y = []

    for i in range (0, len(game_data["board"]["food"])):
        food_x.append(int(game_data["board"]["food"][i]["x"]))
        food_y.append(int(game_data["board"]["food"][i]["y"]))

    for i in range(0, len(game_data["board"]["food"])):
        print(food_x[i], " ")
        print(food_y[i], " ")

    for snake in game_data['board']['snakes']:
        onesnakexy = []  # one snake's body
        snake_num += 1
        onesnake = 0
        for coords in snake['body']:
            onesnakexy.append(list(coords.values()))
            snakexy.append(list(coords.values()))
            onesnake += 1
        distinctsnakexy.append(onesnakexy)
        snake_len.append(onesnake)
        snakehead_x.append(int(snake['body'][0]["x"]))
        snakehead_y.append(int(snake['body'][0]["y"]))

    # append all snakes head coordinates to an array of snake heads (eachcoordsofhead array in allsnakearray) (2dArray)

    myhead = list(game_data['you']['body'][0].values())

    print("Snake: ",  snake_num)

    for i in range(0, snake_num -1):
        print("\neach snake length: " + str(snake_len[i]) + "\n")


    print("x =", my_position_x[0])
    print("y = ", my_position_y[0])
    print("height =", height)
    print("width =", width)
    print("length = ", my_length)

    #the 4 direction we can go

    left_x = my_position_x[0] - 1

    right_x = my_position_x[0] + 1

    down_y = my_position_y[0] + 1

    up_y = my_position_y[0] - 1


    # Truth value of four direction is true by default

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

    print("I am here 1")
    #Determine if its close to enemy's body

    right = [myhead[0] + 1, myhead[1]]
    left = [myhead[0] - 1, myhead[1]]
    down = [myhead[0], myhead[1] + 1]
    up = [myhead[0], myhead[1] - 1]

    if right in snakexy:
        is_right = False

    if left in snakexy:
        is_left = False

    if down in snakexy:
        is_down = False

    if up in snakexy:
        is_up = False

    print("i am here 2")
    #now let's see who is the closest snake to us

    distance_min = []

    # Check for right

    for i in range (0, len(game_data["board"]["food"])):
        x = food_x[i] - right_x
        y = food_y[i] - my_position_y[0]
        distance = x**2 + y**2
        if is_right == False:
            distance_min.append(99999999)
            break
        elif len(distance_min)==0:
            distance_min.append(distance)
        else:
            if distance_min[0] > distance:
                distance_min.pop()
                distance_min.append(distance)

#    print("Distance Right", distance_min[0])

    for i in range (0, len(game_data["board"]["food"])):
        x = food_x[i] - left_x
        y = food_y[i] - my_position_y[0]
        distance = x**2 + y**2
        if is_left == False:
            distance_min.append(99999999)
            break
        elif len(distance_min) < 2:
            distance_min.append(distance)
        else:
            if distance_min[1] > distance:
                distance_min.pop()
                distance_min.append(distance)

 #   print("Distance Left", distance_min[1])

    for i in range (0, len(game_data["board"]["food"])):
        x = food_x[i] - my_position_x[0]
        y = food_y[i] - down_y
        distance = x**2 + y**2
        if is_down == False:
            distance_min.append(99999999)
            break
        elif len(distance_min) < 3:
            distance_min.append(distance)
        else:
            if distance_min[2] > distance:
                distance_min.pop()
                distance_min.append(distance)

  #  print("Distance Down", distance_min[2])

    for i in range (0, len(game_data["board"]["food"])):
        x = food_x[i] - my_position_x[0]
        y = food_y[i] - up_y
        distance = x**2 + y**2
        if is_up == False:
            distance_min.append(99999999)
            break
        elif len(distance_min) < 4:
            distance_min.append(distance)
        else:
            if distance_min[3] > distance:
                distance_min.pop()
                distance_min.append(distance)

  #  print("Distance Up", distance_min[3])


    dir = 0

    for i in range(0 , 3):
        if distance_min[i] == min(distance_min):
            break
        else:
            dir += 1

    for i in range(0, snake_num - 1):
        print("\nSnakeHeadsX: " + str(snakehead_x[i]))

    for i in range(0, snake_num - 1):
        print("\nSnakeHeadsY: " + str(snakehead_y[i]))


    if dir == 0:
        direction = 'right'

    if dir == 1:
        direction = 'left'

    if dir == 2:
        direction = 'down'

    if dir == 3:
        direction = 'up'


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