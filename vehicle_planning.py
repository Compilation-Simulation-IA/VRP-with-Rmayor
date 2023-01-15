   

class VehiclePlanning:
    
    def _init__(self, initial, goals, actions, agent, domain = None):
        self.initial = initial if domain is None else initial + domain
        self.goals = goals
        self.actions = actions
        self.domain = domain
        self.agent = agent

    def goal_test(self, state):
        pass

    def expand_actions(self, state):
        pass

    def act(self, action):
        pass

   

   
