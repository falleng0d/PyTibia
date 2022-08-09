import numpy as np
import cv2
from time import sleep, time
import actionBar.slot
import battleList.core
from chat import chat
import hud.core
import hud.creatures
import radar.config
import radar.core
import utils.core
import utils.image
import utils.window
import utils.window
import dxcam
import timeit


def main():
    loop_time = time()
    window = utils.window.getWindow()
    screenshot = utils.image.RGBtoGray(utils.core.getScreenshot())
    screenshot = np.array(screenshot, dtype=np.uint8)
    radarCoordinate = radar.core.getCoordinate(screenshot)
    battleListCreatures = battleList.core.getCreatures(screenshot)
    # camera = dxcam.create(output_color='GRAY')
    hudCoordinate = hud.core.getCoordinate(screenshot)
    hudImg = hud.core.getImgByCoordinate(screenshot, hudCoordinate)
    creaturesBars = hud.creatures.getCreaturesBars(hudImg.flatten())
    bugHash = utils.image.loadAsArray('hud/images/monsters/Bug.png')
    cyclopsHash = utils.image.loadAsArray('hud/images/monsters/Cyclops.png')
    dragonHash = utils.image.loadAsArray('hud/images/monsters/Dragon.png')
    demonHash = utils.image.loadAsArray('hud/images/monsters/Demon.png')
    ratHash = utils.image.loadAsArray('hud/images/monsters/Dragon.png')
    while True:
        # frame = camera.grab()
        # print(creaturesBars)
        # start_time = time()
        # creaturesBars = hud.creatures.getCreaturesBars(hudImg)
        hud.creatures.getCreatures_perf(
            creaturesBars, hudImg, bugHash, cyclopsHash, demonHash, dragonHash, ratHash)
        # hudCreatures = hud.creatures.getCreatures(
        #     screenshot, battleListCreatures, radarCoordinate=radarCoordinate)
        # print(res)
        # break
        timef = (time() - loop_time)
        timef = timef if timef else 1
        fps = 1 / timef
        print('FPS {}'.format(fps))
        loop_time = time()
        # print("%s" % (time() - start_time))


if __name__ == '__main__':
    main()
