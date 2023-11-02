:- dynamic cells/1.
:- dynamic matrix/1.
:- dynamic original_matrix/1.
:- dynamic last_move/1.
:- dynamic possible_cells/1.


% cells with hp: 1-3
% unknown cells: 0
% nontargetable cells: -1`


last_move.
possible_cells([]).
did_found_current_wall_cells(false).
current_wall_cells([]).



%get_possible_cells(Cell, Cells) :-
%    matrix(M),
%    retractall(possible_cells(_)),
%    get_matrix_value(M, Cell, Value),
%
%    (Value =\= 0 ->
%        define_last_move(Cell),
%        define_possible_cells,
%        possible_cells(PosCells),
%        write(Value)
%        ;
%        PosCells = [],
%        true
%    ),
%    Cells = PosCells.

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

shoot(Cell, Data) :-
    shoot_(Cell),
    remove_destroyed_from_possible_cells(Cell),
    possible_cells(Cells),
    Data = Cells.

shoot_([X, Y]) :-
    matrix(M),
    define_last_move([X, Y]),
    get_element(M, X, Y, CellValue),
    (CellValue > 0 ->
        shoot_hit(M, X, Y, CellValue)
        ;
        shoot_miss(M, X, Y, _), true
    ).

remove_destroyed_from_possible_cells([X, Y]) :-
    matrix(M),
    possible_cells(PosCells),
    get_element(M, X, Y, CellValue),
    (once(member([X, Y], PosCells)), CellValue < 1 -> remove_value_from_possible_cells([X, Y]); true).

shoot_hit(M, X, Y, CellValue) :-
    NewCellValue is CellValue - 1,
    update_matrix_item(M, [X, Y], NewCellValue),
    define_possible_cells.

shoot_miss(M, X, Y, _) :-
    NewCellValue is -1,
    remove_value_from_cells([X, Y]),
    update_matrix_item(M, [X, Y], NewCellValue).


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
    (Value >= 1 -> append([[X, Y]], Cells0, Cells) ; Cells = Cells0, true),
    (ValueNY =\= -1, between(0, 9, NY), compare_cell_with_original_matrix([X, NY]), not_last_move([X, NY]), not_in_possible_cells([X, NY]) -> append([[X, NY]], Cells, Cells1) ; Cells1 = Cells, true),
    (ValueSY =\= -1, between(0, 9, SY), compare_cell_with_original_matrix([X, SY]), not_last_move([X, SY]), not_in_possible_cells([X, SY]) -> append([[X, SY]], Cells1, Cells2) ; Cells2 = Cells1, true),
    (ValueEX =\= -1, between(0, 9, EX), compare_cell_with_original_matrix([EX, Y]), not_last_move([EX, Y]), not_in_possible_cells([EX, Y]) -> append([[EX, Y]], Cells2, Cells3) ; Cells3 = Cells2, true),
    (ValueWX =\= -1, between(0, 9, WX), compare_cell_with_original_matrix([WX, Y]), not_last_move([WX, Y]), not_in_possible_cells([WX, Y]) -> append([[WX, Y]], Cells3, Cells4) ; Cells4 = Cells3, true),
    possible_cells(Cells5),
    add_distinct_elements(Cells5, Cells4, Res),
    retractall(possible_cells(_)),
    assertz(possible_cells(Res)).

compare_cell_with_original_matrix([X, Y]) :-
    matrix(M),
    original_matrix(O),
    get_matrix_value(M, [X, Y], Value),
    get_matrix_value(O, [X, Y], OrigValue),
    (OrigValue =:= 0, Value =:= 0 ; OrigValue =\= 0, Value =\= 0).

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

remove_value_from_possible_cells(Value) :-
    possible_cells(Cells),
    select(Value, Cells, NewList),
    write(NewList),
    retract(possible_cells(_)),
    assert(possible_cells(NewList)).

remove_value_from_cells(Value) :-
    cells(Cells),
    select(Value, Cells, NewList),
    retract(cells(_)),
    assert(cells(NewList)).

update_element(Matrix, X, Y, Value, NewMatrix) :-
    nth0(Y, Matrix, Row, RestRows),
    nth0(X, Row, _, RestRow),
    NewElement is Value,
    nth0(X, NewRow, NewElement, RestRow),
    nth0(Y, NewMatrix, NewRow, RestRows).

update_matrix_item(Matrix, [X, Y], Value) :-
    update_element(Matrix, X, Y, Value, NewMatrix),
    retractall(matrix(_)),
    assertz(matrix(NewMatrix)).

get_element(Matrix, X, Y, Value) :-
    nth0(Y, Matrix, MatrixRow),
    nth0(X, MatrixRow, Value).

get_matrix_value(Matrix, [X, Y], Value) :-
    get_element(Matrix, X, Y, Value).





