"""Demo for the strands-acp-client GIF: a Strands agent hands a task to Claude Code over ACP.

    cd demos && python acp_demo.py

Needs: strands-agents and strands-acp-client installed, model access for the Strands agent
(Amazon Bedrock by default), and Claude Code signed in. The coding agent works read-only in
demos/sample, a tiny project with one bug.
"""
from pathlib import Path

from strands import Agent
from strands_acp_client import make_acp_agent

SAMPLE = Path(__file__).resolve().parent / "sample"

with make_acp_agent(agents=["claude"], cwd=str(SAMPLE), permissions="read_only") as acp_agent:
    agent = Agent(tools=[acp_agent])
    agent("Ask claude to find the bug in retry.py and explain it in two sentences.")
