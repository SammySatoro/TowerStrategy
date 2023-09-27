sum_of_digits(0, 0).
sum_of_digits(N, Sum) :-
    N > 0,
    Next is N // 10,
    Digit is N mod 10,
    sum_of_digits(Next, Rest),
    Sum is Digit + Rest.
