class DomainMaster:
    def handle_investment(self, project_data: dict, player_request: dict) -> dict:
        return {"narrative": "Your investment is being considered.", "updated_state": project_data}
