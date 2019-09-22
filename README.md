# PyKlotski puzzle
This project is my assignment for artificial intelligence classes.

## Klotski file format
Klotski file format is defined as follows:
 - First line determines height and width of the table
 - Follows *height* lines of following format:
   - `-` represents a wall
   - `+` represents a goal space
   - `.` represents a free space
   - any other symbol (including white spaces) represents a block
   - final line contains a single symbol which determines which block is the one that is supposed to be placed to goal space

## Structure
### Event
 - This class I found while researching event system in python
 - Original poster is [longpoke](https://stackoverflow.com/users/80243/l%cc%b2%cc%b3o%cc%b2%cc%b3%cc%b3n%cc%b2%cc%b3%cc%b3g%cc%b2%cc%b3%cc%b3p%cc%b2%cc%b3o%cc%b2%cc%b3%cc%b3k%cc%b2%cc%b3%cc%b3e%cc%b2%cc%b3%cc%b3)
 - It extends list with event handler capabilities
### KlotskiBlock
 - Contained in `klotski.py`
 - Contains methods for block's manipulation such as:
   - `by_one_movements(self)` (movements by one square)
   - `all_movements(self)` (all possible movements of the block on table)
 - Is represented by unique index
 - Contains several properties among which are `table` (KlotskiTable), `shape` (set of positions determining the shape of the block) and `available_movements` (set of positions where can be the block placed to)

### KlotskiTable
 - Contained in `klotski.py`
 - Represents table of klotski blocks
 - Loads from a *klotski* file
 - Is indexable with `int` (returns a row of block indeces) or a `tuple` of `int`s (returns a block index)
 - Contains methods:
   - `get_block(self, index)` (returns a block with given index)
   - `is_solved(self)` (checks whether the puzzle is solved)
   - `move_block(self, block, position)` (moves the given block to the given position if possible, throws `Exception` otherwise)
 - Contains two event handlers - `on_solved` and `on_block_moved`

### KlotskiSimulator
TBD
#### Klotski Simulator's AI format
TBD

## AIs

### PriorityQueueAStar (PQA*)
TBD

### RecursiveIDAStarCopy (CIDA*)
TBD

### RecursiveIDAStarBacktrack (BIDA*)
TBD

### RecursiveBFS (RBFS)
TBD

### SMAstar (SMA*)
TBD

### Comparison
|  States visited  | PQA* | CIDA* | BIDA* | RBFS | SMA* |
| :--------------: | :--: | :---: | :---: | :--: | :--: |
|     sample01     |      |       |       |      |      |
|     sample02     |      |       |       |      |      |
|     sample03     |      |       |       |      |      |
|     sample04     |      |       |       |      |      |
|     sample05     |      |       |       |      |      |
|     sample06     |      |       |       |      |      |

|  Time needed  | PQA* | CIDA* | BIDA* | RBFS | SMA* |
| :-----------: | :--: | :---: | :---: | :--: | :--: |
|    sample01   |      |       |       |      |      |
|    sample02   |      |       |       |      |      |
|    sample03   |      |       |       |      |      |
|    sample04   |      |       |       |      |      |
|    sample05   |      |       |       |      |      |
|    sample06   |      |       |       |      |      |