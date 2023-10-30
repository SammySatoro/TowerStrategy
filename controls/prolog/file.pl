:- dynamic cells/1.
:- dynamic matrix/1.
:- dynamic wall_cells/1.
:- dynamic last_move/1.
:- dynamic nesw_cells/1.
:- dynamic possible_cells/1.
:- dynamic current_wall_cells/1.
:- dynamic none_zero_cells/1.
:- dynamic zero_cells/1.


% cells with hp: 1-3
% unknown cells: 0
% nontargetable cells: -1`




last_move.
possible_cells([]).
did_found_current_wall_cells(false).
current_wall_cells([]).
none_zero_cells([]).
zero_cells([]).


test(Cell, Data) :-
%    define_last_move(Cell),
%    define_possible_cells,
    shoot(Cell),
    possible_cells(Cells),
%    matrix(M),
%    last_move([X, Y]),
%    get_matrix_value(M, [X, Y], _),
%    write(Value),
%    last_move([X, Y]),
%    write(X), write(Y), nl,
%    find_current_wall_cells(Cell, _),
%    current_wall_cells(X),
%    write(X), nl,
%    write(Cells), nl,
    Data = Cells.

get_possible_cells(Cell, Cells) :-
    matrix(M),
    retractall(possible_cells(_)),
    get_matrix_value(M, Cell, Value),
    (Value =\= 0 ->
        define_last_move(Cell),
        define_possible_cells,
        possible_cells(Cells)
        ;
        Cells = []
    ).

get_close_cells([X, Y], Cells) :-
    T is Y - 1, B is Y + 1,
    L is X - 1, R is X + 1,
    Cells0 = [],
    (between(0, 9, T) -> append([[X, T]], Cells0, Cells1); Cells1 = Cells0, true),
    (between(0, 9, B) -> append([[X, B]], Cells1, Cells2); Cells2 = Cells1, true),
    (between(0, 9, L) -> append([[L, Y]], Cells2, Cells3); Cells3 = Cells2, true),
    (between(0, 9, R) -> append([[R, Y]], Cells3, Cells4); Cells4 = Cells3, true),
    (between(0, 9, T) ->
        (between(0, 9, L) -> append([[L, T]], Cells4, Cells5); Cells5 = Cells4, true),
        (between(0, 9, R) -> append([[R, T]], Cells5, Cells6); Cells6 = Cells5, true)
        ; Cells6 = Cells4, true),
    (between(0, 9, B) ->
        (between(0, 9, L) -> append([[L, B]], Cells6, Cells7); Cells7 = Cells6, true),
        (between(0, 9, R) -> append([[R, B]], Cells7, Cells8); Cells8 = Cells7, true)
        ; Cells8 = Cells6, true),
    Cells = Cells8.

shoot([X, Y]) :-
    matrix(M),
    define_last_move([X, Y]),
    get_element(M, X, Y, CellValue),
    (CellValue > 0 ->
        shoot_hit(M, X, Y, CellValue)
        ;
        shoot_miss(M, X, Y, _), true
    ).

shoot_hit(M, X, Y, CellValue) :-
    NewCellValue = CellValue - 1,
    update_matrix_item(M, [X, Y], NewCellValue, _),
    define_possible_cells.

shoot_miss(M, X, Y, _) :-
    NewCellValue = -1,
    remove_value_from_cells([X, Y]),
    update_matrix_item(M, [X, Y], NewCellValue, _).


define_possible_cells :-
    last_move([X, Y]),
    matrix(M),
    NY is Y - 1, EX is X + 1,
    SY is Y + 1, WX is X - 1,
    Cells0 = [],
    get_matrix_value(M, [X, Y], Value),
    (between(0, 9, NY) -> get_matrix_value(M, [X, NY], ValueNY) ; ValueNY = 0, true),
    (between(0, 9, SY) -> get_matrix_value(M, [X, SY], ValueSY) ; ValueSY = 0, true),
    (between(0, 9, EX) -> get_matrix_value(M, [EX, Y], ValueEX) ; ValueEX = 0, true),
    (between(0, 9, WX) -> get_matrix_value(M, [WX, Y], ValueWX) ; ValueWX = 0, true),
    (Value > 0 -> append([[X, Y]], Cells0, Cells) ; Cells = Cells0, true),
    (ValueNY =\= -1, between(0, 9, NY), not_last_move([X, NY]), not_in_possible_cells([X, NY]) -> append([[X, NY]], Cells, Cells1) ; Cells1 = Cells, true),
    (ValueSY =\= -1, between(0, 9, SY), not_last_move([X, SY]), not_in_possible_cells([X, SY]) -> append([[X, SY]], Cells1, Cells2) ; Cells2 = Cells1, true),
    (ValueEX =\= -1, between(0, 9, EX), not_last_move([EX, Y]), not_in_possible_cells([EX, Y]) -> append([[EX, Y]], Cells2, Cells3) ; Cells3 = Cells2, true),
    (ValueWX =\= -1, between(0, 9, WX), not_last_move([WX, Y]), not_in_possible_cells([WX, Y]) -> append([[WX, Y]], Cells3, Cells4) ; Cells4 = Cells3, true),
    possible_cells(Cells5),
    add_distinct_elements(Cells5, Cells4, Res),
    retractall(possible_cells(_)),
    assertz(possible_cells(Res)).


%summ(A, B, Res) :-
%    Res is A + B.
%
%find_current_wall_cells([X, Y]) :-
%    matrix(M),
%    T1 is Y - 1, B1 is Y + 1, L1 is X - 1, R1 is X + 1,
%    T2 is Y - 2, B2 is Y + 2, L2 is X - 2, R2 is X + 2,
%    T3 is Y - 3, B3 is Y + 3, L3 is X - 3, R3 is X + 3,
%    FourSquareTL = [[X, Y],[X, T1],[L1, Y],[L1, T1]],
%    FourSquareTR = [[X, Y],[X, T1],[R1, Y],[R1, T1]],
%    FourSquareBR = [[X, Y],[X, B1],[R1, Y],[R1, B1]],
%    FourSquareBL = [[X, Y],[X, B1],[L1, Y],[L1, B1]],
%    retractall(current_wall_cells(_)),
%    assertz(current_wall_cells(NonZeroCells4)).


%find_current_wall_cells([X, Y], [PrevX, PrevY]) :-
%    matrix(M),
%    T is Y - 1, B is Y + 1, L is X - 1, R is X + 1,
%    NonZeroCells = [],
%    (between(0, 9, T) -> get_matrix_value(M, [X, T], ValueT) ; ValueT = -1, true),
%    (ValueT > 0, ValueT =\= -1 -> append([[X, T]], NonZeroCells, NonZeroCells1) ; NonZeroCells1 = NonZeroCells, true),
%    (between(0, 9, B) -> get_matrix_value(M, [X, B], ValueB) ; ValueB = -1, true),
%    (ValueB > 0, ValueB =\= -1 -> append([[X, B]], NonZeroCells1, NonZeroCells2); NonZeroCells2 = NonZeroCells1, true),
%    (between(0, 9, L) -> get_matrix_value(M, [L, Y], ValueL) ; ValueL = -1, true),
%    (ValueL > 0, ValueL =\= -1 -> append([[L, Y]], NonZeroCells2, NonZeroCells3); NonZeroCells3 = NonZeroCells2, true),
%    (between(0, 9, R) -> get_matrix_value(M, [R, Y], ValueR) ; ValueR = -1, true),
%    (ValueR > 0, ValueR =\= -1 -> append([[R, Y]], NonZeroCells3, NonZeroCells4); NonZeroCells4 = NonZeroCells3, true),
%    none_zero_cells(NZC),
%    (length(NZC, 0) -> retractall(none_zero_cells(_)) ; true),
%    assertz(none_zero_cells(NonZeroCells4)),
%    none_zero_cells(NZC2),
%    write("NZC2"), write(" = "), write(NZC2), nl,
%    (\+ length(NZC2, 0) -> iterate_non_zero_cells(NZC2) ; true),
%    none_zero_cells(NZC3),
%    NonZeroCells5 = [[X,Y]|NZC3],
%    retractall(current_wall_cells(_)),
%    assertz(current_wall_cells(NonZeroCells5)).
%
%iterate_non_zero_cells([]).
%iterate_non_zero_cells([[X,Y]|T]) :-
%    retractall(none_zero_cells(_)),
%    assertz(none_zero_cells(T)),
%    find_current_wall_cells([X,Y], _),
%    iterate_non_zero_cells(T).

%find_current_wall_cells([X, Y]) :-
%    matrix(M),
%    T is Y - 1, B is Y + 1, L is X - 1, R is X + 1,
%    (between(0, 9, T) -> get_matrix_value(M, [X, T], ValueT),
%        (between(0, 9, L) -> get_matrix_value(M, [L, T], ValueLT) ; ValueLT = -1, true),
%        (between(0, 9, R) -> get_matrix_value(M, [R, T], ValueRT) ; ValueRT = -1, true) ; ValueT = -1, true),
%    (between(0, 9, B) -> get_matrix_value(M, [X, B], ValueB),
%        (between(0, 9, L) -> get_matrix_value(M, [L, B], ValueLB) ; ValueLB = -1, true),
%        (between(0, 9, R) -> get_matrix_value(M, [R, B], ValueRB) ; ValueRB = -1, true) ; ValueB = -1, true),
%    (between(0, 9, L) -> get_matrix_value(M, [L, Y], ValueL) ; ValueL = -1, true),
%    (between(0, 9, R) -> get_matrix_value(M, [R, Y], ValueR) ; ValueR = -1, true),
%    Cells = [[X, Y]],
%    (ValueT > 0, between(0, 9, T) -> append([[X, T]], Cells, Cells1),
%        (ValueLT > 0, between(0, 9, L) -> append([[L, T]], Cells1, Cells2) ; Cells2 = Cells1, true),
%        (ValueRT > 0, between(0, 9, R) -> append([[R, T]], Cells2, Cells3) ; Cells3 = Cells2, true) ; Cells3 = Cells, true),
%    (ValueB > 0, between(0, 9, B) -> append([[X, B]], Cells3, Cells4),
%        (ValueLB > 0, between(0, 9, L) -> append([[L, B]], Cells4, Cells5) ; Cells5 = Cells4, true),
%        (ValueRB > 0, between(0, 9, R) -> append([[R, B]], Cells5, Cells6) ; Cells6 = Cells5, true) ; Cells6 = Cells3, true),
%    (ValueL > 0, between(0, 9, L) -> append([[L, Y]], Cells6, Cells7) ; Cells7 = Cells6, true),
%    (ValueR > 0, between(0, 9, R) -> append([[R, Y]], Cells7, Cells8) ; Cells8 = Cells7, true),
%    current_wall_cells(Cells9),
%    add_distinct_elements(Cells9, Cells8, Res),
%    (\+ length(Res, 4) -> true; true),
%    retractall(current_wall_cells(_)),
%    assertz(current_wall_cells(Res)).

remove_item_from_list(_, [], []). % Base case: empty list, return empty list
remove_item_from_list(X, [X|T], R) :- remove_item_from_list(X, T, R). % If X is the head of the list, skip it
remove_item_from_list(X, [H|T], [H|R]) :- dif(H, X), remove_item_from_list(X, T, R). % If H is not X, keep it in the result list

add_distinct_elements(List1, List2, Result) :-
    list_to_set(List1, Set1),
    append(List2, Set1, Concatenated),
    list_to_set(Concatenated, Result).

not_last_move([X, Y]) :-
    last_move([L, M]),
    (L =\= X ; M =\= Y).

not_in_possible_cells([X, Y]) :-
    \+ member([X, Y], possible_cells).


clear_possible_cells :-
    retractall(possible_cells(_)),
    assertz(possible_cells([])).

define_last_move(Value) :-
    retractall(last_move(_)),
    assertz(last_move(Value)).

random_cell(Result) :-
    cells(Cells),
    random_member(Cell, Cells),
    Result = Cell.

remove_value_from_cells(Value) :-
    cells(Cells),
    select(Value, Cells, NewList),
    retract(cells(_)),
    assert(cells(NewList)).

update_element(Matrix, X, Y, Value, NewMatrix) :-
    nth0(Y, Matrix, Row, RestRows),
    nth0(X, Row, Element, RestRow),
    NewElement is Element + Value,
    nth0(X, NewRow, NewElement, RestRow),
    nth0(Y, NewMatrix, NewRow, RestRows).

update_matrix_item(Matrix, [X, Y], Value, NewMatrix) :-
    update_element(Matrix, X, Y, Value, NewMatrix),
    retractall(matrix(_)),
    assertz(matrix(NewMatrix)).

get_element(Matrix, X, Y, Value) :-
    nth0(Y, Matrix, MatrixRow),
    nth0(X, MatrixRow, Value).

get_matrix_value(Matrix, [X, Y], Value) :-
    get_element(Matrix, X, Y, Value).





