from src.repositories.gameWindow.core import getSlotFromCoordinate
from src.repositories.gameWindow.slot import rightClickSlot
from src.repositories.inventory.core import isLockerOpen
from ...typings import Context
from .baseTask import BaseTask


class OpenLockerTask(BaseTask):
    def __init__(self):
        super().__init__()
        self.delayAfterComplete = 1
        self.name = 'openLockerTask'

    # TODO: add unit tests
    def shouldIgnore(self, context: Context) -> bool:
        isOpen = isLockerOpen(context['screenshot'])
        return isOpen

    # TODO: add unit tests
    def do(self, context: Context) -> Context:
        lockerCoordinate = context['deposit']['lockerCoordinate']
        slot = getSlotFromCoordinate(context['radar']['coordinate'], lockerCoordinate)
        rightClickSlot(slot, context['gameWindow']['coordinate'])
        return context

    # TODO: add unit tests
    def did(self, context: Context) -> bool:
        didTask = isLockerOpen(context['screenshot'])
        return didTask
