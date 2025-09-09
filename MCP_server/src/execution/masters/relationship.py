class RelationshipMaster:
    def handle_conversation(self, relationship_state: dict, player_dialogue: str) -> dict:
        return {"narrative": "The NPC looks at you thoughtfully.", "updated_state": relationship_state}
