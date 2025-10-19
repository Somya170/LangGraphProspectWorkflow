import logging
import random

class ResponseTrackerAgent:
    def __init__(self, mode='mocked', tools=None, instructions=''):
        self.mode = mode
        self.tools = tools or []
        self.instructions = instructions

    def run(self, inputs):
        logging.info("ResponseTrackerAgent.run() called")
        campaign_id = inputs.get('campaign_id')
        # mocked: generate some opens and occasional replies
        if self.mode == 'mocked':
            responses = [
                {"message_id": "m1", "status": "opened"},
                {"message_id": "m2", "status": "replied", "reply": "Yes, share more details"},
                {"message_id": "m3", "status": "bounced"}
            ]
            return {"responses": responses}
        # TODO: poll Apollo or SendGrid events in live mode
        raise NotImplementedError("ResponseTrackerAgent: live mode not implemented")
