################################
# message class that is broadcasted and if not in distance when it gets lost
# denial of service attack to make drones not be able to get or broadcast messages for a period of time
# add recursion for neighbor of neighbor to send message to all in network with quality of signal > 0.5
# when jammed, it can not communicate with other drone not just about target but everything
# increase number of attacked drones using for loop outside and create new global variable
# if drone attacked it cant detect
################################


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
UAV_COUNT = 20
UAV_RADIUS = 5
COMMUNICATION_RANGE = 100
MOVE_STEP = 5
FPS = 30

SEPARATION_WEIGHT = 0.05
ALIGNMENT_WEIGHT = 0.05
SEPARATION_DISTANCE = 20

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (120, 120, 0)

SIGNAL_QUALITY_THRESHOLD = 0.3
TARGET_DETECTION_RADIUS = 10


BASE_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
BASE_SIZE = 10

ACTIVATION_DELAY = 0.1
BATTERY_LIFE = 100
BATTERY_DRAIN_RATE = 0.01
BATTERY_MINIMUM_THRESHOLD = 10

ATTACK_DURATION = 3
ATTACK_INTERVAL = 6

FORCE_QUIT_TIME = 20
