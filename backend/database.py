"""
Module pour gérer la base de données SQLite des demandes de ressources.
"""
import sqlite3
from pathlib import Path
import datetime

DB_PATH = Path(__file__).parent / 'resource_requests.db'

def init_db():
    """
    Initialise la base de données avec la table des demandes de ressources.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resource_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            vm_name TEXT NOT NULL,
            current_ram_mb INTEGER NOT NULL,
            current_cpu INTEGER NOT NULL,
            current_storage_gb INTEGER NOT NULL,
            requested_ram_mb INTEGER NOT NULL,
            requested_cpu INTEGER NOT NULL,
            requested_storage_gb INTEGER NOT NULL,
            reason TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP NULL,
            admin_notes TEXT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_resource_request(username, vm_name, current_specs, requested_specs, reason):
    """
    Ajoute une nouvelle demande de ressources.
    
    Args:
        username: Nom de l'utilisateur
        vm_name: Nom de la VM
        current_specs: Dict avec ram_mb, cpu, storage_gb actuels
        requested_specs: Dict avec ram_mb, cpu, storage_gb demandés
        reason: Motif de la demande
    
    Returns:
        ID de la demande créée
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO resource_requests 
        (username, vm_name, current_ram_mb, current_cpu, current_storage_gb,
         requested_ram_mb, requested_cpu, requested_storage_gb, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        username,
        vm_name,
        current_specs['ram_mb'],
        current_specs['cpu'],
        current_specs['storage_gb'],
        requested_specs['ram_mb'],
        requested_specs['cpu'],
        requested_specs['storage_gb'],
        reason
    ))
    
    request_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return request_id

def get_user_requests(username):
    """
    Récupère toutes les demandes d'un utilisateur.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM resource_requests 
        WHERE username = ? 
        ORDER BY created_at DESC
    ''', (username,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_all_requests(status=None):
    """
    Récupère toutes les demandes (pour admin).
    
    Args:
        status: Filtrer par statut ('pending', 'approved', 'rejected') ou None pour tout
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if status:
        cursor.execute('''
            SELECT * FROM resource_requests 
            WHERE status = ?
            ORDER BY created_at DESC
        ''', (status,))
    else:
        cursor.execute('''
            SELECT * FROM resource_requests 
            ORDER BY created_at DESC
        ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def update_request_status(request_id, status, admin_notes=None):
    """
    Met à jour le statut d'une demande.
    
    Args:
        request_id: ID de la demande
        status: Nouveau statut ('approved', 'rejected', etc.)
        admin_notes: Notes optionnelles de l'admin
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE resource_requests 
        SET status = ?, processed_at = ?, admin_notes = ?
        WHERE id = ?
    ''', (status, datetime.datetime.now(), admin_notes, request_id))
    
    conn.commit()
    conn.close()

# Initialiser la DB au chargement du module
init_db()
