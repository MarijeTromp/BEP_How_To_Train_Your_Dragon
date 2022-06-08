""""
Take a matrix of 1xm (m is number of tests) and each entry is an output state
Take a program
If the program matches k output states then it has a k/m chance of belonging to that equivalence class
If k > limit then we match the program to the equivalence class, and we increase the counter of the class
If k < limit then we create a new equivalence class

BUT - this way equivalence classes will not be updated :/
AND - as the algorithm progresses, we have more and more classes, meaning fewer and fewer programs will be explored


observational equivalence pruning is mostly useful when it is not possible to reach a better state from that state
so if we apply x steps to the state, and it remains equal, then we can put the state in a "bad-list"
we use that "bad-list" for observational equivalence pruning.
Any time a state like that appears in the neighborhood, we ignore it
(and do not count is as part of the explore neighborhood, but that might cause empty neighborhoods and deadlocks)
(empty neighborhoods aren't the worst thing though, as there are iterations before we increase search depth)
(so deadlocks are actually unlikely (because of randomness the neighborhood changes each time))


simple implementation:
(IDEA: only prune on observational equivalence between direct neighbors)
(NOTE: this would only have effect on situations in which no improvement is found,
in which case the observationally equivalent neighbor would generally be chosen)
(PRO: saves space, easy to implement. CON: only very superficially applies pruning)
(QUESTION: how we (efficiently) retrieve the output states of a program?)
(QUESTION: how we efficiently save the output states of a program?)
(QUESTION: how do we determine *somechance*?)(ANSWER: by the number of the example worlds are equivalent)
explore neighborhood:
- i times
- - get neighbor
- - get neighbor's output state
- - if neighbor's cost < best neighbor's cost
- - - if output state of best neighbor !equals that of current solution
- - - - best neighbor = neighbor
- - - else (observationally equivalent) if *somechance*
- - - - best neighbor = neighbor
- ...continue with algorithm...

medium implementation:
(IDEA: compares the program's output states not only to predecessor's, but all states)
(PRO: compares more efficiently. CON: could use a lot of space and time, unsure if too much pruning)
explore neighborhood:
- i times
- - get neighbor
- - get neighbor's output state
- - if neighbor's cost < best neighbor's cost
- - - if output state of best neighbor !equals something in the explored-list
- - - - best neighbor = neighbor
- - - else (observationally equivalent to some older program)
- - - - increment counter for that equivalence class
- - - - best neighbor = neighbor with some chance (eg. 1/counter)
- ...continue with algorithm...

explored-list: (PROBLEM: how do we efficiently keep this map? it could be huge)
- hashmap
- keys: example world
- values: tuple(counter, explored state)

dead-end implementation: (USELESS IMPLEMENTATION)
(problem is that pruning on observational equivalence on dead states is
that using a counter to bring in stochasticity is useless, as any dead state
should not be explored)
(NOTE: this won't work at all, because a dead end in the VLNS algorithm is a general dead end.
VLNS has no backtracking... So this would go wrong at the very first dead end
(which is unlikely to even occur at all, making the technique useless))

explore neighborhood:
- i times
- - get neighbor
- - get neighbor's output state
- - if output state is in dead-list
- - - continue (skips one iteration of the loop)
- - if neighbor's cost < best neighbor's cost
- - - best neighbor = neighbor
- ...continue with algorithm...

applying x steps:
- save the old program
- do x times:
- - program = repair(destroy(program))
- if program = old program (observational equivalence)
- then we have dead end
- add program's output state to bad-list
- increment counter of that entry in dead-list

dead-list:
- hashmap
- keys: example world
- values: dead states

"""