from fastapi import APIRouter
from app.agent.agent import agent
from app.agent.agent_schema import AgentRequest
import uuid

router =  APIRouter()

@router.post("/agent")
def agent_chat(data: AgentRequest):

    """
    Main HTTP endpoint for the movie recommendation agent.
    thread_id identifies the conversation — send the same thread_id
    across multiple requests to maintain conversational memory.
    """

    # If not thread_id provided, generate one (new conversation). It is important to indicate to the client to insert the conversational id if he wants to continue with the previous conversation.
    thread_id = data.thread_id or str((uuid.uuid4()))
    result = agent(
        user_input = data.query,
        top_k = data.top_k,
        filters = data.filters,
        user_mode = data.user_mode or "smart",
        thread_id = thread_id,
    )

    print("AGENT RESULT:", result)

    return {
        "query": result.get("query"),
        "action": result.get("action"),
        "movies": result.get("movies", []),
        "filters": result.get("filters", {}),
        "user_mode": result.get("user_mode"),
        "thread_id": thread_id, # Return to the client to use it, if he wants to continue the same conversation
        "conversation_history": result.get("conversation_history", []),
        "explanation": result.get("explanation")
    }


