import minescript as m
import bot.core.minescript_extra as m_extra

import bot.core.decision as decision
import bot.core.movement as move
import bot.core.mining as mining
from bot.core import player

import bot.modes.descend as descend


def run():
    player.auto_tracking = True
    descend.run()
    player._restart = True
    
    while (not player.stop_tracking):
        result = decision.findReachableCluster()

        if (not result):
            m.echo(f"{m_extra.txt_clr('y')}No reachable clusters found")
            break

        path, cluster = result

        move.goToTarget(path, cluster['center'])
        mining.mineCluster(cluster['coords'])
        move.finalizeDescent()



if __name__ == "__main__":
    run()
    