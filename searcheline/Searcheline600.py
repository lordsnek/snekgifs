from Searcheline import Searcheline
import CelesteUtils as utils

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.load_room(self.p8, 5) # load 600m
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    return self.p8.game.objects

  # get list of available inputs for a state - only consider {r, r + z, u + r + x, r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000010] # r
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b100010, 0b100110]) # r + x, u + r + x
    return actions

if __name__ == '__main__':
  # search up to depth 50, but stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(50)
