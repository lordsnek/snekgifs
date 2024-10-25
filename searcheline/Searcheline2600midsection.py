from Searcheline import Searcheline
import CelesteUtils as utils
import math

class Search100(Searcheline):
  # initial state to search from
  def init_state(self):
    utils.set_max_djump(self.p8, 2)
    utils.load_room(self.p8, 25) # load 400m
    #utils.suppress_object(self.p8, self.p8.game.balloon) # don't consider berry block
    #utils.suppress_object(self.p8, self.p8.game.chest)
    utils.skip_player_spawn(self.p8) # skip to after player has spawned
    # execute this list of initial inputs
    #for a in [18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
      #self.p8.set_btn_state(a)
      #self.p8.step()
    # alternatively, using output from a TAS tool:
    utils.place_maddy(self.p8, 64, 80, 0.2, 0.495, -0.8, -0.87, 0, 0)
    return self.p8.game.objects

  def h_cost(self, objs):
    if self.is_rip(objs):
      return math.inf
    else:
      player = self.find_player(objs)
      target_y = 16
      max_spd_y = 3
      target_x = 43
      max_spd_x = 3000000 # arbitrary large x heuristic to avoid paring solutions that don't work; x speed is useless for this search
      return max(math.ceil(abs(player.y - target_y) / max_spd_y), math.ceil(abs(player.x-target_x)/max_spd_x))

  def is_goal(self, objs):
    p = self.find_player(objs)
    return p and ((p.y==16 and p.spd.y+p.rem.y>-.5) and p.y<25 and p.x>35) #and p.djump>0 #Be at the height of the final cloud, without going far to the right

  # get list of available inputs for a state - only consider {r, r + z, u + r + x}
  def allowable_actions(self, objs, player, h_movement, can_jump, can_dash):
    actions = [0b000001] # r
      #actions.extend([0b000000])
    if can_jump:
      actions.extend([0b010001]) # r + z
    if can_dash:
      actions.extend([0b101001,0b100001,0b100100,0b100110]) # u + x, u + l + x
    return actions

  #def exit_heuristic(self, player, e xit_spd_y=3):
   #   if player.x<10:
    #    return math.inf
     # return 0

  #def is_goal(self, objs):
    #p = self.find_player(objs)
    #return p and p.y<50 #Be able to walljump on a wall at the right height.

if __name__ == '__main__':
  # search up to depth 50, but stop at the depth of the first solution found
  s = Search100()
  solutions = s.search(52,complete=True)
