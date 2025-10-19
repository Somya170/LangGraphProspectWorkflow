"""
langgraph_builder.py
Simple dynamic workflow executor for the provided workflow.json.

Usage:
    python langgraph_builder.py --workflow workflow.json --mode mocked
Modes:
    mocked - agents return fake data (good for demo)
    live   - agents should call real APIs (must implement)
"""
import argparse
import importlib
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import logging
from typing import Any

load_dotenv()
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

TEMPL_RE = re.compile(r"\$\{([^}]+)\}")

def camel_to_snake(name: str) -> str:
    # ProspectSearchAgent -> prospect_search_agent
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def resolve_template(value: Any, context: dict):
    # Recursively resolve strings like ${prospect_search.output.leads} or ${ENVVAR}
    if isinstance(value, str):
        def repl(match):
            path = match.group(1)
            parts = path.split('.')
            # config.*
            if parts[0] == 'config':
                # read from context['config']
                v = context.get('config', {})
                for p in parts[1:]:
                    v = v.get(p)
                return json.dumps(v) if not isinstance(v, str) else str(v)
            # env var fallback
            if len(parts) == 1 and os.getenv(parts[0]) is not None:
                return os.getenv(parts[0])
            # step.output...
            if parts[0] in context:
                v = context[parts[0]]
                for p in parts[1:]:
                    if isinstance(v, dict):
                        v = v.get(p)
                    else:
                        v = None
                return json.dumps(v) if not isinstance(v, str) else str(v)
            return ''
        new = TEMPL_RE.sub(repl, value)
        # Try to parse JSON literal if it looks like JSON
        try:
            parsed = json.loads(new)
            return parsed
        except Exception:
            return new
    elif isinstance(value, dict):
        return {k: resolve_template(v, context) for k, v in value.items()}
    elif isinstance(value, list):
        return [resolve_template(v, context) for v in value]
    else:
        return value

def load_workflow(path: str):
    raw = json.loads(Path(path).read_text())
    return raw

def dynamic_import_agent(agent_name: str):
    mod_name = camel_to_snake(agent_name)
    module_path = f"agents.{mod_name}"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise ImportError(f"Agent module not found: {module_path}") from e
    cls = getattr(module, agent_name, None)
    if cls is None:
        raise ImportError(f"Agent class {agent_name} not found in {module_path}")
    return cls

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workflow', default='workflow.json')
    parser.add_argument('--mode', choices=['mocked', 'live'], default='mocked')
    args = parser.parse_args()

    wf = load_workflow(args.workflow)
    logging.info(f"Loaded workflow: {wf.get('workflow_name')} - {wf.get('description')}")
    context = {}
    context['config'] = wf.get('config', {})

    for step in wf.get('steps', []):
        step_id = step['id']
        agent_name = step['agent']
        logging.info(f"--- Running step [{step_id}] -> Agent: {agent_name} ---")
        # Resolve inputs with context
        inputs_raw = step.get('inputs', {})
        resolved_inputs = resolve_template(inputs_raw, context)
        logging.info(f"Resolved inputs for {step_id}: {json.dumps(resolved_inputs, default=str)[:1000]}")
        # Load agent
        AgentClass = dynamic_import_agent(agent_name)
        agent = AgentClass(mode=args.mode, tools=step.get('tools', []), instructions=step.get('instructions', ''))
        try:
            output = agent.run(resolved_inputs)
        except Exception as e:
            logging.exception(f"Agent {agent_name} failed: {e}")
            output = {'error': str(e)}
        context[step_id] = {'output': output}
        logging.info(f"Step {step_id} output keys: {list(output.keys())}")
    logging.info("Workflow execution complete. Final context keys: " + ", ".join(context.keys()))

if __name__ == '__main__':
    main()
