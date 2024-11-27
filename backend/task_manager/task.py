import uuid
from datetime import datetime
from typing import Dict, Any

class Task:
    """Represents a task in the Teagardan framework."""

    def __init__(self, task_id: str = None, description: str = "", agent_id: int = None, status: str = "pending", priority: str = "medium", created_at: datetime = None, metrics: Dict[str, Any] = None, dependencies: List[str] = None):
        self.id = task_id or str(uuid.uuid4())  # Generate UUID if not provided.
        self.description = description
        self.agent_id = agent_id
        self.status = status
        self.priority = priority
        self.created_at = created_at or datetime.now()  # Use current time if not provided.
        self.metrics = metrics or {}  # Initialize metrics if not given.
        self.dependencies = dependencies or []  # Initialize dependencies list, used in phase 2.



    def to_dict(self) -> Dict[str, Any]:  #For easy serialization
        """Converts the Task object to a dictionary."""

        return {
            'id': self.id,
            'description': self.description,
            'agent_id': self.agent_id,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),  # Convert datetime to ISO string for JSON serialization
            'metrics': self.metrics,
            'dependencies': self.dependencies
        }