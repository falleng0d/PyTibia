import numpy as np
from src.repositories.battleList.typings import Creature as BattleListCreature
from src.repositories.gameWindow.typings import Creature as GameWindowCreature
from src.repositories.radar.typings import Coordinate, Waypoint


gameContext = {
    'backpacks': {
        'main': 'brocade backpack',
        'gold': 'crystal backpack',
        'loot': 'beach backpack',
    },
    'battleList': {
        'beingAttackedCreatureCategory': None,
        'creatures': np.array([], dtype=BattleListCreature),
    },
    'cavebot': {
        'enabled': True,
        'holesOrStairs': np.array([], dtype=Coordinate),
        'isAttackingSomeCreature': False,
        'previousTargetCreature': None,
        'targetCreature': None,
        'waypoints': {
            'currentIndex': None,
            'points': np.array([
                # werehyaena cave 1
                ('', 'logout', (33214, 32458, 8), {}),
                ('', 'walk', (33214, 32458, 8), {}),
                ('', 'moveUpNorth', (33214, 32456, 8), {}),
                ('', 'walk', (33217, 32441, 7), {}),
                ('endOfCity', 'walk', (33215, 32406, 7), {}),
                ('', 'walk', (33218, 32377, 7), {}),
                ('', 'walk', (33212, 32359, 7), {}),
                ('', 'useShovel', (33212, 32358, 7), {}),
                ('', 'walk', (33227, 32358, 8), {}),
                ('', 'moveDownEast', (33227, 32358, 8), {}),
                ('', 'walk', (33222, 32355, 9), {}), # 10
                ('', 'moveDownNorth', (33222, 32355, 9), {}), 
                ('caveStart', 'walk', (33207, 32353, 10), {}),
                ('', 'walk', (33189, 32348, 10), {}),
                ('', 'walk', (33193, 32366, 10), {}),
                ('', 'walk', (33208, 32367, 10), {}),
                ('', 'walk', (33223, 32387, 10), {}),
                ('', 'walk', (33200, 32389, 10), {}),
                ('', 'walk', (33196, 32398, 10), {}),
                ('', 'walk', (33210, 32373, 10), {}),
                ('', 'walk', (33221, 32351, 10), {}), # 20
                ('', 'dropFlasks', (33306, 32289, 7), {}),
                ('', 'refillChecker', (33306, 32289, 7), { # 22
                    'minimumOfManaPotions': 200,
                    'minimumOfHealthPotions': 200,
                    'minimumOfCapacity': 500,
                    'waypointLabelToRedirect': 'caveStart',
                }),
                ('', 'walk', (33221, 32353, 10), {}),
                ('', 'moveUpSouth', (33221, 32353, 10), {}),
                ('', 'walk', (33229, 32358, 9), {}),
                ('', 'moveUpWest', (33229, 32358, 9), {}),
                ('', 'walk', (33212, 32358, 8), {}),
                ('', 'useRope', (33212, 32358, 8), {}),
                ('', 'walk', (33220, 32378, 7), {}),
                ('', 'walk', (33221, 32387, 7), {}), # 30
                ('', 'depositGold', (33221, 32387, 7), {}),
                ('', 'walk', (33215, 32422, 7), {}),
                ('', 'walk', (33213, 32454, 7), {}),
                ('', 'moveDownSouth', (33213, 32454, 7), {}),
                ('', 'depositItems', (33214, 32456, 8), {'city': 'Darashia'}),
                ('', 'walk', (33214, 32456, 8), {}),
                ('', 'moveUpNorth', (33214, 32456, 8), {}),
                ('', 'walk', (33217, 32403, 7), {}),
                ('', 'refill', (33306, 32289, 7), {
                    'waypointLabelToRedirect': 'endOfCity'
                }),
                
                # damselfly
                # ('', 'walk', (32883, 32044, 10), {}),
                # ('', 'walk', (32909, 32045, 10), {}),
                # ('', 'walk', (32910, 32027, 10), {}),
                # ('', 'walk', (32884, 32026, 10), {}),
                # ('', 'walk', (32906, 32009, 10), {}),
                # ('', 'walk', (32883, 32009, 10), {}),
                # ('', 'walk', (32857, 32009, 10), {}),
                # ('', 'walk', (32856, 32027, 10), {}),
                # ('', 'walk', (32870, 32036, 10), {}),
                # ('', 'walk', (32856, 32045, 10), {}),
            ], dtype=Waypoint),
            'state': None
        },
    },
    'chat': {
        'tabs': {}
    },
    'comingFromDirection': None,
    'comboSpells': {
        'enabled': True,
        'lastUsedSpell': None,
        'items': [
            {
                'enabled': True,
                'name': '3 ou -',
                'creatures': {
                    'compare': 'lessThan',
                    'value': 4
                },
                'currentSpellIndex': 0,
                'spells': [
                    {'name': 'exori', 'hotkey': 'f4', 'metadata': {'mana': 115}},
                    {'name': 'exori gran', 'hotkey': 'f5', 'metadata': {'mana': 340}},
                    {'name': 'exori', 'hotkey': 'f4', 'metadata': {'mana': 115}},
                    {'name': 'exori min', 'hotkey': 'f7', 'metadata': {'mana': 200}},
                    {'name': 'exori', 'hotkey': 'f4', 'metadata': {'mana': 115}},
                    {'name': 'exori gran', 'hotkey': 'f5', 'metadata': {'mana': 340}},
                ],
            },
            {
                'enabled': True,
                'name': '4 ou +',
                'creatures': {
                    'compare': 'greaterThanOrEqual',
                    'value': 4
                },
                'currentSpellIndex': 0,
                'spells': [
                    {'name': 'exori gran', 'hotkey': 'f5', 'metadata': {'mana': 340}},
                    {'name': 'exori mas', 'hotkey': 'f6', 'metadata': {'mana': 160}},
                    {'name': 'exori', 'hotkey': 'f4', 'metadata': {'mana': 115}},
                    {'name': 'exori gran', 'hotkey': 'f5', 'metadata': {'mana': 340}},
                    {'name': 'exori mas', 'hotkey': 'f6', 'metadata': {'mana': 160}},
                ],
            }
        ],
    },
    'currentTask': None,
    'deposit': {
        'lockerCoordinate': None
    },
    'currentPotionHealing': None,
    'currentSpellHealing': None,
    'gameWindow': {
        'coordinate': None,
        'img': None,
        'previousGameWindowImage': None,
        'walkedPixelsInSqm': 0,
        'previousMonsters': np.array([], dtype=GameWindowCreature),
        'monsters': np.array([], dtype=GameWindowCreature),
        'players': np.array([], dtype=GameWindowCreature),
    },
    'healing': {
        'enabled': True,
        'highPriority': {
            'healthFood': {
                'enabled': False,
                'hotkey': None,
                'hpPercentageLessThanOrEqual': None,
            },
            'manaFood': {
                'enabled': False,
                'hotkey': None,
                'manaPercentageLessThanOrEqual': None,
            },
            'ssa': {
                'enabled': False,
                'hotkey': None,
                'hpPercentageLessThanOrEqual': None,
                'hpPercentageGreaterThanOrEqual': None,
            }
        },
        'potions': {
            'firstHealthPotion': {
                'enabled': True,
                'hotkey': '1',
                'hpPercentageLessThanOrEqual': 50,
                'manaPercentageGreaterThanOrEqual': None,
            },
            'secondHealthPotion': {
                'enabled': False,
                'hotkey': '2',
                'hpPercentageLessThanOrEqual': 70,
                'manaPercentageGreaterThanOrEqual': None,
            },
            'thirdHealthPotion': {
                'enabled': False,
                'hotkey': '1',
                'hpPercentageLessThanOrEqual': 80,
                'manaPercentageGreaterThanOrEqual': None,
            },
            'firstManaPotion': {
                'enabled': True,
                'hotkey': '2',
                'manaPercentageLessThanOrEqual': 80,
            },
            'secondManaPotion': {
                'enabled': False,
                'hotkey': '2',
                'manaPercentageLessThanOrEqual': 90,
            },
            'thirdManaPotion': {
                'enabled': False,
                'hotkey': '2',
                'manaPercentageLessThanOrEqual': 90,
            },
        },
        'spells': {
            'criticalHealing': {
                'enabled': False,
                'hotkey': 'f3',
                'hpPercentageLessThanOrEqual': 90,
                'spell': {
                    'name': 'exura med ico',
                    'manaNeeded': 90,
                    'cooldownInSeconds': 1
                }
            },
            'lightHealing': {
                'enabled': False,
                'hotkey': 'f3',
                'hpPercentageLessThanOrEqual': 90,
                'spell': {
                    'name': 'exura med ico',
                    'manaNeeded': 90,
                    'cooldownInSeconds': 1
                }
            },
            'utura': {
                'enabled': False,
                'hotkey': '3',
                'spell': {
                    'name': 'utura',
                    'manaNeeded': 40,
                    'cooldownInSeconds': 1
                }
            },
            'exuraGranIco': {
                'enabled': False,
                'hotkey': 'f12',
                'hpPercentageLessThanOrEqual': 60,
                'manaPercentageGreaterThanOrEqual': 5,
                'spell': {
                    'name': 'exura gran ico',
                    'manaNeeded': 200,
                    'cooldownInSeconds': 600
                }
            },
        },
        'eatFood': {
            'enabled': True,
            'hotkey': '5',
            'eatWhenFoodIslessOrEqual': 5,
        }
    },
    'hotkeys': {
        'healthPotion': 'f1',
        'manaPotion': 'f2',
        'eatFood': 'f7',
        'rope': 'f8',
        'shovel': 'f9',
    },
    'hotkeysV2': {
        'f1': 'ultimate health potion',
        'f2': 'strong mana potion',
        'f3': 'exura med ico',
        'f12': 'stone skin amulet'
    },
    'loot': {
        'corpsesToLoot': np.array([], dtype=GameWindowCreature),
    },
    'lastPressedKey': None,
    'pause': True,
    'radar': {
        'coordinate': None,
        'previousCoordinate': None,
        'lastCoordinateVisited': None,
    },
    'refill': {
        'enabled': True,
        'health': {
            'item': 'supreme health potion',
            'quantity': 300,
        },
        'mana': {
            'item': 'strong mana potion',
            'quantity': 500,
        },
    },
    'resolution': 1080,
    'statusBar': {
        'hpPercentage': None,
        'hp': None,
        'manaPercentage': None,
        'mana': None,
    },
    'targeting': {
        'enabled': False,
        'creatures': {},
        'canIgnoreCreatures': True,
        'hasIgnorableCreatures' : False,
    },
    'screenshot': None,
    'way': None,
    'window': None
}
