""""
Take a matrix of 1xm (m is number of tests) and each entry is an output state
Take a program
If the program matches k output states then it has a k/m chance of belonging to that equivalence class
If k > limit then we match the program to the equivalence class, and we increase the counter of the class
If k < limit then we create a new equivalence class

BUT - this way equivalence classes will not be updated :/
AND - as the algorithm progresses, we have more and more classes, meaning fewer and fewer programs will be explored
"""