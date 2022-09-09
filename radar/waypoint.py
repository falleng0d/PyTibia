import collections
import json
import time
from time import sleep, time
from typing import List
import radar.config
import numpy as np
from numpy import dtype
import hud.core
import radar.core
import utils.core
import utils.AStar
from hud import creatures
import battleList
import actionBar.slot

waypointArray = np.array([], dtype=dtype)
waypointIndex = None
leaveLoop = False
goalSqm = None
currentSqm = None
delaySpeed = None
lastActionTime = None

waypointType = np.dtype([
    ('routeName', np.str_, 64),
    ('routeType', np.str_, 64),
    ('routeNextRoute', np.str_, 64),
    ('routeLeaveCriteria1', np.uint32, (2,)),
    ('routeLeaveCriteria2', np.uint32, (2,)),
    ('routeLeaveCriteria3', np.uint32, (2,)),
    ('routeLeaveCriteria4', np.uint32, (2,)),
    ('id', np.uint32),
    ('type', np.str_, 64),
    ('coordinate', np.uint32, (3,)),
    ('combatStyle', np.str_, 64),
    ('hotkey', np.str_, 64),
    ('waitTime', np.uint32),
    ('minCreatures', np.uint32),
    ('speed', np.uint32),
    ('tolerance', np.uint32)
])


def loadWaypointJSON(filename):
    global waypointArray
    waypointList = []
    wptFile = open(filename)
    jsonFile = json.load(wptFile)
    for i in range(len(jsonFile['routes'])):
        for j in range(len(jsonFile['routes'][i]['waypoints'])):
            waypointList.append((
                jsonFile['routes'][i]['name'],
                jsonFile['routes'][i]['type'],
                jsonFile['routes'][i]['nextRoute'],
                (jsonFile['routes'][i]['leaveCriteria'][0]['slot'],
                 jsonFile['routes'][i]['leaveCriteria'][0]['minQuantity']) if "leaveCriteria" in jsonFile['routes'][
                    i] else (0, 0),
                (jsonFile['routes'][i]['leaveCriteria'][1]['slot'],
                 jsonFile['routes'][i]['leaveCriteria'][1]['minQuantity']) if "leaveCriteria" in jsonFile['routes'][
                    i] else (0, 0),
                (jsonFile['routes'][i]['leaveCriteria'][2]['slot'],
                 jsonFile['routes'][i]['leaveCriteria'][2]['minQuantity']) if "leaveCriteria" in jsonFile['routes'][
                    i] else (0, 0),
                (jsonFile['routes'][i]['leaveCriteria'][3]['slot'],
                 jsonFile['routes'][i]['leaveCriteria'][3]['minQuantity']) if "leaveCriteria" in jsonFile['routes'][
                    i] else (0, 0),
                jsonFile['routes'][i]['waypoints'][j]['id'],
                jsonFile['routes'][i]['waypoints'][j]['type'],
                tuple(jsonFile['routes'][i]['waypoints'][j]['coord']) if "coord" in jsonFile['routes'][i]['waypoints'][
                    j] else (0, 0, 0),
                jsonFile['routes'][i]['waypoints'][j]['combatStyle'] if "combatStyle" in
                                                                        jsonFile['routes'][i]['waypoints'][
                                                                            j] else 'none',
                jsonFile['routes'][i]['waypoints'][j]['hotkey'] if "hotkey" in jsonFile['routes'][i]['waypoints'][
                    j] else 'none',
                jsonFile['routes'][i]['waypoints'][j]['waitTime'],
                jsonFile['routes'][i]['waypoints'][j]['minCreatures'] if "minCreatures" in
                                                                         jsonFile['routes'][i]['waypoints'][j] else 0,
                jsonFile['routes'][i]['waypoints'][j]['speed'],
                jsonFile['routes'][i]['waypoints'][j]['tolerance']))

    waypointArray = np.array(waypointList, dtype=waypointType)

    return waypointArray


