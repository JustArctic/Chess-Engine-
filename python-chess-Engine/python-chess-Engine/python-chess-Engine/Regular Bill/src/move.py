class Move:

    def __init__(self, initial, final):
        """
        Creates a chess move.

        Parameters:
            initial (Square): The square the piece starts from.
            final (Square): The square the piece moves to.
        """

        # Starting square of the move
        self.initial = initial

        # Destination square of the move
        self.final = final

    def __str__(self):
        """
        Returns a readable string representation of the move.
        Example:
            (4, 6) -> (4, 4)
        """

        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def __eq__(self, other):
        """
        Allows two Move objects to be compared using ==.

        Two moves are considered equal if they have the
        same starting square and ending square.
        """

        return (
            self.initial == other.initial and
            self.final == other.final
        )
