class Brain:
    """
        Brain Object
    """

    def __init__(self):
        self.moves = {}


    def createBrain(self):
        """
            creates the initial random brain

        """
        value_table = {}
        pair_table = {}
        ace_table = {}

        self.moves = {"value_table": value_table, "pair_table": pair_table, "ace_table": ace_table}