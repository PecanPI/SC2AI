import random
import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer, Human
from sc2.ids.unit_typeid import UnitTypeId
from sc2.constants import *


class PecanPiBot(sc2.BotAI):
    async def on_step(self, iteration):
        larva = self.units(UnitTypeId.LARVA)
        drone = self.units(UnitTypeId.DRONE)
        droneCount = self.state.units.amount
        overlords = self.units(UnitTypeId.OVERLORD)
        zergling = self.units(UnitTypeId.ZERGLING)

        await self.distribute_workers()
        await self.buildWorkers()
        await self.buildOverlords()
        await self.buildZerglings()
        await self.buildSpawnPool()

    async def buildWorkers(self):

        if self.can_afford(UnitTypeId.DRONE) and self.supply_left >= 1 and self.units(UnitTypeId.SPAWNINGPOOL)\
                and self.units(UnitTypeId.LARVA).exists and self.units(UnitTypeId.DRONE).amount < 14:
            await self.do(self.units(UnitTypeId.LARVA).random.train(UnitTypeId.DRONE))

    async def buildOverlords(self):
        if self.supply_left <= 2:
            if self.units(UnitTypeId.DRONE).amount == 14 and self.can_afford(UnitTypeId.OVERLORD) \
                    and self.units(UnitTypeId.LARVA).exists and not self.already_pending(UnitTypeId.OVERLORD):
                await self.do(self.units(UnitTypeId.LARVA).random.train(UnitTypeId.OVERLORD))

    async def buildSpawnPool(self):
        if self.can_afford(UnitTypeId.SPAWNINGPOOL) and not self.already_pending(UnitTypeId.SPAWNINGPOOL)\
                and not self.units(UnitTypeId.SPAWNINGPOOL).exists :
            hatcheries = self.units(UnitTypeId.HATCHERY).ready
            await self.build(UnitTypeId.SPAWNINGPOOL, near=hatcheries.first)

    async def buildZerglings(self):
        if self.can_afford(UnitTypeId.ZERGLING) and self.units(UnitTypeId.LARVA).amount > 0\
                and not self.already_pending(UnitTypeId.SPAWNINGPOOL):
            #if self.already_pending(UnitTypeId.SPAWNINGPOOL) and self.units(UnitTypeId.SPAWNINGPOOL).exists \
            if 14 <= self.supply_used < 17:
                await self.do(self.units(UnitTypeId.LARVA).random.train(UnitTypeId.ZERGLING))


run_game(maps.get("KingsCoveLE"), [
    Bot(Race.Zerg, PecanPiBot(), 'PecanPiBot'),
    Computer(Race.Terran, Difficulty.Easy)
    #Human(Race.Zerg,'Matt'),
    #Bot(Race.Zerg, PecanPiBot(), 'PecanPiBot')
], realtime=True)
