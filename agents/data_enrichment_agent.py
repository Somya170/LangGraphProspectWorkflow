import logging

class DataEnrichmentAgent:
    def __init__(self, mode='mocked', tools=None, instructions=''):
        self.mode = mode
        self.tools = tools or []
        self.instructions = instructions

    def run(self, inputs):
        logging.info("DataEnrichmentAgent.run() called")
        leads = inputs.get('leads') or []
        enriched = []
        if self.mode == 'mocked':
            for l in leads:
                enriched.append({
                    "company": l.get("company"),
                    "contact": l.get("contact_name"),
                    "email": l.get("email"),
                    "role": "VP Sales",
                    "technologies": ["aws", "postgres"],
                    "employee_count": l.get("employee_count"),
                    "revenue": l.get("revenue"),
                    "linkedin": l.get("linkedin"),
                    "signal": l.get("signal")
                })
            return {"enriched_leads": enriched}
        # TODO: call Clearbit or PeopleDataLabs APIs in live mode
        raise NotImplementedError("DataEnrichmentAgent: live mode not implemented")
