"""
Want an object that will hold:
    (1) The locations of the walls "#"
    (2) The color of each tile in the maze
    (3) The robots starting position
"""

class Maze:

    # internal structure:
    #   self.walls: set of tuples with wall locations
    #   self.width: number of columns
    #   self.height: number of rows

    def __init__(self, mazefilename):
        # read the maze file into a list of strings
        f = open(mazefilename) # f is a file object in python
        lines = [] # building the maze when the lines
        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) == 0:
                pass
            elif line[0] == "\\": # adding robots to the maze in a different checker
                #print("command")
                # there's only one command, \robot, so assume it is that
                parms = line.split()
                x = int(parms[1])
                y = int(parms[2])
                self.robotloc = (x,y)
            else:
                lines.append(line)
        f.close()

        self.width = len(lines[0])
        self.height = len(lines)
        self.size = self.width * self.height

        self.map = list("".join(lines)) # flattening the maze?

    
     # clever function that enables us to treat the entire maze as a single string and not an array
    def index(self, x, y):
        return (self.height - y - 1) * self.width + x


      # function called only by __str__ that takes the map and the
    #  robot state, and generates a list of characters in order
    #  that they will need to be printed out in.
    def create_render_list(self):
        #print(self.robotloc)
        renderlist = list(self.map)

        x, y = self.robotloc

        renderlist[self.index(x, y)] = "x"

        return renderlist


    # robots are only added to the map when we print the to_string
    def __str__(self):

        # render robot locations into the map
        renderlist = self.create_render_list()

        # use the renderlist to construct a string, by
        #  adding newlines appropriately

        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                s+= renderlist[self.index(x, y)]

            s += "\n"

        return s

   # returns True if the location is a floor
    def legal_loc(self, x, y):
        # first does a check if we are outside of the bound of the maze
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        # then index into the data and see if there is a free space there or not
        if self.map[self.index(x, y)] == "#":
            return False
        
        return True 

    def get_color(self,x,y):
        return self.map[self.index(x,y)]

if __name__ == "__main__":
    tester = Maze("maze1.text")
    # robot can move around the maze!
   
    print(tester)
    tester.robotloc = (2,0)
    print(tester)
    tester.robotloc = (1,0)
    print(tester)
    tester.robotloc = (0,0)
        

