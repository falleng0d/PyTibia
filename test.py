from time import sleep, time
import radar.config
import radar.core
import utils.core
import utils.image
import utils.window
import utils.window
import radar.waypoint
import keyboard


def main():
    # window = utils.window.getWindow()
    # beingAttackedCreature = None
    # corpsesToLoot = np.array([], dtype=hud.creatures.creatureType)
    screenshot = utils.image.RGBtoGray(utils.core.getScreenshot())
    (xOld, yOld, zOld) = radar.core.getCoordinate(screenshot)
    radarCoordinate = radar.core.getCoordinate(screenshot)

    while True:
        screenshot = utils.image.RGBtoGray(utils.core.getScreenshot())
        (x, y, z) = radar.core.getCoordinate(screenshot, previousCoordinate=(xOld, yOld, zOld))

        #x1c, y1c = utils.core.getPixelFromCoordinate((x, y, z))
        #a = radar.waypoint.speedBreakpoints(364, (x1c, y1c, z), 'a')
        radar.waypoint.arrowKeysWalk(screenshot, (x, y, z), (32331, 31810, 7))

    # radarCoordinate = radar.core.getCoordinate(screenshot)
    # battleListCreatures = battleList.core.getCreatures(screenshot)
    # print(battleListCreatures)
    # hudCoordinate = hud.core.getCoordinate(screenshot)
    # hudImg = hud.core.getImgByCoordinate(screenshot, hudCoordinate)
    # creaturesBars = hud.creatures.getCreaturesBars(hudImg.flatten())
    # res = timeit.repeat(lambda: battleList.core.getCreatures(
    #     screenshot), repeat=10, number=1)
    # a = new_panel.array([
    #     [1, 2, 3, 4, 5],
    #     [6, 7, 8, 9, 10]
    # ])
    # r = np.take(a, [[0, 1, 2], [5, 6, 7]])
    # print(r)
    # while True:
    # loop_time = time()
    # hudCreatures = hud.creatures.getCreatures(
    #     screenshot, battleListCreatures, radarCoordinate=radarCoordinate)
    # # print(hudCreatures)
    # res = battleList.core.isAttackingSomeCreature(battleListCreatures)
    # print(res)
    # battleListCreatures = battleList.core.getCreatures(screenshot)
    # break
    # timef = (time() - loop_time)
    # timef = timef if timef else 1
    # fps = 1 / timef
    # print('FPS {}'.format(fps))


if __name__ == '__main__':
    main()
