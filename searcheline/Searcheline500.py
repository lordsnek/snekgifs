from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.load_room(self.p8, 4) # load 500m
    utils.suppress_object(self.p8, self.p8.game.key) # don't consider key
    utils.suppress_object(self.p8, self.p8.game.chest) # don't consider chest
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    utils.place_maddy(self.p8, 41, 48, 0.4, -.001, .8, -.45, 0, 0) # go to the frame before Madeline clips
    return self.p8.game.objects

  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions=[]
    if h_movement:
      actions.extend([0b000001]) # l
      if player.y>28:
        actions.extend([0b000010]) # r
      else:
        if player.x>46:
          actions.extend([0b000000]) # n
    if can_jump:
      actions.extend([0b010010]) # r + z
      actions.extend([0b010001]) # l + z
    if can_dash:
      actions.extend([0b100100, 0b100101]) # u + x, u + l + x
    return actions

  def exit_heuristic(self, player, exit_spd_y=3):
    if player.x>55:
      return math.inf
    if player.x<44 and player.y>28 and player.y<42:
      return math.inf
    return math.ceil((player.y + 4) / exit_spd_y)

if __name__ == '__main__':
  # search up to depth 50, but stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(30,complete=True)
