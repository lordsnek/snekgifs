from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.set_max_djump(self.p8, 2)
    utils.load_room(self.p8, 24) # load 400m
    #utils.suppress_object(self.p8, self.p8.game.balloon) # don't consider berry block
    #utils.suppress_object(self.p8, self.p8.game.fall_floor)
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    # execute this list of initial inputs
    #for a in [18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
      #self.p8.set_btn_state(a)
      #self.p8.step()
    # alternatively, using output from a TAS tool:
    utils.place_maddy(self.p8, 99, 106, -.4, -.265, 1.4, 0.63, 0, 2)
    return self.p8.game.objects

  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      player = self.find_player(objs)
      target_y = 48
      max_spd_y = 3
      target_x = 63
      max_spd_x = 8 # arbitrary large x heuristic to avoid paring solutions that don't work; x speed is useless for this search
      return max(math.ceil(abs(player.y - target_y) / max_spd_y), math.ceil(abs(player.x-target_x)/max_spd_x))

  def is_goal(self, objs):
    p = self.find_player(objs)
    return p and p.y<49 and p.spd.y>0 #and p.djump>0 #Be at the height of the final cloud, without going far to the right

  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000010,0b000001] # r
    # if abs(player.spd.x)<.4:
     # actions.extend([0b000000])
    if can_jump:
      actions.extend([0b010000]) # r + z
    if can_dash:
      actions.extend([0b100101]) # u + x, u + l + x
    return actions

  #def exit_heuristic(self, player, exit_spd_y=3):
   #   if player.x<10:
    #    return math.inf
     # return 0

  #def is_goal(self, objs):
    #p = self.find_player(objs)
    #return p and p.y<50 #Be able to walljump on a wall at the right height.

if __name__ == '__main__':
  # search up to depth 50, but stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(32,complete=True)
