:- dynamic cells/1.
:- dynamic matrix/1.
:- dynamic wall_cells/1.


test2(Res, X):-
    X = Res.
%    wall_cells(Cells),
%    Res is Cells.











%find_targets_in_a_matrix(AllTargets):-
%    matrix(Matrix),
%    find_targets_xs(Matrix, AllTargets).
%
%find_targets_coorinates_([_], _).
%find_targets_coorinates_([Xs1, Xs2 | Rest], Y):-
%    FirstTwo = [Xs1, Xs2],
%    write(FirstTwo), write("  "), write(Y), nl,
%    NextY is Y + 1,
%    find_targets_coorinates_([Xs2 | Rest], NextY).
%
%find_targets_coorinates(Xs):-
%    once(find_targets_coorinates_(Xs, 0)).
%
%check_common_in_xs([],_).
%check_common_in_xs([X|Rest], Xs2):-
%    (once(member(X, Xs2)) -> write(X), nl; true),
%    check_common_in_xs(Rest, Xs2).
%
%find_targets_xs([],[]).
%find_targets_xs([Row|Rest], AllTargets):-
%    find_xs(Row, RowTargets),
%    find_targets_xs(Rest, NewTargets),
%    AllTargets = [RowTargets|NewTargets].
%
%find_xs(Row, Targets):-
%    findall(Index, (nth0(Index, Row, Value), Value > 0), Targets).
