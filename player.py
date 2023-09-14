class Player:
    def __init__(self,id, name, position, rank):
        self.id = id
        self.name = name
        self.rank = rank
        self.position = position

    def get_data(self):
        ret = "Player ID: " + str(self.id) + "\n" + "Player Name: " + str(self.name) + "\n" + "Player Position: " + str(self.position) + "\n" + "Player Rank: " + str(self.rank) + "\n"
        return ret

