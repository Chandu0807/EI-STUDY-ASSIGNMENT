class Command:
    def execute(self, rover):
        pass

class MoveCommand(Command):
    def execute(self, rover):
        rover.move()

class TurnLeftCommand(Command):
    def execute(self, rover):
        rover.turn_left()

class TurnRightCommand(Command):
    def execute(self, rover):
        rover.turn_right()

class Rover:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self):
        # Update position based on direction
        if self.direction == 'N':
            self.y += 1
        elif self.direction == 'S':
            self.y -= 1
        elif self.direction == 'E':
            self.x += 1
        elif self.direction == 'W':
            self.x -= 1

    def turn_left(self):
        # Update direction by turning left
        directions = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        self.direction = directions[self.direction]

    def turn_right(self):
        # Update direction by turning right
        directions = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        self.direction = directions[self.direction]

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []

    def add_obstacle(self, x, y):
        self.obstacles.append((x, y))

    def is_obstacle(self, x, y):
        return (x, y) in self.obstacles

    def within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


import logging

def get_input():
    logger = logging.getLogger(__name__)
    commands = []
    obstacles = []
    grid_size = (10, 10)

    try:
        print("Enter commands (M(forward), L(left), R(right)):")
        commands = input().split()

        print("Enter obstacles (x, y):")
        while True:
            obstacle = input()
            if obstacle == "":
                break
            x, y = map(int, obstacle.split(","))
            
            # Check if obstacle point is within the grid size
            if x >= grid_size[0] or y >= grid_size[1]:
                raise ValueError("Obstacle point is greater than the grid size")

            obstacles.append((x, y))

        print("Enter the grid size (width, height): ")
        grid_size_input = input().split()
        grid_size = (int(grid_size_input[0]), int(grid_size_input[1]))

        if not all(isinstance(command, str) and command in ['M', 'L', 'R'] for command in commands):
            raise ValueError("Invalid commands")

        if not all(isinstance(obstacle, tuple) and len(obstacle) == 2 and all(isinstance(coordinate, int) for coordinate in obstacle) for obstacle in obstacles):
            raise ValueError("Invalid obstacles")

        if grid_size[0] <= 0 or grid_size[1] <= 0:
            raise ValueError("Invalid grid size")

    except Exception as e:
        logger.error(e)
        raise

    return commands, obstacles, grid_size





if __name__ == "__main__":
    commands, obstacles, grid_size = get_input()

    grid = Grid(grid_size[0], grid_size[1])
    for obstacle in obstacles:
        grid.add_obstacle(obstacle[0], obstacle[1])

    rover = Rover(0, 0, 'N')

    command_map = {
        'M': MoveCommand(),
        'L': TurnLeftCommand(),
        'R': TurnRightCommand()
    }
    dir={
     'N':'North',
     'S':'South',
     'E':'East',
     'W':'West'
    }
    for command in commands:
        if not grid.is_obstacle(rover.x, rover.y):
            if command in command_map:
                command_obj = command_map[command]
                command_obj.execute(rover)
        if not grid.within_bounds(rover.x, rover.y):
            print("Rover went out of bounds!")
            break

    if grid.is_obstacle(rover.x, rover.y):
        print("Obstacle detected at position:", (rover.x, rover.y))
        print("Final Position:", (rover.x, rover.y, rover.direction))
        print(f"Status Report: Rover is at ({rover.x}, {rover.y}) facing {dir[ rover.direction]}. Obstacles detected.")
    else:
        print("Final Position:", (rover.x, rover.y, rover.direction))
        print(f"Status Report: Rover is at ({rover.x}, {rover.y}) facing {dir[ rover.direction]}. No obstacles detected.")
