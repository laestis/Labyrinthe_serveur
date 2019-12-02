"""Ce module contient la classe Robot."""

class Robot:

    """gestion du robot"""

    def __init__(self, pos_x = None, pos_y = None):
        """ default constructor will use position {-1,-1}"""
        #Checking constructor argument or not
        if (pos_x is None) :
            self.pos_x = -1
        else:
            self.pos_x = pos_x

        #Checking constructor argument or not
        if (pos_y is None) :
            self.pos_y = -1
        else:
            self.pos_y = pos_y

        # variable to manage door
        self.ThroughDoor = False

    def __repr__(self):
        return "Robot en position [{}][{}]".format(self.pos_x, self.pos_y)
