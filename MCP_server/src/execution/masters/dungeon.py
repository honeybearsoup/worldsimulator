class DungeonMaster:
    def handle_combat_action(self, combat_state: dict, player_action: str) -> dict:
        return {"narrative": "You swing your sword at the goblin!", "updated_state": combat_state}
