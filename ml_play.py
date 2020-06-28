class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        self.c=0
        self.h1=self.h2=self.h3=self.h4=self.h5=2000
        pass
        
    

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |  2 |    |    |
        |    |  1 |    |  3 |    |
        |    |    |  5 |    |    |
        | 10 |  4 |  c |  6 | 11 |
        |    |    |    |    |    |
        |    |  7 |  8 |  9 |    |
        |    |    |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            self.h1=self.h2=self.h3=self.h4=self.h5
            if self.car_pos[0] <= 35: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
                grid.add(12)
                self.h2=0
            elif self.car_pos[0] >= 595: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)
                grid.add(14)
                self.h4=0

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.lanes[self.car_lane] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :   
                        if y>400:
                            print(y)   
                        if y>300 and y<1000:
                            grid.add(13)
                            if y<self.h3: self.h3=y

                        if y > 0 and y < 300:
                            grid.add(2)
                            if y < 200:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y>-80 and y<1000:
                            grid.add(14)
                            if y<self.h4: self.h4=y

                        if y > 80 and y < 250:
                            grid.add(3)
                        elif y < -120 and y > -250:
                            grid.add(9)
                        elif y < 80 and y > -120:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y>-80 and y<1000:
                            grid.add(12)
                            if y<self.h2: self.h2=y

                        if y > 80 and y < 250:
                            grid.add(1)
                        elif y < -120 and y > -250:
                            grid.add(7)
                        elif y < 80 and y > -120:
                            grid.add(4)
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            # if self.player_no == 0:
            #     print(grid)
            if len(grid) == 0:
                return ["SPEED"]
            else:
                if (2 not in grid) :

                    if (13 in grid):
                        if (12 not in grid):
                            return ["SPEED", "MOVE_LEFT"]
                        elif (14 not in grid):
                            return ["SPEED", "MOVE_RIGHT"]
                        elif (self.h2>self.h3) and (self.h2>self.h4):
                            return ["SPEED", "MOVE_LEFT"]
                        elif (self.h4>self.h3):
                            return ["SPEED", "MOVE_RIGHT"]

                if (2 not in grid): # Check forward 
                    # Back to lane center
                    print(2)
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :return ["SPEED"]
                else:
                    if (5 in grid): # NEED to BRAKE
                        if (4 not in grid) : # turn left 
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (6 not in grid) : # turn right
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                    
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid): # turn left 
                        return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid): # turn right
                        return ["SPEED", "MOVE_RIGHT"]
                    if (4 not in grid) : # turn left 
                        return ["MOVE_LEFT"]    
                    if (6 not in grid) : # turn right
                        return ["MOVE_RIGHT"]
                    
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70

        
        if self.c==0:
            print(self.player)
            self.c=1
        
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass