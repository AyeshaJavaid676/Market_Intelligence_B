class TokenTracker:
    def __init__(self):
        self.usage = {
            'Researcher': {'tokens': 0, 'cost': 0},
            'Strategist': {'tokens': 0, 'cost': 0},
            'Writer': {'tokens': 0, 'cost': 0},
            'Critic': {'tokens': 0, 'cost': 0}
        }
        # Groq is FREE! But we still track tokens for metrics
        self.cost_per_1k_tokens = 0  # FREE!
    
    def add_usage(self, agent, tokens):
        self.usage[agent]['tokens'] += tokens
        self.usage[agent]['cost'] = 0  # FREE!
    
    def get_total_cost(self):
        return 0  # FREE!
    
    def get_total_tokens(self):
        return sum(a['tokens'] for a in self.usage.values())