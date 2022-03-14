
class Nim:
    def __init__(self, num_stones, max_removal, starting_player):
        self.num_stones = num_stones
        self.max_removal = max_removal
        self.starting_player = starting_player

        self.remaining_stones = num_stones
        self.playing_player = starting_player

    def get_legal_moves(self, state=None):
        """ Usikker om man skal hente moves ut ifra en state eller fra self-verdier """
        
        moves = []

        for i in range(1, self.max_removal + 1):
            if i <= self.num_stones:
                moves.append(i)



vartest = Nim(4, 6, 1)

# vartest.get_legal_moves()