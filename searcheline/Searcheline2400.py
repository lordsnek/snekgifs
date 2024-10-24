from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.set_max_djump(self.p8, 2)
    utils.load_room(self.p8, 23) # load 2400m
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    return self.p8.game.objects

  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      player = self.find_player(objs)
      target_y = 52
      max_spd_y = 5
      target_x = 71
      max_spd_x = 5
      return max(math.ceil(abs(player.y - target_y) / max_spd_y), math.ceil(abs(player.x-target_x)/max_spd_x))

  def is_goal(self, objs):
    p = self.find_player(objs)
    return p and p.x>65 and p.spd.y==-2 # Cornerjump on the ice

  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000010] # r
    if h_movement and player.x>46 and player.x<50:
     actions.extend([0]) # n
    if h_movement and player.x==8 and player.rem.x==0:
     actions.extend([1]) # l
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b100010,0b100100,0b100110,0b101010,0b100000]) # u + x, u + l + x
    return actions

if __name__ == '__main__':
  # search up to depth 35, and don't stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(35,complete=True)
