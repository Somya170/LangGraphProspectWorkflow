import logging
import random

class ProspectSearchAgent:
    def __init__(self, mode='mocked', tools=None, instructions=''):
        self.mode = mode
        self.tools = tools or []
        self.instructions = instructions

    def run(self, inputs):
        logging.info("ProspectSearchAgent.run() called")
        if self.mode == 'mocked':
            icp = inputs.get('icp', {})
            signals = inputs.get('signals', [])
            # produce 4 mock leads
            leads = []
            for i in range(4):
                leads.append({
                    "company": f"{icp.get('industry','Company')}-{i}",
                    "contact_name": f"Contact {i}",
                    "email": f"contact{i}@example{i}.com",
                    "linkedin": f"https://linkedin.com/in/contact{i}",
                    "signal": random.choice(signals) if signals else "none",
                    "employee_count": 100 + i*50,
                    "revenue": 25000000 + i*5000000
                })
            return {"leads": leads}
        # TODO: implement Clay / Apollo API calls (live mode)
        raise NotImplementedError("ProspectSearchAgent: live mode not implemented")
