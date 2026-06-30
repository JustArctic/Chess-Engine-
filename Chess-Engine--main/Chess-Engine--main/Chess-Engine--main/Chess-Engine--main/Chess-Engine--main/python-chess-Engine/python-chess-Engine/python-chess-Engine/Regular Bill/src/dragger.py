import pygame

from const import *


class Dragger:

    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------
    # Initialises the drag-and-drop controller used when
    # the player moves chess pieces with the mouse.
    #
    # Stores:
    # • Selected piece
    # • Mouse position
    # • Initial square
    # • Dragging state
    # ------------------------------------------------------
    def __init__(self):

        # The chess piece currently being dragged.
        self.piece = None

        # Indicates whether the player is dragging a piece.
        self.dragging = False

        # Current mouse X coordinate.
        self.mouseX = 0

        # Current mouse Y coordinate.
        self.mouseY = 0

        # Starting row of the selected piece.
        self.initial_row = 0

        # Starting column of the selected piece.
        self.initial_col = 0

    # ------------------------------------------------------
    # Update Piece Display
    # ------------------------------------------------------
    # Draws the selected chess piece underneath the mouse
    # cursor while it is being dragged.
    # ------------------------------------------------------
    def update_blit(self, surface):

        # Load the larger piece image used while dragging.
        self.piece.set_texture(size=128)
        texture = self.piece.texture

        # Load the image from disk.
        img = pygame.image.load(texture)

        # Position the image at the current mouse location.
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)

        # Draw the image onto the screen.
        surface.blit(img, self.piece.texture_rect)

    # ------------------------------------------------------
    # Update Mouse Position
    # ------------------------------------------------------
    # Saves the current mouse coordinates whenever the
    # mouse moves.
    # ------------------------------------------------------
    def update_mouse(self, pos):

        # Store the mouse X and Y coordinates.
        self.mouseX, self.mouseY = pos

    # ------------------------------------------------------
    # Save Initial Position
    # ------------------------------------------------------
    # Records the board square from which the player
    # started dragging the piece.
    # ------------------------------------------------------
    def save_initial(self, pos):

        # Convert mouse coordinates into board coordinates.
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    # ------------------------------------------------------
    # Begin Dragging
    # ------------------------------------------------------
    # Stores the selected piece and enables dragging mode.
    # ------------------------------------------------------
    def drag_piece(self, piece):

        # Save the selected piece.
        self.piece = piece

        # Enable dragging.
        self.dragging = True

    # ------------------------------------------------------
    # Stop Dragging
    # ------------------------------------------------------
    # Clears the selected piece and disables dragging mode.
    # ------------------------------------------------------
    def undrag_piece(self):

        # Remove the selected piece.
        self.piece = None

        # Disable dragging.
        self.dragging = False
