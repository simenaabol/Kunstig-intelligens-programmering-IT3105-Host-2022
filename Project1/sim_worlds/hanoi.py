class Hanoi():
    def __init__(self, pegs, discs) :
        self.pegs = pegs
        self.discs = discs

    def get_state(self):
        return "HanoiState"

    def get_legal_moves(self):
        return "LegalHanoiMoves"

    def game_over(self):
        raise NotImplementedError()




