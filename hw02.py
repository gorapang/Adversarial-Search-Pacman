from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):

    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)



class MinimaxAgent(AdversialSearchAgent):
  """
    [문제 01] MiniMaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    def is_game_over(gameState, depth):
      return gameState.isWin() or gameState.isLose() or depth == self.depth


    def max_value(gameState, depth): # 팩맨(MAX)의 최선의 선택 (최댓값)
      if is_game_over(gameState, depth):
        return self.evaluationFunction(gameState)
      
      legal_actions = gameState.getLegalActions()

      # 팩맨(에이전트 0)이 할 수 있는 모든 동작에 대해 min_agent를 호출한 뒤, 그 중 가장 큰 값을 반환
      max_result = max([min_value(gameState.generateSuccessor(0, action), depth, 1) for action in legal_actions])
      return max_result


    def min_value(gameState, depth, idx): # 유령(MIN)의 최선의 선택 (최솟값)
      if is_game_over(gameState, depth):
        return self.evaluationFunction(gameState)
      
      legal_actions = gameState.getLegalActions(idx)

      def next_action(action):
        if (idx == gameState.getNumAgents() - 1): # 모든 유령이 움직인 경우, 다음 깊이로 넘어가 max_agent 호출 (다시 팩맨의 action)
          return max_value(gameState.generateSuccessor(idx, action), depth+1)
        else: # 아직 움직이지 않은 유령이 있다면, 다음 유령의 인덱스로 min_agent 호출
          return min_value(gameState.generateSuccessor(idx, action), depth, idx+1)

      # 가능한 동작 중 가장 작은 값을 반환
      min_result = min(next_action(action) for action in legal_actions)
      return min_result


    legal_actions = gameState.getLegalActions()

    # 모든 동작에 대해 가능한 점수들
    scores = [min_value(gameState.generateSuccessor(0, action), 0, 1) for action in legal_actions]

    # 가능한 최고점
    best_score = max(scores)

    # 최고점을 내는 동작의 index 중 하나를 랜덤으로 고른다
    final_index = random.choice([index for index in range(len(scores)) if scores[index] == best_score])

    return legal_actions[final_index]
  
    raise Exception("Not implemented yet")

    ############################################################################



class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBetaAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    def is_game_over(gameState, depth):
      return gameState.isWin() or gameState.isLose() or depth == self.depth
    

    def max_value(gameState, depth, alpha, beta): # 팩맨(MAX)의 최선의 선택 (최댓값)
      if is_game_over(gameState, depth):
        return self.evaluationFunction(gameState)
      
      legal_actions = gameState.getLegalActions()
      
      successor = []
      v = float("-inf")
      for action in legal_actions:
        v = min_agent(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)
        alpha = max(alpha, v)
        successor.append(v)
        if alpha > beta: # 팩맨의 최솟값이 유령의 최대값보다 크면 가지치기
          break

      return max(successor)
    

    def min_agent(gameState, depth, idx, alpha, beta): # 유령(MIN)의 최선의 선택 (최솟값)
      if is_game_over(gameState, depth):
        return self.evaluationFunction(gameState)
      legal_actions = gameState.getLegalActions(idx)

      successor = []
      v = float("inf")
      for action in legal_actions:
        if idx == gameState.getNumAgents() - 1: # 모든 에이전트가 동작한 경우
          v = max_value(gameState.generateSuccessor(idx, action), depth + 1, alpha, beta) # 깊이를 1 증가시킨다
        else: # 아직 유령 차례인 경우
          v = min_agent(gameState.generateSuccessor(idx, action), depth, idx + 1, alpha, beta) # 다음 인덱스의 에이전트로 넘어간다
        
        beta = min(beta, v)
        successor.append(v)
        if beta < alpha: # MAX의 최솟값보다 현재 최댓값이 작을 경우
          break # for문을 종료하여 남은 하위 노드들은 탐색하지 않음

      return min(successor)


    legal_actions = gameState.getLegalActions()

    alpha = float("-inf") # 팩맨(MAX)의 최솟값
    beta = float("inf") # 유령(MIN)의 최댓값

    # 모든 동작에 대해 가능한 점수들
    scores = [min_agent(gameState.generateSuccessor(0, action), 0, 1, alpha, beta) for action in legal_actions]
    
    #가능한 최고점
    best_score = max(scores)

    # 최고점을 내는 인덱스 중 하나를 랜덤으로 고른다
    final_index = random.choice([index for index in range(len(scores)) if scores[index] == best_score])

    return legal_actions[final_index]
  
    raise Exception("Not implemented yet")

    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] ExpectimaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    def is_game_over(gameState, depth):
      return gameState.isWin() or gameState.isLose() or depth == self.depth
    
    def max_value(gameState, depth):
      if is_game_over(gameState, depth):
        return self.evaluationFunction(gameState)
      
      legal_actions = gameState.getLegalActions()
      # 모든 가능한 행동에 대한 기댓값 중 가장 높은 것 반환
      return max([exp_value(gameState.generateSuccessor(0, action), depth, 1) for action in legal_actions])


    def exp_value(gameState, depth, idx):
      if is_game_over(gameState, depth):
        return self.evaluationFunction(gameState)
      
      v = 0
      legal_actions = gameState.getLegalActions(idx)

      for action in legal_actions:
        if idx == gameState.getNumAgents() - 1: # 모든 agent가 행동을 마친 경우
          v += max_value(gameState.generateSuccessor(idx, action), depth + 1) # 깊이를 1 증가시켜 max 호출하고 값을 v에 더한다
        else:
          v += exp_value(gameState.generateSuccessor(idx, action), depth, idx + 1) # 다음 에이전트로 넘어가 exp 호출하고 값을 v에 더한다

      exp_result = v / len(legal_actions)
      return exp_result  #기댓값 리턴

    legal_actions = gameState.getLegalActions()

    # 모든 동작에 대해 가능한 점수들
    scores = [exp_value(gameState.generateSuccessor(0, action), 0, 1) for action in legal_actions]

    # 가능한 최고점
    best_score = max(scores)

    # 최고점을 내는 인덱스 중 하나를 랜덤으로 고른다
    final_index = random.choice([index for index in range(len(scores)) if scores[index] == best_score])

    return legal_actions[final_index]













    raise Exception("Not implemented yet")
    ############################################################################