def shouldLeaveLoop(screenshot, waypoint):
    meetCriteria = False

    a = actionBar.slot.getSlotCount(screenshot, 'f' + str(waypoint['routeLeaveCriteria2'][0]))
    if waypoint['routeLeaveCriteria1'][1] > actionBar.slot.getSlotCount(screenshot, 'f' + str(
            waypoint['routeLeaveCriteria1'][0])):
        meetCriteria = True

    aaa = actionBar.slot.getSlotCount(screenshot, 'f' + str(waypoint['routeLeaveCriteria2'][0]))
    if waypoint['routeLeaveCriteria2'][1] > actionBar.slot.getSlotCount(screenshot, 'f' + str(
            waypoint['routeLeaveCriteria2'][0])):
        meetCriteria = True

    b = actionBar.slot.getSlotCount(screenshot, 'f' + str(waypoint['routeLeaveCriteria2'][0]))
    if waypoint['routeLeaveCriteria3'][1] > actionBar.slot.getSlotCount(screenshot, 'f' + str(
            waypoint['routeLeaveCriteria3'][0])):
        meetCriteria = True

    bbb = actionBar.slot.getSlotCount(screenshot, 'f' + str(waypoint['routeLeaveCriteria2'][0]))
    if waypoint['routeLeaveCriteria4'][1] > actionBar.slot.getSlotCount(screenshot, 'f' + str(
            waypoint['routeLeaveCriteria4'][0])):
        meetCriteria = True

    return meetCriteria


# TODO: Implement the other types of waypoints
def waypointManager(screenshot, currentPlayerCoordinate):
    global waypointIndex, leaveLoop

    if waypointIndex is None:
        waypointIndex = radar.core.getWaypointIndexFromClosestCoordinate(currentPlayerCoordinate, waypointArray)

    waypoint = waypointArray[waypointIndex]

    aaa = waypoint['type']

    isGroundWaypoint = waypoint['type'] == 'ground'
    if isGroundWaypoint:

        loop_time = time()
        status = goToNextWaypoint(screenshot, currentPlayerCoordinate)
        timef = (time() - loop_time)
        timef = timef if timef else 1
        fps = 1 / timef
        print('FPS goToNextWaypoint {}'.format(fps))
        if status is True:
            print(
                f"Reached waypoint idx:{str(waypointIndex)} {waypoint['coordinate'][0]} {waypoint['coordinate'][1]} {waypoint['coordinate'][2]}")

    isRampWaypoint = waypoint['type'] == 'ramp'
    if isRampWaypoint:
        (currentPlayerCoordinateX, currentPlayerCoordinateY, _) = currentPlayerCoordinate
        (waypointCoordinateX, waypointCoordinateY, _) = waypoint['coordinate']
        xDifference = currentPlayerCoordinateX - waypointCoordinateX
        shouldWalkToLeft = xDifference > 0
        if shouldWalkToLeft:
            utils.core.press('left')

        shouldWalkToRight = xDifference < 0
        if shouldWalkToRight:
            utils.core.press('right')

        yDifference = currentPlayerCoordinateY - waypointCoordinateY
        if yDifference < 0:
            utils.core.press('down')

        if yDifference > 0:
            utils.core.press('up')

    isTradeWaypoint = waypoint['type'] == 'trade'
    if isTradeWaypoint:
        # TODO: Implement chat method to make trade action
        print('chat method here')

    hasReachedEnd = waypointIndex + 1 >= len(waypointArray)
    indexesOfRoute = np.where(waypointArray['routeName'] == waypoint['routeName'])

    if waypoint['routeType'] != 'loop' and status is True:
        if not hasReachedEnd:
            nameOfNextRoute = waypointArray[waypointIndex + 1]['routeName']
            if waypoint['routeName'] == nameOfNextRoute:
                waypointIndex += 1
                return
            else:
                waypointIndex = np.where(waypointArray['routeName'] == waypoint['routeNextRoute'])[0][0]
                return
        else:
            waypointIndex = np.where(waypointArray['routeName'] == waypoint['routeNextRoute'])[0][0]
            return

    if waypoint['routeType'] == 'loop' and status is True:

        if indexesOfRoute[0][0] == waypointIndex:
            if shouldLeaveLoop(screenshot, waypoint):
                waypointIndex = np.where(waypointArray['routeName'] == waypoint['routeNextRoute'])[0][0]
                return

        if not hasReachedEnd:
            nameOfNextRoute = waypointArray[waypointIndex + 1]['routeName']
            if waypoint['routeName'] == nameOfNextRoute:
                waypointIndex += 1
                return
            else:
                waypointIndex = np.where(waypointArray['routeType'] == 'loop')[0][0]
                return
        else:
            waypointIndex = np.where(waypointArray['routeType'] == 'loop')[0][0]
            return


