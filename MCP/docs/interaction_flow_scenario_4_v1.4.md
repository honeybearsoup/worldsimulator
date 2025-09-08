# AI TRPG 핵심 상호작용 흐름 - 시나리오 4 (v1.4 최종안)

## 1. 개요

본 문서는 플레이어의 장기적인 투자가 **'플레이어 주도 서사'**와 결합하여 세상에 어떤 영향을 미치는지를 정의합니다. 이 설계는 시스템이 '결과를 통보'하는 대신, 플레이어에게 **'사건을 제시'**하고 **'선택을 요구'**함으로써, 플레이어가 세상의 변화를 직접 이끌어가는 경험을 제공하는 데 중점을 둡니다.

## 2. 시나리오 4: 거점 투자와 플레이어 주도 위기 극복 (v1.4)

*   **플레이어 목표:** "이 마을을 더 안전하고 좋은 곳으로 만들고 싶다."
*   **핵심 데이터 객체:**
    *   `Project`: 프로젝트의 상태, `risk_factors` (위험 요소), `condition_tags` (상태 태그) 등을 포함하는 동적인 데이터.

---

### [흐름 1] 프로젝트 시작 및 '위험 요소' 정의

1.  **Player Action**: 마을 촌장에게 "낡은 망루를 재건하는 데 자금을 보태고 싶습니다."
2.  **`🏛️ 영지/세력 마스터 (LLM)`**:
    *   **Process**: 플레이어에게 프로젝트 개요를 브리핑하고, 자원 투입을 확인합니다.
    *   **Output (to `데이터 저장소`)**: `WorldState`에 새로운 `Project` 객체를 생성합니다. 이 객체에는 내재된 **위험 요소**가 포함됩니다.
        ```json
        {
          "active_projects": [{
            "project_id": "watchtower_rebuild",
            "status": "under_construction",
            "progress_points": 0,
            "required_points": 30,
            "condition_tags": ["newly_built"],
            "risk_factors": [
              {"type": "bandit_attack", "chance": 0.2, "impact_tags": ["damaged_wall"]},
              {"type": "bad_weather", "chance": 0.1, "impact_tags": ["delay_progress"]}
            ]
          }]
        }
        ```

---

### [흐름 2] 위험 촉발 및 '사건' 제시

1.  **Player Action**: 플레이어가 다른 모험을 떠나 15일의 시간을 보냅니다.
2.  **`📜 서사 엔진 (LLM)`**:
    *   **Input**: `simulate_downtime(elapsed_time="15_days")` 호출.
    *   **LLM Process**:
        1.  `Project`의 `progress_points`를 15 증가시킵니다.
        2.  `risk_factors`를 확인하고, `bandit_attack` 위험(20% 확률)에 대한 주사위를 굴립니다. **(성공 가정)**
        3.  위험이 '촉발'되었음을 인지합니다. **결과를 바로 적용하는 대신**, 담당 마스터에게 이 사건을 처리하도록 위임합니다.
    *   **Output (to `영지/세력 마스터`)**: "위험 촉발됨" 이벤트를 전달합니다.
        `{ "event": "risk_triggered", "project_id": "watchtower_rebuild", "risk_type": "bandit_attack" }`

---

### [흐름 3] 플레이어의 위기 개입 (선택과 결과)

1.  **`🏛️ 영지/세력 마스터 (LLM)`**:
    *   **Input**: `서사 엔진`으로부터 "위험 촉발됨" 이벤트를 받습니다.
    *   **LLM Process**: 이 추상적인 위험을 플레이어가 개입할 수 있는 구체적인 **'선택지'**로 변환합니다.
    *   **Output (to Player)**: 플레이어에게 편지를 보냅니다.
        > "후원자님께. 망루 건설 현장 주변에서 산적들의 움직임이 포착되었습니다. 이대로라면 건설 현장이 습격당할 위험이 있습니다. 어떻게 대응할까요?\n\n1. 용병을 고용하여 경비를 강화한다. (비용: 금화 100)\n2. 내가 직접 가서 처리하겠다. (연계 퀘스트 발생)\n3. 일단은 무시하고 건설을 강행한다. (프로젝트 파손 위험 감수)"
2.  **Player Action**: "내가 직접 가서 처리하겠다"를 선택합니다.
3.  **`🏛️ 영지/세력 마스터 (LLM)`**:
    *   **LLM Process**: 플레이어의 선택에 따라, '산적 소탕' 연계 퀘스트를 생성하고 `던전 마스터`에게 제어권을 넘깁니다.
    *   **결과**: 플레이어는 자신의 행동으로 위기를 직접 해결할 기회를 얻습니다. 프로젝트의 `integrity`는 이제 플레이어의 퀘스트 성공 여부에 따라 결정됩니다.

---

### [흐름 4] 프로젝트 완료와 구체적인 '상태 태그'

1.  **Player Action**: 플레이어가 산적 소탕 퀘스트를 성공적으로 마치고, 추가로 15일의 시간을 보냅니다.
2.  **`📜 서사 엔진 (LLM)`**:
    *   **Input**: `simulate_downtime(elapsed_time="15_days")`.
    *   **LLM Process**:
        1.  `progress_points`가 `required_points`에 도달하여, `status`를 `completed`로 변경합니다.
        2.  프로젝트의 최종 상태를 계산합니다. 플레이어가 위기를 성공적으로 막았으므로, `risk_factors`의 `impact_tags`가 적용되지 않았음을 확인합니다.
    *   **Output (to `데이터 저장소`)**:
        *   `world_modifiers`에 산적 활동률 감소 효과를 최대치(**-0.25**)로 적용합니다.
        *   완성된 망루 객체의 `condition_tags`는 `["newly_built", "well_defended"]`가 됩니다. (`damaged_wall` 태그가 추가되지 않음)

---

### [흐름 5] 세상의 변화 체감

*   **Player Action**: 마을로 돌아옵니다.
*   **`🏡 거점 마스터 (LLM)`**:
    *   **Input**: `get_narrative_context`를 통해 `watchtower_rebuilt` 플래그와 `condition_tags: ["well_defended"]`를 함께 받습니다.
    *   **LLM Process**: 이 구체적인 태그를 바탕으로 생생한 묘사를 생성합니다.
    *   **Output (to Player)**: "그림자 계곡으로 돌아오자, 언덕 위에 견고하고 위풍당당한 새로운 망루가 우뚝 솟아있습니다. 망루 꼭대기에는 당신이 고용한 용병단의 깃발이 자랑스럽게 펄럭이고 있습니다. 순찰 중인 경비병이 당신을 보더니 환한 미소와 함께 깍듯이 경례합니다. '돌아오셨군요, 영웅님! 당신 덕분에 이젠 산적 놈들 걱정 없이 두 발 뻗고 잘 수 있게 되었습니다.'"
