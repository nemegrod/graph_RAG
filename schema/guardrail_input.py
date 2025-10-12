from pydantic import BaseModel

class GuardrailAgentOutput(BaseModel):
  is_not_allowed: bool
  reason: str | None