def goToNextWaypoint(screenshot, currentPlayerCoordinate):
    global waypointIndex, waypointArray, lastPlayerCoordinate

    walkStatus = arrowKeysWalk(screenshot, currentPlayerCoordinate, waypointArray[waypointIndex]['coordinate'])

    if walkStatus is None:
        # TODO: Handle waypoint not on this floor
        print('Method to treat incorrect coordinates here')
        return None
    (hasReachedDestination, isMonsterBlocking) = walkStatus
    #newPlayerCoordinate = radar.core.getCoordinate(screenshot, currentPlayerCoordinate)
    # if newPlayerCoordinate == currentPlayerCoordinate:
    #    # TODO: Handle being stuck on the same position
    #    #print('Player is stuck')
    if hasReachedDestination:
        return True
    if isMonsterBlocking:
        # TODO: Handle monster blocking the path
        print('A creature is blocking the path, change stance to attack')
    return False


def arrowKeysWalk(screenshot, origin, destination):

    global goalSqm, currentSqm, delaySpeed, lastActionTime
    (x1, y1, z1) = origin
    x1, y1 = utils.core.getPixelFromCoordinate(origin)
    (x2, y2, z2) = destination
    x2, y2 = utils.core.getPixelFromCoordinate(destination)
    if z1 != z2:
        if utils.core.manualPressCurrentKeyDown is not None:
            utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)
        return None

    if (x1, y1) == currentSqm and currentSqm is not None:
        print('Ainda esta no mesmo SQM, nao precisa mexer, retornando False False')
        return False, False

    currentTime = time()
    if delaySpeed is not None and lastActionTime is not None:
        if lastActionTime + delaySpeed >= currentTime - delaySpeed*0.50:
            print('Ainda nao esta na hora da acao, retornando False False')
            print(f'lastActionTime {lastActionTime} delaySpeed {delaySpeed} currentTime {currentTime} delaySpeed*0.66 {delaySpeed*0.66} diff {(lastActionTime + delaySpeed) - (currentTime - delaySpeed*0.66)}')
            print('-----')
            return False, False

    currentSqm = (x1, y1)

    #if (x1, y1) == goalSqm:


    #radarImg = radar.config.floorsImgs[z1][y1 - 50:y1 + 50, x1 - 50:x1 + 50]
    #radarWalkableFloorSqms = np.where(
    #    np.isin(radarImg, radar.config.nonWalkablePixelsColors), 1, 0)
    #radarWalkableFloorWithMonstersSqms = np.where(
    #    np.isin(radarImg, radar.config.nonWalkablePixelsColors), 1, 0)
    radarWalkableFloorSqms = radar.config.waypointWalkableFloorsSqms[z1][y1 - 50:y1 + 50, x1 - 50:x1 + 50]
    radarWalkableFloorWithMonstersSqms = radar.config.waypointWalkableFloorsSqms[z1][y1 - 50:y1 + 50, x1 - 50:x1 + 50]
    #battleListCreatures = battleList.core.getCreatures(screenshot)

    #creaturesHud = hud.creatures.getCreatures(screenshot, battleListCreatures)

    #for creature in creaturesHud:
    #    radarWalkableFloorWithMonstersSqms[creature['slot'][1] + 45, creature['slot'][0] + 43] = 1

    if abs(y2 - y1) == 0 and abs(x2 - x1) == 0:
        if utils.core.manualPressCurrentKeyDown is not None:
            utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)
            print('chegou no destino, retornando True False')
        return True, False

    path = utils.AStar.search(radarWalkableFloorWithMonstersSqms, 1, (50, 50), (y2 - y1 + 50, x2 - x1 + 50))

    if path is None:
        path = utils.AStar.search(radarWalkableFloorSqms, 1, (50, 50), (y2 - y1 + 50, x2 - x1 + 50))
        if path is not None:
            if utils.core.manualPressCurrentKeyDown is not None:
                utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)
            print('Travado, retornando False True')
            return False, True

    (calcY, calcX) = path[1]
    print(f"X: {calcX} Y: {calcY}")
    print(f'Coord atual {origin[0], origin[1]}')


    # converter coordenadas de volta nas coords do jogo para ter um pathing mais preciso
    if calcY < 50 and calcX < 50:
        delaySpeed = speedBreakpoints(getPlayerSpeed(), (currentSqm[0], currentSqm[1], z1), 'q') / 1000
        lastActionTime = time()
        if utils.core.manualPressCurrentKeyDown is None:
            utils.core.manualPress('q', True)
            print('nao havia nada apertado, apertando q')
        elif utils.core.manualPressCurrentKeyDown != 'q':
            print('soltando ' + utils.core.manualPressCurrentKeyDown + ' e pressionando q')
            #utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)

            utils.core.manualPress('q', True)
        else:
            print('ja esta apertando o a, nao fara nada')

    if calcY < 50 and calcX > 50:
        delaySpeed = speedBreakpoints(getPlayerSpeed(), (currentSqm[0], currentSqm[1], z1), 'e') / 1000
        lastActionTime = time()
        if utils.core.manualPressCurrentKeyDown is None:
            utils.core.manualPress('e', True)
            print('nao havia nada apertado, apertando e')
        elif utils.core.manualPressCurrentKeyDown != 'e':
            print('soltando ' + utils.core.manualPressCurrentKeyDown + ' e pressionando e')
            #utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)

            utils.core.manualPress('e', True)
        else:
            print('ja esta apertando o e, nao fara nada')

    if calcY > 50 and calcX < 50:
        delaySpeed = speedBreakpoints(getPlayerSpeed(), (currentSqm[0], currentSqm[1], z1), 'z') / 1000
        lastActionTime = time()
        if utils.core.manualPressCurrentKeyDown is None:
            utils.core.manualPress('z', True)
            print('nao havia nada apertado, apertando z')
        elif utils.core.manualPressCurrentKeyDown != 'z':
            print('soltando ' + utils.core.manualPressCurrentKeyDown + ' e pressionando z')
            #utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)

            utils.core.manualPress('z', True)
        else:
            print('ja esta apertando o z, nao fara nada')

    if calcY > 50 and calcX > 50:
        delaySpeed = speedBreakpoints(getPlayerSpeed(), (currentSqm[0], currentSqm[1], z1), 'c') / 1000
        lastActionTime = time()
        if utils.core.manualPressCurrentKeyDown is None:
            utils.core.manualPress('c', True)
            print('nao havia nada apertado, apertando c')
        elif utils.core.manualPressCurrentKeyDown != 'c':
            print('soltando ' + utils.core.manualPressCurrentKeyDown + ' e pressionando c')
            #utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)

            utils.core.manualPress('c', True)
        else:
            print('ja esta apertando o c, nao fara nada')

    if calcY < 50 and calcX == 50:
        delaySpeed = speedBreakpoints(getPlayerSpeed(), (currentSqm[0], currentSqm[1], z1), 'w') / 1000
        lastActionTime = time()
        if utils.core.manualPressCurrentKeyDown is None:
            utils.core.manualPress('w', True)
            print('nao havia nada apertado, apertando w')
        elif utils.core.manualPressCurrentKeyDown != 'w':
            print('soltando ' + utils.core.manualPressCurrentKeyDown + ' e pressionando w')
            #utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)
            utils.core.manualPress('w', True)
        else:
            print('ja esta apertando o w, nao fara nada')

    if calcY > 50 and calcX == 50:
        delaySpeed = speedBreakpoints(getPlayerSpeed(), (currentSqm[0], currentSqm[1], z1), 's') / 1000
        lastActionTime = time()
        if utils.core.manualPressCurrentKeyDown is None:
            utils.core.manualPress('s', True)
            print('nao havia nada apertado, apertando s')
        elif utils.core.manualPressCurrentKeyDown != 's':
            print('soltando ' + utils.core.manualPressCurrentKeyDown + ' e pressionando s')
            #utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)
            utils.core.manualPress('s', True)
        else:
            print('ja esta apertando o s, nao fara nada')

    if calcX < 50 and calcY == 50:
        delaySpeed = speedBreakpoints(getPlayerSpeed(), (currentSqm[0], currentSqm[1], z1), 'a') / 1000
        lastActionTime = time()

        if utils.core.manualPressCurrentKeyDown is None:
            utils.core.manualPress('a', True)
            print('nao havia nada apertado, apertando a')
        elif utils.core.manualPressCurrentKeyDown != 'a':
            print('soltando ' + utils.core.manualPressCurrentKeyDown + ' e pressionando a')
            #utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)

            utils.core.manualPress('a', True)
        else:
            print('ja esta apertando o a, nao fara nada')


    if calcX > 50 and calcY == 50:
        delaySpeed = speedBreakpoints(getPlayerSpeed(), (currentSqm[0], currentSqm[1], z1), 'd') / 1000
        lastActionTime = time()
        if utils.core.manualPressCurrentKeyDown is None:
            utils.core.manualPress('d', True)
            print('nao havia nada apertado, apertando d')
        elif utils.core.manualPressCurrentKeyDown != 'd':
            print('soltando ' + utils.core.manualPressCurrentKeyDown + ' e pressionando d')
            #utils.core.manualPress(utils.core.manualPressCurrentKeyDown, False)

            utils.core.manualPress('d', True)
        else:
            print('ja esta apertando o d, nao fara nada')

    print('retornando False False no fim')
    return False, False


