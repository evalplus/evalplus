"""
Given a square matrix of size N*N given as a list of lists, where each cell is associated with a specific cost. A path is defined as a specific sequence of cells that starts from the top-left cell move only right or down and ends on bottom right cell. We want to find a path with the maximum average over all existing paths. Average is computed as total cost divided by the number of cells visited in the path.
"""

def maxAverageOfPath(cost):
  assert isinstance(cost, list), "invalid inputs" # $_CONTRACT_$
  assert len(cost) > 0, "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, list) for x in cost), "invalid inputs" # $_CONTRACT_$
  assert all(len(x) == len(cost) == len(cost[0]) for x in cost), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in sum(cost, [])), "invalid inputs" # $_CONTRACT_$
  N = len(cost)
  dp = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
  dp[0][0] = cost[0][0]
  for i in range(1, N):
    dp[i][0] = dp[i - 1][0] + cost[i][0]
  for j in range(1, N):
    dp[0][j] = dp[0][j - 1] + cost[0][j]
  for i in range(1, N):
    for j in range(1, N):
      dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) + cost[i][j]
  # all paths are of length 2 * N - 1, so just divide by that
  return dp[N - 1][N - 1] / (2 * N - 1)



assert maxAverageOfPath([[1, 2, 3], [6, 5, 4], [7, 3, 9]]) == 5.2
assert maxAverageOfPath([[2, 3, 4], [7, 6, 5], [8, 4, 10]]) == 6.2
assert maxAverageOfPath([[3, 4, 5], [8, 7, 6], [9, 5, 11]]) == 7.2
assert maxAverageOfPath([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 5.8
