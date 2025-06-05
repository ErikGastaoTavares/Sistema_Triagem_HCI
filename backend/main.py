from fastapi import FastAPI, HTTPException, Depends, status, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import uuid
from datetime import datetime
import os
import torch
import chromadb
from dotenv import load_dotenv
import json
import logging

# Importar serviços otimizados
from embedding_service import EmbeddingService
from ollama_service import OllamaService

# Importar módulos de usuários
from rotas_usuarios import router as usuarios_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("triagem_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("triagem_api")

# Initialize FastAPI app
app = FastAPI(
    title="Sistema de Triagem API",
    description="API para o Sistema de Triagem baseado no Protocolo de Manchester",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas de usuários
app.include_router(usuarios_router)

# Inicializar serviços
try:
    embedding_service = EmbeddingService()
    logger.info("Serviço de embeddings inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar serviço de embeddings: {str(e)}")
    embedding_service = None

try:
    ollama_service = OllamaService()
    logger.info("Serviço Ollama inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar serviço Ollama: {str(e)}")
    ollama_service = None

# Initialize ChromaDB
try:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection_name = "triagem_hci"
    
    try:
        collection = chroma_client.get_collection(name=collection_name)
        logger.info(f"Coleção ChromaDB '{collection_name}' carregada com sucesso")
    except ValueError:
        collection = chroma_client.create_collection(name=collection_name)
        logger.info(f"Coleção ChromaDB '{collection_name}' criada com sucesso")
    except Exception:
        try:
            collection = chroma_client.create_collection(name=collection_name)
            logger.info(f"Coleção ChromaDB '{collection_name}' criada com sucesso após erro")
        except:
            collection = chroma_client.get_collection(name=collection_name)
            logger.info(f"Coleção ChromaDB '{collection_name}' carregada com sucesso após erro")
except Exception as e:
    logger.error(f"Erro ao inicializar ChromaDB: {str(e)}")
    collection = None

# Pydantic models
class TriagemRequest(BaseModel):
    sintomas: str
    classificacao: str = None
    justificativa: str = None
    condutas: str = None

class TriagemProcessar(BaseModel):
    sintomas: str

class TriagemResponse(BaseModel):
    id: str
    sintomas: str
    resposta: str
    classificacao: str
    justificativa: str
    condutas: str
    data_hora: str

class ValidationRequest(BaseModel):
    triagem_id: str
    validado_por: str
    feedback: str

class ValidationResponse(BaseModel):
    success: bool
    message: str

# Database functions
def init_validation_db():
    conn = sqlite3.connect('./validacao_triagem.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS validacao_triagem (
        id TEXT PRIMARY KEY,
        sintomas TEXT NOT NULL,
        resposta TEXT NOT NULL,
        data_hora TEXT NOT NULL,
        validado INTEGER DEFAULT 0,
        feedback TEXT,
        validado_por TEXT,
        data_validacao TEXT,
        classificacao TEXT,
        justificativa TEXT,
        condutas TEXT
    )
    ''')
    conn.commit()
    conn.close()
    logger.info("Banco de dados de validação inicializado")

def salvar_para_validacao(sintomas, resposta, classificacao="", justificativa="", condutas=""):
    conn = sqlite3.connect('./validacao_triagem.db')
    cursor = conn.cursor()
    triagem_id = str(uuid.uuid4())
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO validacao_triagem (id, sintomas, resposta, data_hora, classificacao, justificativa, condutas) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (triagem_id, sintomas, str(resposta), data_hora, classificacao, justificativa, condutas)
    )
    conn.commit()
    conn.close()
    logger.info(f"Triagem salva para validação: id={triagem_id}")
    return triagem_id

def carregar_casos_validados():
    try:
        conn = sqlite3.connect('./validacao_triagem.db')
        cursor = conn.cursor()
        cursor.execute("SELECT sintomas, resposta FROM validacao_triagem WHERE validado = 1")
        casos = cursor.fetchall()
        conn.close()
        logger.info(f"Casos validados carregados: {len(casos)} casos")
        return casos
    except Exception as e:
        logger.error(f"Erro ao carregar casos validados: {str(e)}")
        return []

def obter_triagens(filtro="todas"):
    conn = sqlite3.connect('./validacao_triagem.db')
    cursor = conn.cursor()
    
    query = "SELECT id, sintomas, resposta, data_hora, validado, feedback, validado_por, data_validacao FROM validacao_triagem"
    
    if filtro == "pendentes":
        query += " WHERE validado = 0"
    elif filtro == "validadas":
        query += " WHERE validado = 1"
        
    query += " ORDER BY data_hora DESC"
    
    cursor.execute(query)
    triagens = cursor.fetchall()
    conn.close()
    
    result = []
    for triagem in triagens:
        result.append({
            "id": triagem[0],
            "sintomas": triagem[1],
            "resposta": triagem[2],
            "data_hora": triagem[3],
            "validado": triagem[4],
            "feedback": triagem[5],
            "validado_por": triagem[6],
            "data_validacao": triagem[7]
        })
    
    logger.info(f"Triagens obtidas: {len(result)} triagens (filtro: {filtro})")
    return result

def validar_triagem(triagem_id, validado_por, feedback):
    conn = sqlite3.connect('./validacao_triagem.db')
    cursor = conn.cursor()
    data_validacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "UPDATE validacao_triagem SET validado = 1, feedback = ?, validado_por = ?, data_validacao = ? WHERE id = ?",
        (feedback, validado_por, data_validacao, triagem_id)
    )
    conn.commit()
    conn.close()
    logger.info(f"Triagem validada: id={triagem_id}, validado_por={validado_por}")
    return True

# Initialize database
init_validation_db()

# Load validated cases
casos_validados = carregar_casos_validados()

# Insert validated cases into vector database
if collection is not None and embedding_service is not None:
    for i, (sintomas, resposta) in enumerate(casos_validados):
        case_id = f"validated_case_{i}"
        try:
            embedding = embedding_service.get_embedding(sintomas)
            collection.add(
                embeddings=[embedding],
                ids=[case_id],
                metadatas=[{"content": sintomas, "resposta": resposta}]
            )
            logger.info(f"Caso validado adicionado ao ChromaDB: case_id={case_id}")
        except Exception as e:
            logger.error(f"Erro ao processar caso validado {case_id}: {str(e)}")

# API endpoints
@app.get("/")
async def root():
    return {"message": "Sistema de Triagem API"}

@app.post("/api/triagem", response_model=TriagemResponse)
async def realizar_triagem(request: TriagemProcessar):
    try:
        # Check if symptoms are provided
        if not request.sintomas:
            logger.warning("Requisição de triagem sem sintomas")
            raise HTTPException(status_code=400, detail="Sintomas não fornecidos")
        
        logger.info(f"Iniciando triagem: {request.sintomas[:50]}...")
        
        # Verificar se os serviços estão disponíveis
        if embedding_service is None:
            logger.error("Serviço de embeddings não disponível")
            raise HTTPException(status_code=503, detail="Serviço de embeddings não disponível")
        
        if ollama_service is None:
            logger.error("Serviço Ollama não disponível")
            raise HTTPException(status_code=503, detail="Serviço Ollama não disponível")
        
        if collection is None:
            logger.error("ChromaDB não disponível")
            raise HTTPException(status_code=503, detail="Serviço de banco de dados vetorial não disponível")
        
        # Convert symptoms to embedding
        query_embedding = embedding_service.get_embedding(request.sintomas)
        logger.info("Embedding gerado com sucesso")
        
        # Query vector database for similar cases
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        
        # Extract similar cases
        similar_cases = [metadata["content"] for metadata in results['metadatas'][0]]
        logger.info(f"Casos similares encontrados: {len(similar_cases)}")
        
        # Formatar prompt com casos similares
        prompt = ollama_service.format_prompt(request.sintomas, similar_cases)
        
        # Call Ollama API with optimized service
        response_text = await ollama_service.generate_response(prompt)
        logger.info(f"Resposta gerada: {len(response_text)} caracteres")
        
        # Process the response with optimized service
        classificacao, justificativa, condutas = ollama_service.process_response(response_text)
        logger.info(f"Resposta processada: classificação={classificacao}")
        
        # Save to validation database
        triagem_id = salvar_para_validacao(
            request.sintomas, 
            response_text,
            classificacao,
            justificativa,
            condutas
        )
        
        return {
            "id": triagem_id,
            "sintomas": request.sintomas,
            "resposta": response_text,
            "classificacao": classificacao,
            "justificativa": justificativa,
            "condutas": condutas,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except HTTPException as e:
        # Repassar exceções HTTP
        raise e
    except Exception as e:
        logger.error(f"Erro ao processar triagem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar triagem: {str(e)}")

@app.get("/api/triagens")
async def listar_triagens(filtro: str = "todas"):
    try:
        triagens = obter_triagens(filtro)
        return {"triagens": triagens}
    except Exception as e:
        logger.error(f"Erro ao listar triagens: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar triagens: {str(e)}")

@app.post("/api/validar", response_model=ValidationResponse)
async def validar(request: ValidationRequest):
    try:
        success = validar_triagem(request.triagem_id, request.validado_por, request.feedback)
        if success:
            return {"success": True, "message": "Triagem validada com sucesso"}
        else:
            return {"success": False, "message": "Erro ao validar triagem"}
    except Exception as e:
        logger.error(f"Erro ao validar triagem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao validar triagem: {str(e)}")

@app.get("/api/estatisticas")
async def estatisticas():
    try:
        conn = sqlite3.connect('./validacao_triagem.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM validacao_triagem")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM validacao_triagem WHERE validado = 1")
        validadas = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM validacao_triagem WHERE validado = 0")
        pendentes = cursor.fetchone()[0]
        conn.close()
        
        return {
            "total": total,
            "validadas": validadas,
            "pendentes": pendentes
        }
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")

@app.get("/api/status")
async def status():
    """Endpoint para verificar o status dos serviços"""
    try:
        status_data = {
            "api": "online",
            "embedding_service": "online" if embedding_service is not None else "offline",
            "ollama_service": "online" if ollama_service is not None else "offline",
            "chromadb": "online" if collection is not None else "offline",
            "database": "online"  # Assumimos que o banco SQLite está sempre disponível
        }
        
        # Verificar se o Ollama está realmente disponível
        if ollama_service is not None:
            status_data["ollama_available"] = ollama_service._is_ollama_available()
        
        return status_data
    except Exception as e:
        logger.error(f"Erro ao verificar status: {str(e)}")
        return {
            "api": "degraded",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
