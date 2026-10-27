from collections import deque
import heapq
from itertools import count


class SearchResult:
    def __init__(self, path, expanded):
        self.path = path
        self.expanded = expanded


def reconstruct_path(parents, goal):
    path = []
    state = goal
    while state is not None:
        path.append(state)
        state = parents[state]
    path.reverse()
    return path


def bfs(campus, start, goal):
    frontier = deque([start])
    parents = {start: None}
    expanded = 0
    while frontier:
        state = frontier.popleft()
        if state == goal:
            return SearchResult(reconstruct_path(parents, goal), expanded)
        expanded += 1
        for action, successor in campus.neighbors(state):
            if successor not in parents:
                parents[successor] = state
                frontier.append(successor)
    return SearchResult(None, expanded)


def manhattan(state, goal):
    """TODO 1: Return Manhattan distance between two (row, column) tuples."""
    row, column = state
    goal_row, goal_column = goal
    return abs(row - goal_row) + abs(column - goal_column)


def astar(campus, start, goal):
    """TODO 2: Return SearchResult(path, expanded) for A* graph search."""
    # Keep possible locations in a priority queue where smaller a star score is checked first.
    order = count()
    # Each tuple is (estimated total cost(A star Score), tie-breaking order, cost so far, location).
    # Frontier is initialized with the start location, which has cost 0 and an estimated total cost equal to the Manhattan distance to the goal.
    frontier = [(manhattan(start, goal), next(order), 0, start)]

    # These dictionaries remember how we got to each location and the cheapest
    # cost we have found so far for getting there.
    parents = {start: None}
    best_costs = {start: 0}
    expanded = 0

    while frontier:
        # Get the next location with the lowest estimated total cost.
        item = heapq.heappop(frontier)
        _, _, cost_so_far, current = item

        # Ignore an old queue entry if we already found a cheaper way to its location.
        if cost_so_far != best_costs[current]:
            continue

        # Reaching the goal means we can rebuild and return the route.
        if current == goal:
            return SearchResult(reconstruct_path(parents, goal), expanded)

        # This location is being expanded as we look at its neighbors.
        expanded += 1
        neighbors = campus.neighbors(current)
        for _, neighbor in neighbors:
            # One step to a neighbor costs 1.
            new_cost = cost_so_far + 1

            # Save the neighbor only if this route is better than the old one.
            old_cost = best_costs.get(neighbor, float("inf"))
            if new_cost < old_cost:
                best_costs[neighbor] = new_cost
                parents[neighbor] = current

                # The score combines the cost so far with the distance to the goal.
                estimated_total = new_cost + manhattan(neighbor, goal)
                heapq.heappush(
                    frontier,
                    (estimated_total, next(order), new_cost, neighbor),
                )

    # The queue ran out, so there is no route from start to goal.
    return SearchResult(None, expanded)


def epsilon_greedy(q_values, state, actions, epsilon, rng):
    """TODO 3: Choose an action with epsilon-greedy exploration."""
    # Sometimes try any action to explore what it does.
    if rng.random() < epsilon:
        return rng.choice(actions)

    # Otherwise find the actions with the highest known value.
    best_value = max(q_values.get((state, action), 0.0) for action in actions)
    best_actions = [
        action for action in actions
        if q_values.get((state, action), 0.0) == best_value
    ]

    # Choose randomly among ties so the first listed action is not favored.
    return rng.choice(best_actions)


def q_learning_update(q_values, state, action, reward, next_state,
                      actions, alpha, gamma, terminal):
    """TODO 4: Update exactly one Q-table entry in place; return nothing."""
    old_value = q_values.get((state, action), 0.0)

    # A terminal action has no future reward after the current reward.
    if terminal:
        target = reward
    else:
        # Include all possible next actions; missing Q-values are zero.
        best_next_value = max(
            q_values.get((next_state, next_action), 0.0)
            for next_action in actions
        )
        target = reward + gamma * best_next_value

    # Move the old estimate partway toward the target and update this entry.
    q_values[(state, action)] = old_value + alpha * (target - old_value)
