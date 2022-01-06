# Chess

Project to create Chess game with display using Pygame module. Also created move generation programme that generates legal chess moves to chosen depth in Stockfish format.

## Chess game

To try out the offline game, download the following files: board.py, main.py & pieces.py. Install Pygame module with pip.

``` python3 -m pip install -U pygame --user ```


## Move generation

Download either of the move generation files and change the position FEN, as well as depth and check_to_depth values.  

### Performance comparison of move generation versions 1 & 2

Tested on Ryzen 5 3600/16 GB RAM/SSD  

### Test position 1

FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 (Initial position)
<p align="left"><img src="https://user-images.githubusercontent.com/40373653/147361434-d5462ded-8121-4248-8688-f2b3b39e7fd5.PNG" height="400" width="400"></p>

#### Depth 3 - 8902 nodes (20 initial nodes)

* v1: 4.52s (1.97 kN/s)  
* v2: 0.48s (18.5 kN/s)  
* v3: 0.07s (127 kN/s)  


### Test position 2

FEN: r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -
<p align="left"><img src="https://user-images.githubusercontent.com/40373653/147361436-f61e4da4-d7d8-49f5-b612-070a83218f5d.PNG" height="400" width="400"></p>

#### Depth 3 - 97862 Nodes (48 initial nodes)  

* v1: 50.1s (1.95 kN/s)  
* v2: 6.18s (15.8 kN/s)  
* v3: 0.56s (175 kN/s)  


### Test position 3

FEN: r3k2r/p6p/8/B7/1pp1p3/3b4/P6P/R3K2R w KQkq -
<p align="left"><img src="https://user-images.githubusercontent.com/40373653/147379256-bb93d6d5-0267-4157-9e52-9dd4f1a0993c.PNG" height="400" width="400"></p>

#### Depth 4 - 150072 Nodes (17 initial nodes)  

* v1: 46.1s (3.25 kN/s)  
* v2: 6.58s (22.8 kN/s)  
* v3: 0.96s (156 kN/s)  


### Test position 4

FEN: 8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 
<p align="left"><img src="https://user-images.githubusercontent.com/40373653/147361438-3356fed6-897c-40a3-bd3d-80b0a7ed08a9.PNG" height="400" width="400"></p>

#### Depth 5 - 674624 Nodes (14 initial nodes)

* v1: 154s (4.38 kN/s)  
* v2: 23.6s (28.6 kN/s)  
* v3: 4.08s (165 kN/s)  

## Credits

This project took reference and inspiration from the following sources:
* [Sebastian Lague's Chess AI](https://www.youtube.com/watch?v=U4ogK0MIzqk)
* [KettCodes' Chess Game with Pygame](https://github.com/KettCodes/PythonPracticeChessBoard2)
* [Chessprogramming Wiki](https://www.chessprogramming.org/Perft_Results) for various positions and perft results to debug move generation programme.
* [Numpty Perft](https://sites.google.com/site/numptychess/perft) for more positions and perft results.
