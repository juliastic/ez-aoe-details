from enum import Enum

class Action(Enum):
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)

class Unit(Action):
    VILLAGER = 'Villager'

    ARCHER = 'Archer'
    SKIRMISHER = 'Skirmisher'
    CAVALRY_ARCHER = 'Cavalry Archery'

    KNIGHT = 'Knight'
    SCOUT = 'Scout'
    CAMEL = 'Camel'
    BATTLE_ELEPHANT = 'Battle Elephant'

    EAGLE = 'Eagle'
    MILITIA = 'Militia'
    SPEARMAN = 'Spearman'

    MONK = 'Monk'

    MANGONEL = 'Mangonel'
    ORGAN_GUN = 'Organ Gun'
    BATTERING_RAM = 'Battering Ram'
    TREBUCHET = 'Trebuchet'

class Building(Action):
    DOCK = 'Dock'
    MILL = 'Mill'
    MARKET = 'Market'
    TOWN_CENTER = 'Town Center'

    ARCHERY = 'Archery'
    STABLE = 'Stable'
    BARRACKS = 'Barracks'
    SIEGE_WORKSHOP = 'Siege Workshop'
    CASTLE = 'Castle'
    BLACKSMITH = 'Blacksmith'
    MONASTERY = 'Monastery'

    WATCH_TOWER = 'Watch Tower'

#todo: dock and unique units ... and unique techs and university techs etc
class Technology(Action):
    # TC Technologies
    FEUDAL_AGE = 'Feudal Age'
    CASTLE_AGE = 'Castle Age'
    IMPERIAL_AGE = 'Imperial Age'

    LOOM = 'Loom'
    TOWN_WATCH = 'Town Watch'
    TOWN_PATROL = 'Town Patrol'
    WHEELBARROW = 'Wheelbarrow'
    HAND_CART = 'Hand Cart'

    # Mill Technologies
    HORSE_COLLAR = 'Horse Collar'
    HEAVY_PLOW = 'Heavy Plow'

    # Lumber Camp Technologies
    DOUBLE_BIT_AXE = 'Double Bit Axe'
    BOW_SAW = 'Bow Saw'

    # Mining Camp Technologies
    GOLD_MINING = 'Gold Mining'
    GOLD_SHAFT_MINING = 'Gold Shaft Mining'
    STONE_MINING = 'Stone Mining'
    STONE_SHAFT_MINING = 'Stone Shaft Mining'

    # Blacksmith Technologies
    FORGING = 'Forging'
    IRON_CASTING = 'Iron Casting'
    BLAST_FURNANCE = 'Blast Furnace'
    FLETCHING = 'Fletching'
    BODKIN_ARROW = 'Bodkin Arrow'
    BRACER = 'Bracer'

    SCALE_MAIL_ARMOR = 'Scale Mail Armor'
    CHAIN_MAIL_ARMOR = 'Chain Mail Armor'
    PLATE_MAIL_ARMOR = 'Plate Mail Armor'
    SCALE_BARDING_ARMOR = 'Scale Barding Armor'
    CHAIN_BARDING_ARMOR = 'Chain Barding Armor'
    PLATE_BARDING_ARMOR = 'Plate Barding Armor'
    PADDED_ARCHER_ARMOR = 'Padded Archer Armor'
    LEATHER_ARCHER_ARMOR = 'Leather Archer Armor'
    RING_ARCHER_ARMOR = 'Ring Archer Armor'

    # Archery Technologies
    THUMB_RING = 'Thumb Ring'
    PARTHIAN_TACTICS = 'Parthian Tactics'

    CROSSBOWMAN = 'Crossbowman'
    ARBALESTER = 'Arbalester'
    ELITE_SKIRMISHER = 'Elite Skirmisher'
    IMPERIAL_SKIRMISHER = 'Imperial Skirmisher'
    HEAVY_CAVALARY_ARCHER = 'Heavy Cavalry Archer'

    # University Technologies
    BALLISTICS = 'Ballistics'

    # Barrack Technologies
    ARSON = 'Arson'
    SUPPLIES = 'Supplies'
    SQUIRES = 'Squires'

    PIKEMEN = 'Pikemen'
    HALBERDIER = 'Halberdier'
    MAN_AT_ARMS = 'Man-at-Arms'
    LONGSWORD = 'Longsword'
    TWO_HANDED_SWORDSMAN = 'Two-Handed Swordsman'
    CHAMPION = 'Champion'
    EAGLE_WARRIOR = 'Eagle Warrior'
    ELITE_EAGLE_WARRIOR = 'Elite Eagle Warrior'

    # Stable Technologies
    BLOODLINES = 'Bloodlines'
    HUSBANDRY = 'Husbandry'

    LIGHT_CAVALARY = 'Light Cavalary'
    HUSSAR = 'Hussar'
    CAVALIER = 'Cavalier'
    PALADIN = 'Paladin'
    HEAVY_CAMEL = 'Heavy Camel'
    IMPERIAL_CAMEL = 'Imperial Camel'
    ELITE_BATTLE_ELEPHANT = 'Elite Battle Elephant'

class MainType(Action):
    ECO = 'Economy'
    MIL = 'Military'

class UnitType(Action):
    INF = 'Infantry'
    CAV = 'Cavalary'
    ARCH = 'Archer'
    MONK = 'Monk'
    SIEGE = 'Siege'

