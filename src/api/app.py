import os
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.api.models import QueryRequest, QueryResponse, ErrorResponse, HealthResponse
from src.agent import create_math_agent
from src import __version__


load_dotenv()

_agent_instance: Optional[object] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Inicializa o agente na startup e limpa recursos no shutdown.
    """
    global _agent_instance
    
    try:
        print("🚀 Inicializando AI Math Agent...")
        _agent_instance = create_math_agent(
            model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
            verbose=False
        )
        print("✅ Agente inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar agente: {str(e)}")
        _agent_instance = None
    
    yield
    
    _agent_instance = None
    print("👋 Agente encerrado.")


app = FastAPI(
    title="AI Math Agent API",
    description="API REST para o Agente Inteligente de Matemática baseado em ReAct",
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_agent():
    """
    Retorna a instância do agente.
    Cria uma nova instância se necessário (fallback).
    """
    global _agent_instance
    
    if _agent_instance is None:
        try:
            _agent_instance = create_math_agent(
                model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
                verbose=False
            )
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Agente não disponível: {str(e)}"
            )
    
    return _agent_instance


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "name": "AI Math Agent API",
        "version": __version__,
        "description": "API REST para o Agente Inteligente de Matemática baseado em ReAct",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint para verificar o status da API
    """
    try:
        agent = get_agent()
        return HealthResponse(
            status="healthy",
            version=__version__
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {str(e)}"
        )


@app.post("/query", response_model=QueryResponse, tags=["Agent"])
async def query_agent(request: QueryRequest):
    """
    Endpoint principal para consultar o agente.
    
    Recebe uma pergunta (matemática ou conhecimento geral) e retorna
    a resposta processada pelo agente ReAct.
    """
    try:
        agent = get_agent()
        
        if request.model_name or request.temperature is not None:
            temp_agent = create_math_agent(
                model_name=request.model_name or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                temperature=request.temperature if request.temperature is not None else float(os.getenv("OPENAI_TEMPERATURE", "0")),
                verbose=False
            )
            agent = temp_agent
        
        result = agent.invoke({"input": request.query})
        answer = result.get("output", "Não foi possível gerar uma resposta.")
        
        return QueryResponse(
            query=request.query,
            answer=answer
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar consulta: {str(e)}"
        )


