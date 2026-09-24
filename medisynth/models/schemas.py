from pydantic import BaseModel, Field
from typing import List


class Finding(BaseModel):
    finding: str
    evidence: str
    confidence: float = Field(ge=0.0, le=1.0)


class AgentAnalysis(BaseModel):
    agent: str
    findings: List[Finding]
    possible_conditions: List[str]
    uncertainties: List[str]
    contradictions: List[str]
    
    
class DebateResult(BaseModel):
    topic: str
    participants: List[str]
    positions: List[str]
    evidence: List[str]
    responses: List[str]
    revised_positions: List[str]
    conclusion: str
    
    
class ConsensusResult(BaseModel):
    consensus: str
    differential: List[str]
    supporting_evidence: List[str]
    unresolved_conflicts: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_gaps: List[str]