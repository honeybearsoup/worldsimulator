from fastapi import FastAPI
from .control.orchestrator import Orchestrator
from .data.models import PlayerActionInput, ServerResponse

app = FastAPI(
    title="MCP AI TRPG Server",
    description="A server to manage and run AI-powered TRPG sessions.",
    version="0.1.0"
)

orchestrator = Orchestrator()

@app.post("/action", response_model=ServerResponse)
def handle_action(action_input: PlayerActionInput):
    """
    This is the main entry point for all player actions.
    It receives the player's text and routes it through the orchestrator.
    """
    narrative_response = orchestrator.handle_player_action(action_input.text)

    return ServerResponse(
        narrative=narrative_response,
        game_state_updates={}
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the MCP AI TRPG Server. Use the /docs endpoint for the API."}
