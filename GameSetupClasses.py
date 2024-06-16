# Imports 
import HelperFunctionsGame as HFG
import numpy as np

class Battleship_Board():
    
    def __init__(self, state):
        self.state = state
        self.board = np.full((11, 11), '   ')
        self.board[0, 1:] = np.array([f'{i}  ' if i < 10 else f'{i} ' for i in range(1, 11)])
        self.board[1:, 0] = HFG.letter_labels
        self.board[0, 0] = ' '
    
    def __repr__(self):
        return f"\n{np.array2string(self.board, separator=' ')}\nThis is an {self.state} battleship board."

# Defines the types of ships available in the game
class Ship():
    def __init__(self, ship_type, size, status, s='S'):
        self.ship_type = ship_type
        self.size = size
        self.status = status
        self.s = s
        self.health = size

    def __repr__(self):
        return f"This is a {self.ship_type} with a size of {self.size}. The current status of this ship is {self.status}. The symbol for this ship is {self.s}" 

def create_ship(ship_type):
    ships = {
        'carrier': ('Carrier', 5, 'Functional', ' S '),
        'battleship': ('Battleship', 4, 'Functional', ' S '),
        'cruiser': ('Cruiser', 3, 'Functional', ' S '),
        'submarine': ('Submarine', 3, 'Functional', ' S '),
        'destroyer': ('Destroyer', 2, 'Functional', ' S ')
    }
    
    if ship_type.lower() in ships:
        
        return Ship(*ships[ship_type.lower()])
    
    raise ValueError("Unknown ship type")

class Player():
    def __init__(self, name, num_ships=5, ships={}):
        self.name = name 
        self.num_ships = num_ships
        self.ships = ships
        self.friendly_board = Battleship_Board('Active')
        self.target_board = Battleship_Board('Active')
    
    def __repr__(self):
        return f"This player's name is {self.name}. They have an {self.friendly_board.state} friendly board and an {self.target_board.state} target board. They currently have {self.num_ships} ships remaining"
    
    def display_friendly_board(self):
        print("This is your friendly board: \n", self.friendly_board.board ,"\n")
    
    def display_target_board(self):
        print("This is your target board: \n", self.target_board.board ,"\n")
        
    def is_occupied(self, size, start_position, orientation):
        row, column = HFG.label_to_coord(start_position)
        if orientation.lower() == 'up':
            
            return any(self.friendly_board.board[row-i, column] != '   ' for i in range(size))
        
        elif orientation.lower() == 'down':
            
            return any(self.friendly_board.board[row+i, column] != '   ' for i in range(size))
        
        elif orientation.lower() == 'right':
            
            return any(self.friendly_board.board[row, column+i] != '   ' for i in range(size))
        
        elif orientation.lower() == 'left':
            return any(self.friendly_board.board[row, column-i] != '   ' for i in range(size))
    
    def ship_to_board(self, ship_type, start_position, orientation):
        new_ship = create_ship(ship_type)
        
        if self.is_occupied(new_ship.size, start_position, orientation):
            
            print("Spot already filled. Please change the location of your current ship")
            return False
        
        else:
            
            self.place_ship(new_ship, start_position, orientation)


    def place_ship(self, ship, start_position, orientation):
        positions = []
        row, column = HFG.label_to_coord(start_position)
        
        if orientation.lower() == 'up':
            
            self.friendly_board.board[row-ship.size+1:row+1, column] = ship.s
            positions = [(row-i, column) for i in range(ship.size)]
            
        elif orientation.lower() == 'down':
            
            self.friendly_board.board[row:row+ship.size, column] = ship.s
            positions = [(row+i, column) for i in range(ship.size)]
            
        elif orientation.lower() == 'right':
            
            self.friendly_board.board[row, column:column+ship.size] = ship.s
            positions = [(row, column+i) for i in range(ship.size)]
            
        elif orientation.lower() == 'left':
            
            self.friendly_board.board[row, column-ship.size+1:column+1] = ship.s
            positions = [(row, column-i) for i in range(ship.size)]
            
        self.ships[ship] = positions

    
    def strike(self, enemy, location):
        row, column = HFG.label_to_coord(location)
        
        if enemy.friendly_board.board[row, column] == ' S ':
            enemy.friendly_board.board[row, column] = ' H '
            self.target_board.board[row, column] = ' H '
            
        elif enemy.friendly_board.board[row, column] == '   ':
            enemy.friendly_board.board[row,column] = ' M '
            self.target_board.board[row, column] = ' M '
            
        elif enemy.friendly_board.board[row, column] in [' M ', ' H ']:
            print("You have already struck here. Please select a new location")
    
    def Turn(self, enemy):
        self.display_friendly_board()
        self.display_target_board()



