from ..execution.masters.hub import HubMaster

class Orchestrator:
    def __init__(self):
        self.hub_master = HubMaster()

    def handle_player_action(self, player_input: str) -> str:
        # For this skeleton, we route directly to the HubMaster.
        narrative_context = {"location": "entry_tavern"}
        return self.hub_master.generate_narrative(narrative_context)
