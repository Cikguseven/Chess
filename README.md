# Chess
Project to create Chess game with display using Pygame module. Also created move generation programme that generates legal chess moves to chosen depth in Stockfish format.

## Chess game
To try out the offline game, download the following files: board.py, main.py & pieces.py. Install pygame with pip.
``` python3 -m pip install -U pygame --user ```

## Move generation
Download either of the move generation files and change the position FEN, as well as depth and check_to_depth values.

### Performance comparison of move generation versions

#### Test position 1
FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 (Initial position)
![p1](https://user-images.githubusercontent.com/40373653/147361434-d5462ded-8121-4248-8688-f2b3b39e7fd5.PNG)
Depth 3 - 8902 Nodes
v1: 4.52s (1.97 kN/s)
v2: 0.48s (18.5 kN/s, ~9.4x faster)


#### Test position 2
FEN: r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -
![p2](https://user-images.githubusercontent.com/40373653/147361436-f61e4da4-d7d8-49f5-b612-070a83218f5d.PNG)
Depth 3 - 97862 Nodes
v1: 50.1s (1.95 kN/s)
v2: 6.18s (15.8 kN/s, ~8.1x faster)


#### Test position 3
FEN: 8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 
![p3](https://user-images.githubusercontent.com/40373653/147361438-3356fed6-897c-40a3-bd3d-80b0a7ed08a9.PNG)
Depth 5 - 674624 Nodes
v1: 154s (4.38 kN/s)
v2: 23.6s (28.6 kN/s, ~6.5x faster)


Credits to Chessprogramming wiki for providing various positions and perft results to debug move generation programme.
