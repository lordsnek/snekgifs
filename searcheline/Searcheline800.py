from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.load_room(self.p8, 7) # load 400m
    utils.suppress_object(self.p8, self.p8.game.balloon) # don't consider the balloon
    utils.suppress_object(self.p8, self.p8.game.fall_floor) # don't consider the crumbles
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    
    # using output from a TAS tool:
    utils.place_maddy(self.p8, 9, 112, -.2, 0, 0, 0, 6, 1)
    return self.p8.game.objects

  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      player = self.find_player(objs)
      target_y = 39
      max_spd_y = 3
      target_x = 92
      max_spd_x = 400000 # arbitrary large x heuristic to avoid paring solutions that don't work; x speed is useless for this search
      return max(math.ceil(abs(player.y - target_y) / max_spd_y), math.ceil(abs(player.x-target_x)/max_spd_x))

  def is_goal(self, objs):
    p = self.find_player(objs)
    return p and p.y<40 # be at the lowest height the balloon could reach

  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000000] # n
    if can_jump:
      actions.extend([0b010000]) # z
    if can_dash:
      actions.extend([0b100100]) # u + x
    return actions
    
if __name__ == '__main__':
  # search up to depth 40, but don't stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(40,complete=True)
