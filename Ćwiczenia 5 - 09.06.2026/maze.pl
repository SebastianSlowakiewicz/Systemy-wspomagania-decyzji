%maze.pl
% A program that finds a path through a maze

solve_maze :- path([start],Solution), write(Solution).

path([finish|RestOfPath],[finish|RestOfPath]).
path([CurrentLocation|RestOfPath],Solution):-
	connected_to(CurrentLocation,NextLocation),
	\+ member(NextLocation,RestOfPath),
	path([NextLocation,CurrentLocation|RestOfPath],Solution).

connected_to(Location1,Location2):- connect(Location1,Location2).
connected_to(Location1,Location2):- connect(Location2,Location1).