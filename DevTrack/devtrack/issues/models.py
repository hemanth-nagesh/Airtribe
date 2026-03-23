from django.db import models
from abc import ABC, abstractmethod
from datetime import datetime
# Create your models here.
class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }

class Reporter(BaseEntity):
    def __init__(self,id, name, email, team):
        super().__init__()
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name:
            raise ValueError('Name cannot be empty')
        if '@' not in self.email:
            raise ValueError('Invalid email')

class Issue(BaseEntity):
    # These are the only allowed values for status and priority
    VALID_STATUSES = ["open", "in_progress", "resolved", "closed"]
    VALID_PRIORITIES = ["low", "medium", "high", "critical"]

    def __init__(self, id, title, description, status, priority, reporter_id, created_at=None):
        super().__init__()
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = created_at or datetime.now().isoformat()

    def validate(self):
        # Check 1 — title must not be empty
        if not self.title:
            raise ValueError("Title cannot be empty")
 
        # Check 2 — status must be one of the 4 allowed values
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {self.VALID_STATUSES}")
 
        # Check 3 — priority must be one of the 4 allowed values
        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {self.VALID_PRIORITIES}")
 
        # Check 4 — reporter_id must be present
        if not self.reporter_id:
            raise ValueError("Reporter ID cannot be empty")
    def describe(self):
        return f"{self.title} [{self.priority}]"

class CriticalIssue(Issue):
    def describe(self):
        return f"URGENT: {self.title} - need immediate attention"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"Low Priority: {self.title} - can be addressed later"