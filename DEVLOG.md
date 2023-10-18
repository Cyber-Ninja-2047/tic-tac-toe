# 2023-10-18

Completed the class Node, including features below:

* storing important properties:
  1. board status
  2. current turn
  3. parent node
  4. child nodes
* when the node is instantiated, automatically determine whether the node is terminal state and the winner of the node.

* the "expand" method, to generate and return all child nodes.

The users only need to instantiate the Node once. Then access the properties "terminated" and "winner" to check the status, or call method "expand" to get nodes in the next layer instead of to calculate board status manually every time.

