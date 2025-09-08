# AI TRPG 핵심 상호작용 흐름 v1.3

## 1. 개요

본 문서는 시스템의 핵심 철학인 **'추론이 아닌 관찰(Observation over Inference)'** 에 기반하여 상호작용 흐름을 정의합니다. 시스템은 플레이어의 마음을 억측하지 않고, 관찰 가능한 사실과 명시적인 행동에 기반하여 반응합니다.

이 버전(v1.3)은 **데이터 일관성**과 **시스템 반응성**을 보장하는 구체적인 메커니즘(이벤트 기반 캐시 무효화, 핵심 분기점 분석)을 도입하여, 정교함과 안정성 사이의 균형을 맞추는 데 중점을 둡니다.

## 2. 핵심 상호작용 시나리오

**시나리오 1: 새로운 도시에 도착하여 다음 할 일을 모색하기 (개선안 v1.3)**
시스템이 어떻게 플레이어의 누적된 행동을 객관적으로 분석하고, 이야기의 중요한 분기점에서 깊이 있는 서사를 제공하며, 데이터 일관성을 유지하는지 보여줍니다.

*   **플레이어 목표:** "새로운 도시에 도착했다. 여기서 뭘 해야 할지 알아보고 싶다."
*   **사전 조건 (상황):**
    1.  플레이어는 최근 며칠간 `["산적 소굴 토벌", "괴물 추격", "장거리 이동"]` 등 힘든 여정을 계속해왔습니다.
    2.  `서사 엔진`은 백그라운드에서 "알 수 없는 역병이 남부 지방에 퍼지기 시작함"이라는 월드 이벤트를 발생시켰고, 이와 관련된 `CacheInvalidationEvent`를 이벤트 버스에 발행했습니다.
*   **시작 상태:** 플레이어가 '벨라리아' 시의 성문에 도착. `거점 마스터`가 활성화됩니다.

---

### [흐름 1] 플레이어 입력 및 마스터의 1차 응답

*   **Player Action:** "드디어 벨라리아에 도착했군. 여기서 뭘 좀 할 수 있으려나?"
*   → **🏡 거점 마스터:**
    *   **Input:** 플레이어의 자연어 입력.
    *   **Process (Triage & Fast Response):**
        1.  **의도 분석:** 플레이어의 의도가 '주변 정보 탐색' 및 '새로운 활동 모색'임을 파악합니다.
        2.  **캐시 유효성 검사:** 최근 `CacheInvalidationEvent`를 수신했는지 확인합니다. '역병' 관련 이벤트가 있었지만, '도시의 일반적인 장소(선술집, 대장간 등)'에 대한 정보는 유효하다고 판단합니다.
        3.  **신속 응답:** 유효한 캐시 정보를 바탕으로, 도시에 대한 첫인상과 기본적인 장소들을 즉시 묘사하여 빠른 반응 속도를 제공합니다.
            > "거대한 성문이 여러분을 맞이합니다. 벨라리아의 활기찬 시장에서는 상인들의 외침이 들려오고, '취한 드래곤'이라는 간판을 단 선술집에서는 노랫소리가 흘러나옵니다."
        4.  **핵심 분기점 인지:** 플레이어가 '새로운 도시에 처음 도착'했다는 것을 **'핵심 분기점(Key Junction)'**으로 인지합니다. 이는 단순한 정보 조회를 넘어, 깊이 있는 서사 분석이 필요한 시점이라고 판단합니다.
    *   **Output (to 📜 서사 엔진):** `analyze_narrative_options_at_junction` MCP를 호출합니다.

---

### [흐름 2] 핵심 분기점에서의 심층 분석

*   **📜 서사 엔진:**
    *   **Input:** `거점 마스터`로부터 **데이터 계약**에 따른 `PlayerState`와 `JunctionContext`를 받습니다.
        *   **`PlayerState` (행동 기반 상태):** 플레이어의 '감정'을 추측하는 대신, '관찰된 사실'을 기록합니다.
            ```json
            {
              "recent_actions": [
                {"type": "combat", "intensity": "high", "count": 1},
                {"type": "chase", "duration": "long", "count": 1},
                {"type": "travel", "mode": "on_foot", "duration": "2_days"}
              ],
              "fatigue_level": 3, // 행동에 따라 계산된 객관적 피로도
              "last_rest_timestamp": "3_days_ago"
            }
            ```
    *   **Process (Strategic Analysis):**
        1.  **행동 상태 분석:** "플레이어의 캐릭터는 최근 휴식 없이 고강도 활동을 연달아 수행하여 육체적 피로도가 높다"고 객관적으로 판단합니다.
        2.  **전략적 제안:** 현재 월드 이벤트('역병의 시작')와 플레이어의 상태(피로함)를 종합적으로 고려하여, 여러 갈래의 가능한 서사 줄기를 '전략적 제안'으로 생성합니다.
    *   **Output (to 🏡 거점 마스터):** 각 제안에 대한 '이유'와 '연출 힌트'가 포함된 객체를 반환합니다.
        ```json
        {
          "strategic_suggestions": [
            {
              "type": "rest_and_gather_info",
              "title": "휴식 및 정보 수집",
              "reasoning": "Player fatigue is high. A low-intensity activity is recommended.",
              "hook": "The 'Whispering Apothecary' is known for restorative potions and is a hub for rumors about a strange illness."
            },
            {
              "type": "immediate_action",
              "title": "도시 경비대 지원",
              "reasoning": "High-risk, high-reward. Connects player to the city's power structure quickly.",
              "hook": "The city guard captain is recruiting skilled adventurers to investigate recent disturbances near the city walls."
            }
          ]
        }
        ```

---

### [흐름 3] 마스터의 전술적 연출 및 선택지 제공

*   **🏡 거점 마스터:**
    *   **Input:** `서사 엔진`의 전략적 제안을 받습니다.
    *   **Process (Tactical Execution):**
        1.  **연출 결정:** `서사 엔진`이 제안한 두 가지 큰 방향성을 바탕으로, 구체적인 장면을 어떻게 연출할지 결정합니다. 예를 들어, '휴식 및 정보 수집' 제안을 채택하여, 약제상을 통해 '역병'이라는 세계관의 중요 단서를 자연스럽게 노출하기로 합니다.
        2.  **장면 생성:** 플레이어에게 선택지를 제공하기 위한 구체적인 묘사를 생성합니다.
    *   **Output (to Player):** 플레이어가 다음에 취할 행동을 선택할 수 있도록, 명확한 선택지가 포함된 텍스트를 전달합니다.
        > "지친 몸을 이끌고 도시를 둘러보던 중, 약초 냄새가 물씬 풍기는 '속삭이는 약제상'이라는 가게와, 도시 성벽으로 향하는 경비대 순찰대의 모습이 눈에 띕니다. 어떻게 하시겠습니까?\n\n1. 약제상에 들어가 휴식을 취하며 정보를 얻는다.\n2. 경비대에게 다가가 무슨 일인지 알아본다."