class Filter():
    NONE = 0
    AVG_VIL = 1
    AVG_MIL = 2
    TECHNOLOGIES = 3
    AVG_MIL_BUILDINGS = 4
    AVG_ECO_BUILDINGS = 5
    EAPM = 6

class FilterType():
    BUILDINGS = 'buildings'
    UNITS = 'units'
    EAPM = 'eapm'
    TECHNOLOGIES = 'technologies'
    GAMEDURATION = 'gameduration'
    ACTION_COORDINATES = 'action_coordinates'
class SkillLevel():
    PRO = 'pro' # ELO > 2200
    HIGH = 'high' # ELO > 1800
    MIDDLE = 'middle' # ELO > 1000
    LOW = 'low' # ELO <= 1000

UNIT_IDS = {
    MainType.ECO: {
        83: Unit.VILLAGER
    },
    UnitType.INF: {
        74: Unit.MILITIA,
        93: Unit.SPEARMAN,
        751: Unit.EAGLE,
    },  
    UnitType.CAV: {
        38: Unit.KNIGHT,
        448: Unit.SCOUT,
        329: Unit.CAMEL,
        1132: Unit.BATTLE_ELEPHANT,
    },
    UnitType.ARCH: {
        4: Unit.ARCHER,
        7: Unit.SKIRMISHER,
        39: Unit.CAVALRY_ARCHER,
    },
    UnitType.MONK: {
        125: Unit.MONK,
    },
    UnitType.SIEGE: {
        280: Unit.MANGONEL,
        1001: Unit.ORGAN_GUN,
        1258: Unit.BATTERING_RAM,
        42: Unit.TREBUCHET,
    }
}

BUILDING_IDS = {
    MainType.ECO: {
        51: Building.DOCK,
        68: Building.MILL,
        84: Building.MARKET,
        109: Building.TOWN_CENTER,
    },
    MainType.MIL: {
        10: Building.ARCHERY,
        12: Building.BARRACKS,
        49: Building.SIEGE_WORKSHOP,
        82: Building.CASTLE,
        101: Building.STABLE,
        79: Building.WATCH_TOWER,
        104: Building.MONASTERY,
    }
}

TECHNOLOGY_IDS = {
    MainType.ECO: {
        # TC Technologies
        101: Technology.FEUDAL_AGE,
        102: Technology.CASTLE_AGE,
        103: Technology.IMPERIAL_AGE,

        8: Technology.TOWN_WATCH,
        280: Technology.TOWN_PATROL,
        22: Technology.LOOM,
        213: Technology.WHEELBARROW,
        249: Technology.HAND_CART,

        14: Technology.HORSE_COLLAR,
        13: Technology.HEAVY_PLOW,

        # Lumber Camp Technologies
        202: Technology.DOUBLE_BIT_AXE,
        203: Technology.BOW_SAW,

        # Mining Camp Technologies
        55: Technology.GOLD_MINING,
        182: Technology.GOLD_SHAFT_MINING,
        278: Technology.STONE_MINING,
        279: Technology.STONE_SHAFT_MINING,
    },
    MainType.MIL: {
        # Blacksmith Technologies
        67: Technology.FORGING,
        68: Technology.IRON_CASTING,
        75: Technology.BLAST_FURNANCE,
        199: Technology.FLETCHING,
        200: Technology.BODKIN_ARROW,
        201: Technology.BRACER,

        74: Technology.SCALE_MAIL_ARMOR,
        76: Technology.CHAIN_MAIL_ARMOR,
        77: Technology.PLATE_MAIL_ARMOR,
        80: Technology.PLATE_BARDING_ARMOR,
        81: Technology.SCALE_BARDING_ARMOR,
        82: Technology.CHAIN_BARDING_ARMOR,
        211: Technology.PADDED_ARCHER_ARMOR,
        212: Technology.LEATHER_ARCHER_ARMOR,
        219: Technology.RING_ARCHER_ARMOR,

        # Archery Technologies
        437: Technology.THUMB_RING,
        436: Technology.PARTHIAN_TACTICS,

        100: Technology.CROSSBOWMAN,
        237: Technology.ARBALESTER,
        98: Technology.ELITE_SKIRMISHER,
        655: Technology.IMPERIAL_SKIRMISHER,
        218: Technology.HEAVY_CAVALARY_ARCHER,

        # University Technologies
        93: Technology.BALLISTICS,

        # Barrack Technologies
        602: Technology.ARSON,
        716: Technology.SUPPLIES,
        215: Technology.SQUIRES,

        197: Technology.PIKEMEN,
        429: Technology.HALBERDIER,
        222: Technology.MAN_AT_ARMS,
        207: Technology.LONGSWORD,
        217: Technology.TWO_HANDED_SWORDSMAN,
        264: Technology.CHAMPION,
        384: Technology.EAGLE_WARRIOR,
        434: Technology.ELITE_EAGLE_WARRIOR,

        # Stable Technologies
        39: Technology.HUSBANDRY,
        435: Technology.BLOODLINES,

        209: Technology.CAVALIER,
        265: Technology.PALADIN,
        254: Technology.LIGHT_CAVALARY,
        428: Technology.HUSSAR,
        236: Technology.HEAVY_CAMEL,
        521: Technology.IMPERIAL_CAMEL,
        631: Technology.ELITE_BATTLE_ELEPHANT,
    }
}