def speedBreakpoints(playerSpeed, position, direction):

    breakpointsMap = {70: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 111, 142, 200, 342, 1070],
                      90: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 120, 147, 192, 278, 499, 1842],
                      95: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 157, 205, 299, 543, 2096],
                      100: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 113, 135, 167, 219, 321, 592, 2382],
                      110: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 126, 150, 187, 248, 367, 696, 3060],
                      125: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 175, 219, 293, 444, 876, 4419],
                      140: [0, 0, 0, 0, 0, 0, 0, 111, 125, 143, 167, 201, 254, 344, 531, 1092, 6341],
                      150: [0, 0, 0, 0, 0, 0, 0, 120, 135, 155, 181, 219, 278, 380, 595, 1258, 8036],
                      160: [0, 0, 0, 0, 0, 0, 116, 129, 145, 167, 196, 238, 304, 419, 663, 1443, 10167],
                      200: [0, 0, 0, 114, 124, 135, 149, 167, 190, 219, 261, 322, 419, 597, 998, 2444, 25761],
                      250: [250, 117, 126, 135, 146, 160, 175, 195, 220, 252, 295, 356, 446, 598, 884, 1591, 4557, 81351]}

    breakpointSpeed = [850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50]

    (x1, y1, z1) = position
    level = z1
    position = (x1, y1)
    directionMap = {
        'q': (-1, -1),
        'w': ( 0, -1),
        'e': ( 1, -1),
        'a': (-1,  0),
        's': ( 0,  1),
        'd': ( 1,  0),
        'z': (-1,  1),
        'c': ( 1,  1)
    }

    pathMap = radar.config.floorsPathsSqms[z1]
    futureCoordinate = (y1 + directionMap[direction][1], x1 + directionMap[direction][0])
    futurePathValue = pathMap[futureCoordinate]
    tileBreakpoints = breakpointsMap[futurePathValue]
    for i in range(len(tileBreakpoints)):
        if playerSpeed <= tileBreakpoints[i]:
            return breakpointSpeed[i-1]


def getPlayerSpeed():
    return 364