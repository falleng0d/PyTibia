from src.features.gameWindow.core import getSlotFromCoordinate
from src.features.gameWindow.slot import rightClickSlot
from .baseTask import BaseTask


class UseHoleTask(BaseTask):
    def __init__(self, value):
        super().__init__()
        self.delayBeforeStart = 2
        self.delayAfterComplete = 2
        self.name = 'useHole'
        self.value = value

    def do(self, context):
        slot = getSlotFromCoordinate(
            context['radar']['coordinate'], self.value['coordinate'])
        rightClickSlot(slot, context['gameWindow']['coordinate'])
        return context
    