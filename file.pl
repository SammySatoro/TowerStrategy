:- use_module(library(random)).

% Define the size of the matrix (10x10)
size(10).

% Generate a random permutation of cells
random_permutation_cells(Permutation) :-
    size(Size),
    findall(X-Y, (between(1, Size, X), between(1, Size, Y)), Cells),
    random_permutation(Cells, Permutation).

% Define the ship lengths
ship_lengths([4, 3, 3, 2, 2, 2, 20, 20, 20, 20]).

% Place ships randomly on the matrix
place_ships(Matrix) :-
    random_permutation_cells(Permutation),
    ship_lengths(ShipLengths),
    place_ships(ShipLengths, Permutation, Matrix).

place_ships([], _, _).
place_ships([Length|Rest], [X-Y|RestCoords], Matrix) :-
    set_cell(Matrix, X, Y, 'B'),
    assert(battleship(X, Y)), % Add the ship coordinates to facts
    Length1 is Length - 1,
    place_ship(Length1, RestCoords, Matrix).

set_cell(Matrix, X, Y, Value) :-
    nth1(X, Matrix, Row),
    nth1(Y, Row, Value).

% Query to generate a matrix with ship placements
generate_matrix(Matrix) :-
    size(Size),
    length(Matrix, Size),
    generate_matrix_rows(Size, Matrix).

generate_matrix_rows(_, []).
generate_matrix_rows(Size, [Row|Rest]) :-
    length(Row, Size),
    generate_matrix_rows(Size, Rest).