from pydantic import BaseModel
from typing import List, Dict, Any

# Core Data Objects
class Stats(BaseModel):
    strength: int
    dexterity: int
    wisdom: int

class InventoryItem(BaseModel):
    item_id: str
    quantity: int

class RecentAction(BaseModel):
    action_type: str
    timestamp: str
    details: Dict[str, Any]

class PlayerState(BaseModel):
    player_id: str
    name: str
    stats: Stats
    inventory: List[InventoryItem]
    fatigue_level: int
    last_rest_timestamp: str
    recent_actions: List[RecentAction]

class RelationshipVectors(BaseModel):
    trust: int
    empathy: int
    respect: int
    fear: int

class RelationshipState(BaseModel):
    relationship_id: str
    npc_id: str
    vectors: RelationshipVectors
    emotional_state: str
    known_topics: List[str]
    is_suspicious: bool

class RiskFactor(BaseModel):
    type: str
    chance: float
    impact_tags: List[str]

class Project(BaseModel):
    project_id: str
    initiator: str
    status: str
    progress_points: int
    required_points: int
    condition_tags: List[str]
    risk_factors: List[RiskFactor]
    tags: List[str]
    funding_needed: int

class Trigger(BaseModel):
    source_type: str
    target_id: str
    keywords: List[str]

class StoryHook(BaseModel):
    hook_id: str
    related_quest_id: str
    urgency: str
    triggers: List[Trigger]

class TimedEvent(BaseModel):
    event_id: str
    type: str
    details: Dict[str, Any]
    delay: str
    priority: int
    conditions: List[str]

# API Data Models
class PlayerActionInput(BaseModel):
    player_id: str
    session_id: str
    text: str

class ServerResponse(BaseModel):
    narrative: str
    game_state_updates: Dict[str, Any]

# MCP Interface Contracts
class HandOffToMaster(BaseModel):
    intent: str
    confidence: float
    target_master: str
    context: Dict[str, Any]

class StrategicSuggestion(BaseModel):
    type: str
    title: str
    reasoning: str
    hook: str

class AnalyzeNarrativeOptionsOutput(BaseModel):
    strategic_suggestions: List[StrategicSuggestion]

class RiskTriggeredEvent(BaseModel):
    event: str = "risk_triggered"
    project_id: str
    risk_type: str

class RelationshipUpdate(BaseModel):
    field: str
    operation: str
    value: Any

class UpdateRelationshipStateInput(BaseModel):
    relationship_id: str
    updates: List[RelationshipUpdate]
