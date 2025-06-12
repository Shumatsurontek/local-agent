"""
Team routes for the API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from teams import collaborative_team

router = APIRouter()

# Available teams
TEAMS = {
    "collaborative": collaborative_team
}

class TeamChatRequest(BaseModel):
    message: str
    stream: bool = False

class TeamChatResponse(BaseModel):
    team_name: str
    response: str
    success: bool
    error: str = None

@router.get("/")
async def list_teams():
    """List all available teams"""
    return {
        "teams": {
            team_id: {
                "name": team.name,
                "description": team.description or f"{team.name} team",
                "members_count": len(team.members) if hasattr(team, 'members') else 0
            }
            for team_id, team in TEAMS.items()
        }
    }

@router.get("/{team_id}")
async def get_team_info(team_id: str):
    """Get information about a specific team"""
    if team_id not in TEAMS:
        raise HTTPException(status_code=404, detail=f"Team '{team_id}' not found")
    
    team = TEAMS[team_id]
    return {
        "id": team_id,
        "name": team.name,
        "description": team.description or f"{team.name} team",
        "mode": getattr(team, 'mode', 'unknown'),
        "members": [
            {
                "name": member.name,
                "description": member.description or f"{member.name} agent"
            }
            for member in team.members
        ] if hasattr(team, 'members') else [],
        "instructions": team.instructions
    }

@router.post("/{team_id}/chat")
async def chat_with_team(team_id: str, request: TeamChatRequest):
    """Chat with a specific team"""
    if team_id not in TEAMS:
        raise HTTPException(status_code=404, detail=f"Team '{team_id}' not found")
    
    try:
        team = TEAMS[team_id]
        response = team.run(request.message)
        
        return TeamChatResponse(
            team_name=team.name,
            response=response.content,
            success=True
        )
    except Exception as e:
        return TeamChatResponse(
            team_name=TEAMS[team_id].name,
            response="",
            success=False,
            error=str(e)
        ) 