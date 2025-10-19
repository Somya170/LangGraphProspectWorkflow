import logging

class ScoringAgent:
    def __init__(self, mode='mocked', tools=None, instructions=''):
        self.mode = mode
        self.tools = tools or []
        self.instructions = instructions

    def score_one(self, lead, criteria):
        # simple scoring example: normalize revenue & employees, weight signals
        revenue = lead.get('revenue', 0)
        employees = lead.get('employee_count', 0)
        signal = lead.get('signal')
        score = 0
        score += (min(revenue, 200000000) / 200000000) * criteria.get('revenue_weight', 0.4)
        score += (min(employees, 1000) / 1000) * criteria.get('employee_weight', 0.2)
        score += (0.0 if not signal else 1.0) * criteria.get('signal_weight', 0.4)
        return score

    def run(self, inputs):
        logging.info("ScoringAgent.run() called")
        enriched = inputs.get('enriched_leads', [])
        criteria = inputs.get('scoring_criteria', {"revenue_weight":0.4,"employee_weight":0.2,"signal_weight":0.4})
        ranked = []
        for lead in enriched:
            s = self.score_one(lead, criteria)
            item = {**lead, "score": round(s, 4)}
            ranked.append(item)
        ranked.sort(key=lambda x: x['score'], reverse=True)
        return {"ranked_leads": ranked}
