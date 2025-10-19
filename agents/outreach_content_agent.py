import logging
import os
# optional: import openai for live mode

class OutreachContentAgent:
    def __init__(self, mode='mocked', tools=None, instructions=''):
        self.mode = mode
        self.tools = tools or []
        self.instructions = instructions
        # if live mode and OpenAI used, set client here (not implemented)

    def generate_message_mock(self, lead, persona, tone):
        name = lead.get('contact', lead.get('contact_name', 'there'))
        company = lead.get('company')
        body = (f"Hi {name},\n\n"
                f"I noticed {company} is doing great work in the {lead.get('technologies','tech')} space. "
                "At Analytos.ai we help SaaS teams improve pipeline generation by identifying the best-fit accounts and outreach. "
                "Would you be open to a short 15-minute chat next week?\n\nBest,\nSomya (Analytos.ai)")
        return body

    def run(self, inputs):
        logging.info("OutreachContentAgent.run() called")
        ranked = inputs.get('ranked_leads', [])
        persona = inputs.get('persona', 'SDR')
        tone = inputs.get('tone', 'friendly')
        messages = []
        if self.mode == 'mocked':
            for r in ranked:
                body = self.generate_message_mock(r, persona, tone)
                messages.append({"lead": r.get("company"), "to_email": r.get("email"), "email_body": body})
            return {"messages": messages}
        # TODO: call OpenAI to craft personalized messages in live mode
        raise NotImplementedError("OutreachContentAgent: live mode not implemented")
