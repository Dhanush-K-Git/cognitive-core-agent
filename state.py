import operator
from typing import Annotated, List, TypedDict

class AgentState(TypedDict):
    task: str
    plan: List[str]
    research_data: Annotated[List[str], operator.add]
    final_report: str