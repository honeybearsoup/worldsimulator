# AI TRPG 핵심 상호작용 흐름 v1.2

## 1. 개요

본 문서는 데이터 스키마를 먼저 정의하는 대신, 시스템의 핵심적인 **상호작용 시나리오(Interaction Scenario)**와 그에 따른 **데이터 흐름(Data Flow)**을 먼저 정의합니다. 이 "흐름 우선 설계" 방식을 통해, 각 컴포넌트 간에 어떤 정보가 오고 가야 하는지를 명확히 하고, 이를 바탕으로 필요한 데이터 모델의 요구사항을 자연스럽게 도출하는 것을 목표로 합니다.

이 버전(v1.2)은 각 컴포넌트의 **역할과 책임을 명확히** 하고, **풍부한 데이터 계약(Data Contract)**을 통해 유연하고 지능적인 상호작용을 구현하는 데 중점을 둡니다.

## 2. 핵심 상호작용 시나리오

**시나리오 1: 거점에서 모험 확인하기 (개선안 v1.2)**
플레이어의 모호한 입력을 시스템이 어떻게 지능적으로 해석하고, 각 전문가 AI(마스터)의 재량권을 존중하며 서사적 맥락에 맞는 경험을 제공하는지 보여줍니다.

*   **플레이어 목표:** "새로운 할 일이 있는지 알아보고 싶다."
*   **시작 상태:** 플레이어는 `거점 마스터`가 활성화된 상태입니다.

---

### [흐름 1] 플레이어 입력 및 의도 분석

*   **Player Action:** "뭐 재밌는 일 없어?"
*   → **⚙️ 오케스트레이터 (Orchestrator):**
    *   **Input:** 플레이어의 자연어 입력.
    *   **Process:**
        1.  입력을 분석하여 가능성 있는 여러 의도와 그 확률을 도출합니다. (`{"type": "view_available_adventures", "probability": 0.7}`, `{"type": "hear_rumors", "probability": 0.25}`)
        2.  만약 모든 의도의 확률이 유의미하게 낮다면, 플레이어에게 의도를 명확히 하기 위한 질문을 생성합니다.
    *   **Output (to 🏡 거점 마스터):** 여러 가능성을 담은 분석 결과를 전달합니다.
        ```json
        {
          "intents": [
            {"type": "view_available_adventures", "probability": 0.7},
            {"type": "hear_rumors", "probability": 0.25}
          ],
          "context": {"location": "tavern"}
        }
        ```

---

### [흐름 2] 마스터의 재량적 판단 및 컨텍스트 요청

*   **🏡 거점 마스터:**
    *   **Input:** 오케스트레이터로부터 여러 의도가 포함된 분석 결과를 받습니다.
    *   **Process (Discretion):**
        1.  **재량권 행사:** "소문 듣기(hear_rumors)"는 심층적인 서사 분석이 필요 없는 가벼운 요청이라고 판단합니다. 자신이 보유한 **로컬 캐시(Local Cache)**에서 즉시 처리할 수 있는 소문 정보를 확인합니다.
        2.  **판단 및 에스컬레이션:** "모험 확인(view_available_adventures)"은 플레이어의 현재 상태와 더 깊은 서사적 맥락이 필요하다고 판단합니다. 이 부분에 대해서는 `서사 엔진`에게 **'전략적 분석'**을 요청하기로 결정합니다.
    *   **Output (to 📜 서사 엔진):** `analyze_narrative_options` MCP를 호출합니다. 이때, **데이터 계약(Data Contract)**에 따라 `PlayerState` 객체와 `RequestContext` 객체를 전달합니다.
        *   **`PlayerState` (서사 상태 벡터):** 단순한 플래그가 아닌, 플레이어의 상태를 다차원적으로 표현하는 풍부한 정보 객체입니다.
            ```json
            {
              "recent_history": {
                "last_quest_id": "save_the_village",
                "outcome": "pyrrhic_victory",
                "involved_npc_death": true
              },
              "inferred_sentiment": {
                "weariness": 0.8,
                "pride": 0.6
              }
            }
            ```

---

### [흐름 3] 전략적 분석 및 제안 생성

*   **📜 서사 엔진 (The Strategist):**
    *   **Input:** `거점 마스터`로부터 `PlayerState`와 `RequestContext`를 받습니다.
    *   **Process ('What' to do):**
        1.  **서사 상태 분석:** 플레이어의 `서사 상태 벡터`를 분석합니다. (예: "씁쓸한 승리를 경험했고, 피로감과 자부심이 공존하는군.")
        2.  **전략적 추천:** 현재 맥락에 가장 어울리는 모험을 **'추천'**하고, 어울리지 않는 모험의 우선순위를 낮춥니다. 단순히 긍정/부정 필터링을 넘어, '왜' 이 모험이 지금 적절한지에 대한 이유를 함께 고려합니다.
    *   **Output (to 🏡 거점 마스터):** `거점 마스터`가 최종 연출을 할 수 있도록, 구체적인 지시가 아닌 **'전략적 제안'**이 담긴 JSON 객체를 반환합니다.
        ```json
        {
          "strategic_suggestions": {
            "recommended_adventures": [
              {
                "adventure_id": "stolen_pie",
                "reasoning": "A low-stakes, lighthearted quest to counter recent weariness."
              }
            ],
            "deprioritized_adventures": [
              {
                "adventure_id": "goblin_cave",
                "reasoning": "Another high-stakes combat quest, may lead to burnout."
              }
            ]
          }
        }
        ```

---

### [흐름 4] 마스터의 전술적 연출 및 최종 응답

*   **🏡 거점 마스터 (The Tactician):**
    *   **Input:** `서사 엔진`의 전략적 제안과 자신이 캐시에서 찾은 소문 정보를 모두 받습니다.
    *   **Process ('How' to do it):**
        1.  **종합 및 최종 연출 결정:** `서사 엔진`의 제안('가벼운 퀘스트를 주어라')과 로컬 정보(소문)를 종합하여, 최종적인 장면을 어떻게 연출할지 **스스로 결정합니다.**
        2.  **창의적 실행:** 제안을 바탕으로, "마을 광대 '핍'이 울상을 지으며 다가와 자신의 파이를 도둑맞았다고 호소하는" 장면을 생성하기로 결정합니다. 이전에 캐시에서 찾은 "최근 오크들이 심상치 않다"는 소문은 선술집 주인의 입을 통해 전달하기로 합니다.
    *   **Output (to Player):** 최종적으로 생성된 텍스트 묘사와 선택지를 플레이어에게 전달합니다.
