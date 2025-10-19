import logging

class FeedbackTrainerAgent:
    def __init__(self, mode='mocked', tools=None, instructions=''):
        self.mode = mode
        self.tools = tools or []
        self.instructions = instructions

    def run(self, inputs):
        logging.info("FeedbackTrainerAgent.run() called")
        responses = inputs.get('responses', [])
        opens = sum(1 for r in responses if r.get('status') == 'opened')
        replies = sum(1 for r in responses if r.get('status') == 'replied')
        total = max(1, len(responses))
        open_rate = opens / total
        reply_rate = replies / total
        recommendations = []
        # Simple rules for recommendations
        if open_rate < 0.2:
            recommendations.append({"area":"subject_line","suggestion":"Make subject benefit-led and short"})
        if reply_rate < 0.05:
            recommendations.append({"area":"call_to_action","suggestion":"Try offering a small time window and clear value in first sentence"})
        recommendations.append({"metrics":{"open_rate":open_rate,"reply_rate":reply_rate,"opens":opens,"replies":replies}})
        # TODO: write recommendations to Google Sheets in live mode and prompt human approval
        return {"recommendations": recommendations}
