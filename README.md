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
Results are averaged from 20 runs where all agents had 3 minutes for the search.

| Success Rate (%) |  Random   | CIDA* | PQA*  | BIDA* | RBFS  | SMA*  |
| :--------------: | :-------: | :---: | :---: | :---: | :---: | :---: |
|     sample01     |   100.0   | 100.0 | 100.0 | 100.0 |  TBD  |  TBD  |
|     sample02     |   100.0   | 100.0 | 100.0 | 100.0 |  TBD  |  TBD  |
|     sample03     |   100.0   | 100.0 | 100.0 | 100.0 |  TBD  |  TBD  |
|     sample04     |   100.0   | 100.0 | 100.0 | 100.0 |  TBD  |  TBD  |
|     sample05     |    0.0    |  0.0  |  0.0  |  0.0  |  TBD  |  TBD  |
|     sample06     | **100.0** |  0.0  |  0.0  |  0.0  |  TBD  |  TBD  |
|     sample07     | **75.0**  |  0.0  |  0.0  |  0.0  |  TBD  |  TBD  |

| Steps Needed (#) |   Random   | CIDA* | PQA*  | BIDA* | RBFS  | SMA*  |
| :--------------: | :--------: | :---: | :---: | :---: | :---: | :---: |
|     sample01     |     1      |   1   |   1   |   1   |  TBD  |  TBD  |
|     sample02     |     10     |   5   | **1** | **1** |  TBD  |  TBD  |
|     sample03     |    215     |  12   | **9** | **9** |  TBD  |  TBD  |
|     sample04     |     76     |   7   | **1** | **1** |  TBD  |  TBD  |
|     sample05     |     0      |   0   |   0   |   0   |  TBD  |  TBD  |
|     sample06     |  **833**   |   0   |   0   |   0   |  TBD  |  TBD  |
|     sample07     | **251734** |   0   |   0   |   0   |  TBD  |  TBD  |

| States visited (#) | Random | CIDA*  |   PQA*   | BIDA*  | RBFS  | SMA*  |
| :----------------: | :----: | :----: | :------: | :----: | :---: | :---: |
|      sample01      | **1**  |   2    |    2     |   2    |  TBD  |  TBD  |
|      sample02      |   10   |   19   |  **2**   |   10   |  TBD  |  TBD  |
|      sample03      |  215   |  3302  |  **37**  |  1558  |  TBD  |  TBD  |
|      sample04      |   76   |  100   |  **2**   |  146   |  TBD  |  TBD  |
|      sample05      | 654144 | 24238  |  **12**  | 275416 |  TBD  |  TBD  |
|      sample06      |  833   | 129481 | **334**  | 145399 |  TBD  |  TBD  |
|      sample07      | 251734 | 109907 | **1566** | 179654 |  TBD  |  TBD  |

| Time needed (s) | Random  | CIDA* |  PQA*   | BIDA* | RBFS  | SMA*  |
| :-------------: | :-----: | :---: | :-----: | :---: | :---: | :---: |
|    sample01     |   0.0   |  0.0  |   0.0   |  0.0  |  TBD  |  TBD  |
|    sample02     |   0.0   |  0.0  |   0.0   |  0.0  |  TBD  |  TBD  |
|    sample03     |   0.0   |  4.0  |   0.0   |  1.0  |  TBD  |  TBD  |
|    sample04     |   0.0   |  0.0  |   0.0   |  0.0  |  TBD  |  TBD  |
|    sample05     |  180.0  | 60.0  | **0.0** | 180.0 |  TBD  |  TBD  |
|    sample06     | **0.0** | 180.0 |  180.0  | 180.0 |  TBD  |  TBD  |
|    sample07     |  108.0  | 180.0 |  180.0  | 180.0 |  TBD  |  TBD  |

| CPU Used (%) |  Random  | CIDA* |   PQA*   | BIDA* | RBFS  | SMA*  |
| :----------: | :------: | :---: | :------: | :---: | :---: | :---: |
|   sample01   |   33.0   | 18.0  | **16.0** | 29.0  |  TBD  |  TBD  |
|   sample02   |   34.0   | 20.0  | **11.0** | 33.0  |  TBD  |  TBD  |
|   sample03   | **50.0** | 54.0  |   52.0   | 53.0  |  TBD  |  TBD  |
|   sample04   | **45.0** | 52.0  |   48.0   | 51.0  |  TBD  |  TBD  |
|   sample05   |   74.0   | 70.0  | **18.0** | 78.0  |  TBD  |  TBD  |
|   sample06   | **52.0** | 77.0  |   69.0   | 76.0  |  TBD  |  TBD  |
|   sample07   | **68.0** | 71.0  |   71.0   | 73.0  |  TBD  |  TBD  |

| Memory Used (%) | Random | CIDA* | PQA*  | BIDA* | RBFS  | SMA*  |
| :-------------: | :----: | :---: | :---: | :---: | :---: | :---: |
|    sample01     |  30.0  | 29.0  | 29.0  | 29.0  |  TBD  |  TBD  |
|    sample02     |  36.0  | 29.0  | 29.0  | 29.0  |  TBD  |  TBD  |
|    sample03     |  30.0  | 29.0  | 29.0  | 29.0  |  TBD  |  TBD  |
|    sample04     |  36.0  | 29.0  | 29.0  | 29.0  |  TBD  |  TBD  |
|    sample05     |  36.0  | 29.0  | 29.0  | 29.0  |  TBD  |  TBD  |
|    sample06     |  36.0  | 29.0  | 29.0  | 29.0  |  TBD  |  TBD  |
|    sample07     |  30.0  | 29.0  | 29.0  | 29.0  |  TBD  |  TBD  |

> INFO: Memory is only orientational due to caching and garbage collector