from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.set_max_djump(self.p8, 2)
    utils.load_room(self.p8, 27) # load 2600m
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    utils.place_maddy(self.p8, 43, 109, -0.200012, -0.435104, 1, 2, 0, 0)
    return self.p8.game.objects

  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      player = self.find_player(objs)
      target_y = 100
      max_spd_y = 5
      target_x = 95
      max_spd_x = 5
      return max(math.ceil(abs(player.y - target_y) / max_spd_y), math.ceil(abs(player.x-target_x)/max_spd_x))

  def is_goal(self, objs):
     p = self.find_player(objs)
     return p and p.x>94 and p.y<101 #and p.spd.x==2 and p.spd.y==-2 # be at the right height to clip on the first block


  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    #jank=False #sorry
    actions = [0b000010] # r
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b101010,0b100010,0b100110]) # d + u + x, r + x, u + x
    if player.x<48:
      actions.extend([0b000000])
    return actions

if __name__ == '__main__':
  # search up to depth 40, and don't stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(42,complete=True)
