import os
import sys
import django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async
from datetime import datetime

# Add project path to sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetpython.settings')
django.setup()

from UserApp.models import User, OrganizingCommitee
from ConferenceApp.models import Conference
from SessionApp.models import Session

mcp = FastMCP(name="conference_server")

# a. List all conferences
@mcp.tool()
async def list_conferences() -> str:
    """List all conferences with their dates and themes."""
    
    @sync_to_async
    def _get_conferences():
        return list(Conference.objects.all().order_by('start_date'))
    
    conferences = await _get_conferences()
    if not conferences:
        return "No conferences found."
    
    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date}) - Theme: {c.get_theme_display()}"
        for c in conferences
    ])

# b. Get conference details by name
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""
    
    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
    
    conference = await _get_conference()
    
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    if not conference:
        return f"Conference '{name}' not found."
    
    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )

# c. List sessions for a specific conference
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""
    
    @sync_to_async
    def _get_sessions():
        try:
            conference = Conference.objects.get(name__icontains=conference_name)
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    
    result, conference = await _get_sessions()
    
    if result == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."
    if conference is None:
        return f"Conference '{conference_name}' not found."
    
    sessions = result
    if not sessions:
        return f"No sessions found for conference '{conference.name}'."
    
    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_date} - {s.end_date}) in {s.room}\n"
            f"  Topic: {s.topic}"
        )
    
    return "\n".join(session_list)

# d. Filter conferences by theme
@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """Filter conferences by theme (CS&IA, CS, or SE)."""
    
    @sync_to_async
    def _get_themed_conferences():
        return list(Conference.objects.filter(theme__icontains=theme).order_by('start_date'))
    
    conferences = await _get_themed_conferences()
    
    if not conferences:
        return f"No conferences found with theme matching '{theme}'."
    
    return "\n".join([
        f"- {c.name} ({c.location}) - {c.start_date} to {c.end_date}"
        for c in conferences
    ])

# e. Bonus: Get organizing committee for a conference
@mcp.tool()
async def get_conference_committee(conference_name: str) -> str:
    """Get organizing committee members for a conference."""
    
    @sync_to_async
    def _get_committee():
        try:
            conference = Conference.objects.get(name__icontains=conference_name)
            return conference, list(conference.commitees.select_related('user').all())
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    
    conference, members = await _get_committee()
    
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."
    if not conference:
        return f"Conference '{conference_name}' not found."
    
    if not members:
        return f"No committee members found for '{conference.name}'."
    
    committee_list = []
    for member in members:
        committee_list.append(
            f"- {member.user.get_full_name()} ({member.user.user_id}) - {member.get_commitee_role_display()} - Joined: {member.date_join}"
        )
    
    return f"Organizing Committee for '{conference.name}':\n" + "\n".join(committee_list)

# f. Bonus: List all users by role
@mcp.tool()
async def list_users_by_role(role: str) -> str:
    """List all users filtered by role (participant or commitee)."""
    
    @sync_to_async
    def _get_users():
        return list(User.objects.filter(role=role).order_by('last_name'))
    
    users = await _get_users()
    
    if not users:
        return f"No users found with role '{role}'."
    
    user_list = []
    for user in users:
        user_list.append(
            f"- {user.get_full_name()} ({user.user_id}) - {user.email}\n"
            f"  Affiliation: {user.affiliation} | Nationality: {user.nationality}"
        )
    
    return f"Users with role '{role}':\n" + "\n".join(user_list)

if __name__ == "__main__":
    mcp.run(transport="http")
