:- dynamic matrix/1.
:- dynamic(cells/1).


matrix.

unknown.    %0
damaged.    %1
broken.     %2
possible.   %3
destroyed.  %4



random_cell(Result) :-
    cells(Cells),
    random_member(Cell, Cells),
    Result = Cell.

remove_value(cells(List), Value) :-
    select(Value, List, NewList),
    retract(cells(_)),
    assert(cells(NewList)).

% Define a helper predicate to update a single element
update_element(Matrix, X, Y, Value, NewMatrix) :-
    nth0(X, Matrix, Row, RestRows),
    nth0(Y, Row, Element, RestRow),
    NewElement is Element + Value,
    nth0(X, NewRow, NewElement, RestRow),
    nth0(Y, NewMatrix, NewRow, RestRows).

% Define the main predicate to update the matrix
update_matrix(Matrix, [X, Y], Value, NewMatrix) :-
    update_element(Matrix, X, Y, Value, NewMatrix).


