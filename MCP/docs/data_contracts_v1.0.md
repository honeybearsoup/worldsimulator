# MCP - 데이터 계약서 v1.0

## 1. 개요 (Overview)
본 문서는 MCP 시스템의 컴포넌트 간에 교환되는 모든 주요 JSON 객체의 구조, 필드, 데이터 타입을 정의하는 '단일 진실 공급원(Single Source of Truth)'입니다. 모든 컴포넌트는 본 문서에 정의된 데이터 계약을 준수하여 통신해야 합니다.

---

## 2. 핵심 데이터 객체 (Core Data Objects)
`데이터 저장소(Data Store)`에 저장되거나, 컴포넌트 간에 자주 전달되는 핵심적인 데이터들의 스키마를 정의합니다.

### 2.1. `PlayerState`
플레이어 캐릭터의 현재 상태와 누적된 행동 기록을 나타냅니다.
```json
{
  "player_id": "string",
  "name": "string",
  "stats": {
    "strength": "integer",
    "dexterity": "integer",
    "wisdom": "integer"
  },
  "inventory": [
    { "item_id": "string", "quantity": "integer" }
  ],
  "fatigue_level": "integer",
  "last_rest_timestamp": "string",
  "recent_actions": [
    {
      "action_type": "string",
      "timestamp": "string",
      "details": "object"
    }
  ]
}
```

### 2.2. `RelationshipState`
특정 NPC와 플레이어 간의 다차원적 관계를 나타냅니다.
```json
{
  "relationship_id": "string",
  "npc_id": "string",
  "vectors": {
    "trust": "integer",
    "empathy": "integer",
    "respect": "integer",
    "fear": "integer"
  },
  "emotional_state": "string",
  "known_topics": ["string"],
  "is_suspicious": "boolean"
}
```

### 2.3. `Project`
월드에서 진행 중인 장기 프로젝트의 상태를 나타냅니다.
```json
{
  "project_id": "string",
  "initiator": "string",
  "status": "string",
  "progress_points": "integer",
  "required_points": "integer",
  "condition_tags": ["string"],
  "risk_factors": [
    {
      "type": "string",
      "chance": "float",
      "impact_tags": ["string"]
    }
  ],
  "tags": ["string"],
  "funding_needed": "integer"
}
```

### 2.4. `StoryHook`
서사 분기점의 '진입로'를 정의하는 객체입니다.
```json
{
  "hook_id": "string",
  "related_quest_id": "string",
  "urgency": "string",
  "triggers": [
    {
      "source_type": "string",
      "target_id": "string",
      "keywords": ["string"]
    }
  ]
}
```

### 2.5. `TimedEvent`
`서사 엔진`의 이벤트 큐에 들어가는 이벤트 객체입니다.
```json
{
  "event_id": "string",
  "type": "string",
  "details": "object",
  "delay": "string",
  "priority": "integer",
  "conditions": ["string"]
}
```

---

## 3. MCP 인터페이스 계약 (MCP Interface Contracts)

### 3.1. `Orchestrator` 출력
`오케스트레이터`가 전문 마스터에게 작업을 위임할 때 사용하는 `HandOffToMaster` 객체입니다.
```json
{
  "intent": "string",
  "confidence": "float",
  "target_master": "string",
  "context": "object"
}
```

### 3.2. `NarrativeEngine` 인터페이스
`서사 엔진`이 호출되거나, 이벤트를 발생시킬 때의 데이터 계약입니다.

*   `analyze_narrative_options_at_junction` **Input**:
    ```json
    {
      "player_state": "PlayerState",
      "junction_context": {
        "location_id": "string",
        "is_first_visit": "boolean"
      }
    }
    ```
*   `analyze_narrative_options_at_junction` **Output**:
    ```json
    {
      "strategic_suggestions": [
        {
          "type": "string",
          "title": "string",
          "reasoning": "string",
          "hook": "string"
        }
      ]
    }
    ```
*   `risk_triggered` 이벤트 객체:
    ```json
    {
      "event": "risk_triggered",
      "project_id": "string",
      "risk_type": "string"
    }
    ```

### 3.3. `RelationshipMaster` 인터페이스
`관계 마스터`가 `데이터 저장소`의 상태를 변경할 때의 데이터 계약입니다.

*   `update_relationship_state` **Input**:
    ```json
    {
      "relationship_id": "string",
      "updates": [
        {
          "field": "string",
          "operation": "string",
          "value": "any"
        }
      ]
    }
    ```
