from pydantic import BaseModel, Field
from typing import Dict, Any


class RetrievalTool(BaseModel):
    """
    Represents the function that the AI can call to retrieve textbook content; 
    has parameters for the search query and returns relevant text chunks with source information
    """
    name: str = Field(default="search_knowledge_base")
    description: str = Field(default="Search the knowledge base for information related to the user's query")
    parameters: Dict[str, Any] = Field(default={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to find relevant information in the knowledge base"
            }
        },
        "required": ["query"]
    })

    class Config:
        json_schema_extra = {
            "example": {
                "name": "search_knowledge_base",
                "description": "Search the knowledge base for information related to the user's query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to find relevant information in the knowledge base"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

    def model_post_init(self, __context):
        # Validation: name must be a valid identifier
        if not self.name or not self.name.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Name must be a valid identifier")
        
        # Validation: parameters must follow JSON Schema format
        if not isinstance(self.parameters, dict):
            raise ValueError("Parameters must be a dictionary")
        
        if "type" not in self.parameters or self.parameters["type"] != "object":
            raise ValueError("Parameters must have type 'object'")
        
        if "properties" not in self.parameters:
            raise ValueError("Parameters must have 'properties' key")
        
        if "required" not in self.parameters:
            raise ValueError("Parameters must have 'required' key")