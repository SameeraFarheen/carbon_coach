from google.adk.tools import ToolContext


def log_activity(
    category: str,
    description: str,
    emissions: float,
    unit: str,
    tool_context: ToolContext
) -> dict:
    """Save an activity in the current ADK session."""

    if emissions < 0:
        return {"error": "Emissions cannot be negative."}

    activities = tool_context.state.get("activities", [])

    activity = {
        "category": category,
        "description": description,
        "emissions": emissions,
        "unit": unit
    }

    activities.append(activity)
    tool_context.state["activities"] = activities

    return {
        "message": "Activity successfully recorded.",
        "activity": activity,
        "total_activities": len(activities)
    }


def get_activity_summary(
    tool_context: ToolContext
) -> dict:
    """Retrieve activities recorded in this session."""

    activities = tool_context.state.get("activities", [])

    return {
        "total_activities": len(activities),
        "activities": activities,
        "note": "Different emission units and scopes must be kept separate."
    }