# Homework 1: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

### HW1
1. How is Breadth-first Search different in graphs than in trees?
    - Trees have no cycles meaning theres no need to have keep track of nodes that we've already seen as the structure assures no cycles.

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).
    - BFS can be used to find the shortest path to a point given multiple points. The structure of an algorithm allows it to go down and evaluate multiple paths meaning that you can keep track of distance between two target points.

### HW2
1. Compare and contrast Breadth-first Search and Depth-first Search by providing one similarity and one difference.
    - BFS and DFS are both ways of traversing a graph
    - DFS is typically implemeneted using a stack while BFS usually uses a queue

2. Explain why a Depth-first Search traversal does not necessarily find the shortest path between two vertices. What is one such example of a graph where a DFS search would not find the shortest path?

    - DFS may not find the shortest path due to the nature of the traversal it values depth over breadth. Meaning that the algorithm will go as far down a path as it can before backtracking and trying another. Say that we have A->B->C
    and we also have A->C. If during the traversal dfs goes down the path with B it will not return the shortest path.

3. Explain why we cannot perform a topological sort on a graph containing a cycle.