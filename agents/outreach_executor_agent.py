import logging
import uuid

class OutreachExecutorAgent:
    def __init__(self, mode='mocked', tools=None, instructions=''):
        self.mode = mode
        self.tools = tools or []
        self.instructions = instructions

    def run(self, inputs):
        logging.info("OutreachExecutorAgent.run() called")
        messages = inputs.get('messages', [])
        sent_status = []
        if self.mode == 'mocked':
            for m in messages:
                sent_status.append({
                    "lead": m.get("lead"),
                    "to": m.get("to_email"),
                    "status": "sent",
                    "message_id": str(uuid.uuid4())
                })
            campaign_id = str(uuid.uuid4())
            return {"sent_status": sent_status, "campaign_id": campaign_id}
        # TODO: integrate SendGrid / Apollo to send messages and return campaign_id, statuses
        raise NotImplementedError("OutreachExecutorAgent: live mode not implemented")

