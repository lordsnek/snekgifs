from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.load_room(self.p8, 8) # load 900m
    utils.suppress_object(self.p8, self.p8.game.balloon) # don't consider balloons
    utils.suppress_object(self.p8, self.p8.game.fake_wall) # don't consider berry block
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    return self.p8.game.objects

  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      player = self.find_player(objs)
      target_y = 32
      max_spd_y = 10000 # arbitrary large y heuristic to avoid paring solutions that don't work; y speed is useless for this search
      target_x = 92
      max_spd_x = 4 
      return max(math.ceil(abs(player.y - target_y) / max_spd_y), math.ceil(abs(player.x-target_x)/max_spd_x))

  def is_goal(self, objs):
    p = self.find_player(objs)
    return p and (p.spd.y<-2.78 and p.spd.y>-2.8) # Be in a position such that you recently hit a spring
  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    if h_movement:
     actions = [0b000010] # r
    else:
      actions = ([0b000000]) # n
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b100010, 0b100110, 0b101010]) # r + x, u + l + x, u + d + x
    return actions

if __name__ == '__main__':
  # search up to depth 31, and don't stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(31,complete=True)
