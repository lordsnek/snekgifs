from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.set_max_djump(self.p8, 2)
    utils.load_room(self.p8, 23) # load 400m
    #utils.suppress_object(self.p8, self.p8.game.balloon) # don't consider berry block
    #utils.suppress_object(self.p8, self.p8.game.fall_floor)
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    # execute this list of initial inputs
    #for a in [18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
      #self.p8.set_btn_state(a)
      #self.p8.step()
    # alternatively, using output from a TAS tool:
    #utils.place_maddy(self.p8, 9, 112, -.2, 0, 0, 0, 6, 2)
    return self.p8.game.objects

  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      player = self.find_player(objs)
      target_y = 52
      max_spd_y = 5
      target_x = 71
      max_spd_x = 5 # arbitrary large x heuristic to avoid paring solutions that don't work; x speed is useless for this search
      return max(math.ceil(abs(player.y - target_y) / max_spd_y), math.ceil(abs(player.x-target_x)/max_spd_x))

  def is_goal(self, objs):
    p = self.find_player(objs)
    return p and p.x>65 and p.spd.y==-2 #and p.djump>0 #Be at the height of the final cloud, without going far to the right

  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000010] # r
    if h_movement and player.x>46 and player.x<50:
     actions.extend([0])
    if h_movement and player.x==8 and player.rem.x==0:
     actions.extend([1])
      #actions.extend([0b000000])
    if can_jump:
      actions.extend([0b010010]) # r + z
    if can_dash:
      actions.extend([0b100010,0b100100,0b100110,0b101010,0b100101]) # u + x, u + l + x
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
  solutions = s.search(35,complete=True)
