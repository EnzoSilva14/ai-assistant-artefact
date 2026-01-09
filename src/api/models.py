from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """Modelo de requisição para consulta ao agente"""
    query: str = Field(..., description="Pergunta ou consulta a ser processada pelo agente", min_length=1)
    model_name: Optional[str] = Field(None, description="Nome do modelo OpenAI a usar (opcional)")
    temperature: Optional[float] = Field(None, description="Temperatura do modelo (opcional, padrão: 0)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Quanto é 128 vezes 46?",
                "model_name": "gpt-4o-mini",
                "temperature": 0.0
            }
        }


class QueryResponse(BaseModel):
    """Modelo de resposta da API"""
    answer: str = Field(..., description="Resposta do agente")
    query: str = Field(..., description="Consulta original")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Quanto é 128 vezes 46?",
                "answer": "O resultado de 128 × 46 é 5.888"
            }
        }


class ErrorResponse(BaseModel):
    """Modelo de resposta de erro"""
    error: str = Field(..., description="Mensagem de erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais do erro")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "OPENAI_API_KEY não encontrada",
                "detail": "Configure a variável de ambiente ou crie um arquivo .env"
            }
        }


class HealthResponse(BaseModel):
    """Modelo de resposta do health check"""
    status: str = Field(..., description="Status da API")
    version: str = Field(..., description="Versão da aplicação")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }
