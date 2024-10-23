from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.load_room(self.p8, 6) # load 700m
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    return self.p8.game.objects

  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      player = self.find_player(objs)
      target_y = 32
      max_spd_y = 4
      target_x = 0
      max_spd_x =1000 # arbitrary large x heuristic to avoid paring solutions that don't work; x speed is useless for this search
      return max(math.ceil(abs(player.y - target_y) / max_spd_y), math.ceil(abs(player.x-target_x)/max_spd_x))

  def is_goal(self, objs):
    p = self.find_player(objs)
    return p and p.y==32 and p.x<53 #Be at the height of the final cloud, without going far to the right
  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions=[]
    if h_movement:
      actions.extend([0b000000]) # n
      if player.y>100:
        actions.extend([0b000010]) # r
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b100100, 0b100110]) # u + x, u + r + x
    return actions

if __name__ == '__main__':
  # search up to depth 50, but stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(100,complete=True)
