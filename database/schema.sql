PRAGMA foreign_keys = ON;

DROP  TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP  TABLE IF EXISTS documents;
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name_file TEXT NOT NULL UNIQUE,
    status_file TEXT NULL,  -- uploaded | processed | error
    mime_type TEXT NULL,
    size INTEGER NULL,
    topic TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_ready_to_process BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

DROP  TABLE IF EXISTS chunks;
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    order_chunk INTEGER NOT NULL,
    strategy_chunk TEXT NOT NULL,
    token_count INTEGER  NULL,
    overlap_token INTEGER  NULL,
    metadata JSON NULL, -- Metadati aggiuntivi (pagina, riga, etc.)
    is_convert_embeded BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Tabella Virtuale per sqlite-vec (4096 è la dimensione di Llama3)
-- embedding float[4096] definisce un vettore di 4096 numeri a virgola mobile
DROP TABLE IF EXISTS vss_chunks;
CREATE VIRTUAL TABLE vss_chunks USING vec0(
    chunk_id INTEGER PRIMARY KEY,
    embedding float[4096]
);

DROP  TABLE IF EXISTS queries;
CREATE TABLE queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    query TEXT NOT NULL,
    topic TEXT NOT NULL,
    embedding BLOB NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

DROP  TABLE IF EXISTS results;
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    context TEXT NOT NULL,
    score REAL NOT NULL,
    model TEXT NOT NULL,
    user_feedback INTEGER DEFAULT NULL, -- NULL: no feedback, 1: OK, 0: KO
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE
);

/*
 Serve per:
capire perché il modello ha risposto così
analisi errori
Pareto / score multi‑obiettivo
*/
DROP  TABLE IF EXISTS chunk_usage;
CREATE TABLE chunk_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER,
    chunk_id INTEGER,
    similarity REAL,
    rank INTEGER,
    FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE,
    FOREIGN KEY (chunk_id) REFERENCES chunks(id) ON DELETE CASCADE
);

DROP  TABLE IF EXISTS rag_runs;
CREATE TABLE rag_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER,
    embedding_model TEXT,
    llm_model TEXT,
    chunk_strategy TEXT,
    retrieval_k INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS JOBS_FAILED;
CREATE TABLE JOBS_FAILED (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    row_id INTEGER NOT NULL,
    meta_data JSON NULL,
    exception TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);