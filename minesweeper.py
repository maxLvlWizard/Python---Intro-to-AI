import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells      

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
           if cell in sentence.cells:
                sentence.cells.remove(cell)
                sentence.count -= 1
            
 

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # Mark the cell as safe
        self.safes.add(cell)
        
        ### Add sentence to the AI's knowledge base based on teh value of the cell and the count ###
        
        sentence_cells = set()
        
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    sentence_cells.add((i,j))
        if count > 0:                    
            self.knowledge.append(Sentence(sentence_cells, count))
            print("Adding Sentence to Knowledge database: ", sentence_cells, count)
        else:
            self.safes = self.safes.union(sentence_cells)

        updates_available = True
        while updates_available is True:
            updates_available = False

#
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)

            ###  mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base ###
            print("updating knowledge for known safes and know mines")        
            for safe in self.safes:
                for sentence in self.knowledge:
                    if safe in sentence.cells:
                            self.mark_safe((safe))
                            updates_available = True
        
            for mine in self.mines:
                for sentence in self.knowledge:
                    if mine in sentence.cells:
                            self.mark_mine((mine))
                            updates_available = True
    
    # If number of cells in sentence equlas the count, all cells are mines. Update self.mines and delete sentence from knowledge database. 
            fz_mines = frozenset()
            for sentence in self.knowledge:
                if len(sentence.cells) == sentence.count:
                   fz_mines = sentence.cells 
                   print("Sentence with all MINES: ", sentence)
                   self.mines = self.mines.union(fz_mines)
                   self.knowledge.remove(sentence)
                   updates_available = True
    
    # If the count is zero, all cells are safe. Update self.safes and delete sentence from knowledge database.                
            fz_safe = frozenset()
            for sentence in self.knowledge:
                if sentence.count == 0:
                   fz_safes = sentence.cells 
                   print("Sentence with all safes: ", sentence)
                   self.safes = self.safes.union(fz_safes)
                   self.knowledge.remove(sentence)
                   updates_available = True
    
    # Create new sentences based on knowledge
            print("Checking if we can create new sentences")
            for sentence in self.knowledge: 
                set1 = sentence.cells
                count1 = sentence.count
                for my_sentence in self.knowledge:
                    set2 = my_sentence.cells
                    count2 = my_sentence.count
                    if set1 < set2:
                        my_sentence_cells = set2 - set1
                        my_sentence_count = count1 - count2                    
                        if my_sentence_count > 0:
                            if len(my_sentence_cells) > 0:
                                updates_available = True 
                                print("Creating new sentence: ", my_sentence_cells, my_sentence_count)
                                self.knowledge.append(Sentence(my_sentence_cells, my_sentence_count))
                            else:
                                if len(my_sentence_cells) > 0:
                                    updates_available = True 
                                    print("Adding safe cells: ", my_sentence_cells)
                                    self.safes = my_sentence_cells.union(self.safes)
                       
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.moves_made) < len(self.safes):
            safe_move = self.safes - self.moves_made
            return safe_move.pop()


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        available_move = False
        
        while available_move is False:
            row = random.randint(0,7)
            column = random.randint(0,7)
            if (row, column) not in self.mines:
                if (row, column) not in self.moves_made:
                    available_move = True
        return (row, column)    
        

def move():
    move = ai.make_safe_move()
    if move not in board.mines:
        print("Moing here: ", move)
        ai.add_knowledge(move, board.nearby_mines(move))
        if ai.mines == board.mines:
            return "YOU WIN"
        else:
            return print("Remaining safe moves: ", ai.safes - ai.moves_made)

def random_move():
    move = ai.make_random_move()
    if move in board.mines:
        return "You Lose"
    else:
        ai.add_knowledge(move, board.nearby_mines(move))
        print("Remaining safe moves: ", ai.safes - ai.moves_made)
        
#board = Minesweeper()      
  
#ai = MinesweeperAI()
#board.print()



                 