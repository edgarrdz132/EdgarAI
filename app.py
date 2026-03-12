"""
EdgarAI — Backend con autenticación, roles y PostgreSQL
========================================================
Roles:
  - admin    : ve todos los tickets y conversaciones
  - operador : ve solo sus propios tickets y conversaciones

Requisitos:
    pip install flask flask-cors openai pillow python-dotenv psycopg2-binary flask-session

Uso:
    python app.py  →  http://localhost:5000
"""

import os, base64, uuid, json, hashlib, secrets
from datetime import datetime
from flask import (Flask, request, jsonify, render_template,
                   send_from_directory, session, redirect, url_for)
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# ── OpenAI ────────────────────────────────────────────────────────────────────
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ── PostgreSQL ────────────────────────────────────────────────────────────────
try:
    import psycopg2, psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("⚠️  psycopg2 no instalado. Ejecuta: pip install psycopg2-binary")

DATABASE_URL   = os.getenv("DATABASE_URL", "").replace("subabase.com", "supabase.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o")

# ── App ───────────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
CORS(app)

SYSTEM_PROMPT = """Eres EdgarAI, un asistente experto en Soporte IT corporativo.
Tu misión es diagnosticar y resolver problemas técnicos de manera clara, profesional y empática.
Especialidades: Hardware, Software, Redes/VPN, Seguridad, Servidores, Impresoras, Correo, Accesos.
Pautas: sé conciso, usa pasos numerados, responde siempre en español."""

ESTADOS_VALIDOS = ["Abierto", "En progreso", "Resuelto", "Cerrado"]

def now_str():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ═════════════════════════════════════════════════════════════════════════════
# BASE DE DATOS
# ═════════════════════════════════════════════════════════════════════════════

def get_conn():
    if not PSYCOPG2_AVAILABLE or not DATABASE_URL:
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def init_db():
    conn = get_conn()
    if not conn:
        print("⚠️  Sin PostgreSQL — usando memoria")
        return
    try:
        with conn.cursor() as cur:
            # Usuarios
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id           SERIAL PRIMARY KEY,
                    username     VARCHAR(80)  UNIQUE NOT NULL,
                    password     VARCHAR(200) NOT NULL,
                    nombre       VARCHAR(100) NOT NULL,
                    rol          VARCHAR(20)  NOT NULL DEFAULT 'operador',
                    creado_en    VARCHAR(20)
                );
            """)
            # Tickets
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id                VARCHAR(20)  PRIMARY KEY,
                    usuario_id        INTEGER REFERENCES usuarios(id),
                    nombre            VARCHAR(100),
                    resumen           TEXT,
                    categoria         VARCHAR(80),
                    subcategoria      VARCHAR(120),
                    area              VARCHAR(80),
                    activo            VARCHAR(80),
                    descripcion       TEXT,
                    prioridad         INTEGER,
                    estado            VARCHAR(30) DEFAULT 'Abierto',
                    creado_en         VARCHAR(20),
                    actualizado_en    VARCHAR(20),
                    historial_estados JSONB DEFAULT '[]'::jsonb
                );
            """)
            # Conversaciones
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversaciones (
                    id          SERIAL PRIMARY KEY,
                    usuario_id  INTEGER REFERENCES usuarios(id),
                    titulo      VARCHAR(200),
                    mensajes    JSONB DEFAULT '[]'::jsonb,
                    creado_en   VARCHAR(20),
                    actualizado_en VARCHAR(20)
                );
            """)
        conn.commit()

        # Crear admin por defecto si no existe
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM usuarios WHERE username = 'admin'")
            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO usuarios (username, password, nombre, rol, creado_en)
                    VALUES (%s, %s, %s, %s, %s)
                """, ('admin', hash_password('admin123'), 'Administrador', 'admin', now_str()))
                conn.commit()
                print("✅ Usuario admin creado — user: admin / pass: admin123")

        conn.close()
        print("✅ PostgreSQL inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando DB: {e}")
        conn.rollback()
        conn.close()

# ── Fallback memoria ──────────────────────────────────────────────────────────
usuarios_mem  = {
    'admin': {'id':1,'username':'admin','password':hash_password('admin123'),
              'nombre':'Administrador','rol':'admin','creado_en':now_str()}
}
tickets_mem   = {}
conv_mem      = {}
next_user_id  = 2

# ═════════════════════════════════════════════════════════════════════════════
# HELPERS AUTH
# ═════════════════════════════════════════════════════════════════════════════

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autenticado', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated

def current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    conn = get_conn()
    if conn:
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT id,username,nombre,rol FROM usuarios WHERE id=%s", (uid,))
                row = cur.fetchone()
                conn.close()
                return dict(row) if row else None
        except:
            conn.close()
    return usuarios_mem.get(session.get('username'))

# ═════════════════════════════════════════════════════════════════════════════
# RUTAS — PÁGINAS
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    user = current_user()
    return render_template('index.html', user=user)

@app.route('/admin')
def admin_panel():
    if 'user_id' not in session:
        return redirect('/login')
    user = current_user()
    if not user or user['rol'] != 'admin':
        return redirect('/')
    return render_template('admin.html', user=user)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# ═════════════════════════════════════════════════════════════════════════════
# RUTAS — AUTH
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/auth/login', methods=['POST'])
def auth_login():
    data     = request.get_json(force=True)
    username = data.get('username','').strip().lower()
    password = data.get('password','').strip()

    if not username or not password:
        return jsonify({'error': 'Usuario y contraseña requeridos'}), 400

    user = None
    conn = get_conn()
    if conn:
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s",
                            (username, hash_password(password)))
                row = cur.fetchone()
                if row:
                    user = dict(row)
            conn.close()
        except Exception as e:
            conn.close()
    else:
        u = usuarios_mem.get(username)
        if u and u['password'] == hash_password(password):
            user = u

    if not user:
        return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401

    session['user_id']  = user['id']
    session['username'] = user['username']
    session['rol']      = user['rol']
    return jsonify({'ok': True, 'user': {
        'id': user['id'], 'username': user['username'],
        'nombre': user['nombre'], 'rol': user['rol']
    }})


@app.route('/auth/register', methods=['POST'])
def auth_register():
    data     = request.get_json(force=True)
    username = data.get('username','').strip().lower()
    password = data.get('password','').strip()
    nombre   = data.get('nombre','').strip()
    rol      = data.get('rol','operador')

    if not all([username, password, nombre]):
        return jsonify({'error': 'Todos los campos son requeridos'}), 400
    if len(password) < 6:
        return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
    if rol not in ['admin','operador']:
        rol = 'operador'

    conn = get_conn()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM usuarios WHERE username=%s", (username,))
                if cur.fetchone():
                    conn.close()
                    return jsonify({'error': 'El usuario ya existe'}), 409
                cur.execute("""
                    INSERT INTO usuarios (username,password,nombre,rol,creado_en)
                    VALUES (%s,%s,%s,%s,%s) RETURNING id
                """, (username, hash_password(password), nombre, rol, now_str()))
                new_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return jsonify({'ok': True, 'id': new_id})
        except Exception as e:
            conn.rollback(); conn.close()
            return jsonify({'error': str(e)}), 500
    else:
        global next_user_id
        if username in usuarios_mem:
            return jsonify({'error': 'El usuario ya existe'}), 409
        usuarios_mem[username] = {
            'id': next_user_id, 'username': username,
            'password': hash_password(password), 'nombre': nombre,
            'rol': rol, 'creado_en': now_str()
        }
        next_user_id += 1
        return jsonify({'ok': True})


@app.route('/auth/logout', methods=['POST'])
def auth_logout():
    session.clear()
    return jsonify({'ok': True})

@app.route('/auth/reset-password', methods=['POST'])
def auth_reset_password():
    data     = request.get_json(force=True)
    username = data.get('username', '').strip().lower()
    new_pass = data.get('new_password', '').strip()

    if not username or not new_pass:
        return jsonify({'error': 'Usuario y nueva contraseña requeridos'}), 400
    if len(new_pass) < 6:
        return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400

    conn = get_conn()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM usuarios WHERE username=%s", (username,))
                if not cur.fetchone():
                    conn.close()
                    return jsonify({'error': 'Usuario no encontrado'}), 404
                cur.execute(
                    "UPDATE usuarios SET password=%s WHERE username=%s",
                    (hash_password(new_pass), username)
                )
            conn.commit()
            conn.close()
            return jsonify({'ok': True})
        except Exception as e:
            conn.rollback(); conn.close()
            return jsonify({'error': str(e)}), 500
    else:
        if username not in usuarios_mem:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        usuarios_mem[username]['password'] = hash_password(new_pass)
        return jsonify({'ok': True})


@app.route('/auth/me')
def auth_me():
    user = current_user()
    if not user:
        return jsonify({'error': 'No autenticado'}), 401
    return jsonify({'user': user})

# ═════════════════════════════════════════════════════════════════════════════
# RUTAS — CHAT
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/ask', methods=['POST'])
@login_required
def ask():
    user         = current_user()
    user_message = request.form.get('message','').strip()
    image_file   = request.files.get('image')
    conv_id      = request.form.get('conv_id')

    if not user_message and not image_file:
        return jsonify({'response': 'Por favor escribe un mensaje.'}), 400

    if not OPENAI_AVAILABLE or not OPENAI_API_KEY:
        return _demo_response(user_message)

    try:
        client  = OpenAI(api_key=OPENAI_API_KEY)
        content = []

        if image_file:
            img_b64    = base64.standard_b64encode(image_file.read()).decode()
            media_type = image_file.content_type or 'image/jpeg'
            content.append({'type':'image_url','image_url':{
                'url': f'data:{media_type};base64,{img_b64}', 'detail':'high'}})

        content.append({'type':'text',
            'text': user_message or 'Analiza esta imagen y dime qué problema técnico ves.'})

        response = client.chat.completions.create(
            model=OPENAI_MODEL, max_tokens=1024,
            messages=[
                {'role':'system','content':SYSTEM_PROMPT},
                {'role':'user',  'content':content}
            ]
        )
        ai_text = response.choices[0].message.content

        # Guardar en BD
        _save_message(user['id'], conv_id, user_message or '[imagen]', ai_text)

        return jsonify({'response': ai_text})

    except Exception as e:
        app.logger.error(f'Error OpenAI: {e}')
        return jsonify({'response': f'❌ **Error:** {str(e)}'}), 500


def _save_message(user_id, conv_id, user_msg, ai_msg):
    """Guarda un par de mensajes en la conversación."""
    ahora = now_str()
    par   = [
        {'role':'user',      'content':user_msg, 'ts':ahora},
        {'role':'assistant', 'content':ai_msg,   'ts':ahora}
    ]
    conn = get_conn()
    if conn:
        try:
            with conn.cursor() as cur:
                if conv_id:
                    cur.execute("""
                        UPDATE conversaciones
                        SET mensajes = mensajes || %s::jsonb,
                            actualizado_en = %s
                        WHERE id=%s AND usuario_id=%s
                    """, (json.dumps(par), ahora, conv_id, user_id))
                else:
                    titulo = user_msg[:60] if user_msg else 'Conversación'
                    cur.execute("""
                        INSERT INTO conversaciones
                            (usuario_id,titulo,mensajes,creado_en,actualizado_en)
                        VALUES (%s,%s,%s::jsonb,%s,%s)
                    """, (user_id, titulo, json.dumps(par), ahora, ahora))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f'Error guardando conversación: {e}')
            conn.rollback(); conn.close()
    else:
        key = str(user_id)
        if key not in conv_mem:
            conv_mem[key] = []
        conv_mem[key].extend(par)


@app.route('/conversaciones', methods=['GET'])
@login_required
def list_conversaciones():
    user = current_user()
    conn = get_conn()
    if conn:
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                if user['rol'] == 'admin':
                    cur.execute("""
                        SELECT c.id, c.titulo, c.creado_en, c.actualizado_en,
                               u.nombre as usuario_nombre
                        FROM conversaciones c
                        JOIN usuarios u ON c.usuario_id = u.id
                        ORDER BY c.actualizado_en DESC LIMIT 50
                    """)
                else:
                    cur.execute("""
                        SELECT id,titulo,creado_en,actualizado_en
                        FROM conversaciones WHERE usuario_id=%s
                        ORDER BY actualizado_en DESC LIMIT 50
                    """, (user['id'],))
                rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return jsonify({'conversaciones': rows})
        except Exception as e:
            conn.close()
            return jsonify({'conversaciones': []})
    return jsonify({'conversaciones': []})

# ═════════════════════════════════════════════════════════════════════════════
# RUTAS — TICKETS
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/tickets', methods=['POST'])
@login_required
def create_ticket():
    user = current_user()
    data = request.get_json(force=True)

    for field in ['nombre','resumen','categoria','subcategoria','prioridad']:
        if not data.get(field):
            return jsonify({'error': f'Campo requerido: {field}'}), 400

    ticket_id = 'TKT-' + str(uuid.uuid4()).split('-')[0].upper()
    ahora     = now_str()
    historial = [{'estado':'Abierto','fecha':ahora,'nota':'Ticket creado'}]

    ticket = {
        'id': ticket_id, 'usuario_id': user['id'],
        'nombre': data['nombre'], 'resumen': data['resumen'],
        'categoria': data['categoria'], 'subcategoria': data['subcategoria'],
        'area': data.get('area',''), 'activo': data.get('activo',''),
        'descripcion': data.get('descripcion',''),
        'prioridad': int(data['prioridad']),
        'estado': 'Abierto', 'creado_en': ahora, 'actualizado_en': ahora,
        'historial_estados': historial
    }

    conn = get_conn()
    print(f"DEBUG conn: {conn}, DATABASE_URL: {DATABASE_URL[:30] if DATABASE_URL else 'NONE'}")
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO tickets
                        (id,usuario_id,nombre,resumen,categoria,subcategoria,
                         area,activo,descripcion,prioridad,estado,
                         creado_en,actualizado_en,historial_estados)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    ticket_id, user['id'], ticket['nombre'], ticket['resumen'],
                    ticket['categoria'], ticket['subcategoria'],
                    ticket['area'], ticket['activo'], ticket['descripcion'],
                    ticket['prioridad'], 'Abierto', ahora, ahora,
                    json.dumps(historial)
                ))
            conn.commit(); conn.close()
        except Exception as e:
            conn.rollback(); conn.close()
            return jsonify({'error': str(e)}), 500
    else:
        tickets_mem[ticket_id] = ticket

    return jsonify({'ticket': ticket}), 201


@app.route('/tickets', methods=['GET'])
@login_required
def list_tickets():
    user   = current_user()
    estado = request.args.get('estado','').strip()
    conn   = get_conn()

    if conn:
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                if user['rol'] == 'admin':
                    q = "SELECT t.*, u.nombre as usuario_nombre FROM tickets t LEFT JOIN usuarios u ON t.usuario_id=u.id"
                    params = []
                    if estado and estado in ESTADOS_VALIDOS:
                        q += " WHERE t.estado=%s"
                        params.append(estado)
                    q += " ORDER BY t.prioridad DESC"
                    cur.execute(q, params)
                else:
                    q = "SELECT * FROM tickets WHERE usuario_id=%s"
                    params = [user['id']]
                    if estado and estado in ESTADOS_VALIDOS:
                        q += " AND estado=%s"
                        params.append(estado)
                    q += " ORDER BY prioridad DESC"
                    cur.execute(q, params)

                rows = []
                for r in cur.fetchall():
                    t = dict(r)
                    if isinstance(t.get('historial_estados'), str):
                        t['historial_estados'] = json.loads(t['historial_estados'])
                    rows.append(t)
            conn.close()
            return jsonify({'tickets': rows, 'total': len(rows)})
        except Exception as e:
            conn.close()

    # Fallback memoria
    lista = list(tickets_mem.values())
    if user['rol'] != 'admin':
        lista = [t for t in lista if t['usuario_id'] == user['id']]
    if estado:
        lista = [t for t in lista if t['estado'] == estado]
    lista.sort(key=lambda t: t['prioridad'], reverse=True)
    return jsonify({'tickets': lista, 'total': len(lista)})


@app.route('/tickets/<ticket_id>/estado', methods=['PATCH'])
@login_required
def update_estado(ticket_id):
    user  = current_user()
    data  = request.get_json(force=True)
    nuevo = data.get('estado','').strip()
    nota  = data.get('nota','').strip() or f'Estado actualizado a: {nuevo}'
    ahora = now_str()

    if nuevo not in ESTADOS_VALIDOS:
        return jsonify({'error': f'Estado inválido. Opciones: {ESTADOS_VALIDOS}'}), 400

    conn = get_conn()
    if conn:
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # Verificar acceso
                if user['rol'] == 'admin':
                    cur.execute("SELECT * FROM tickets WHERE id=%s", (ticket_id,))
                else:
                    cur.execute("SELECT * FROM tickets WHERE id=%s AND usuario_id=%s",
                                (ticket_id, user['id']))
                row = cur.fetchone()
                if not row:
                    conn.close()
                    return jsonify({'error': 'Ticket no encontrado'}), 404

                t = dict(row)
                historial = t['historial_estados'] if isinstance(t['historial_estados'], list) \
                            else json.loads(t['historial_estados'])
                historial.append({'estado': nuevo, 'fecha': ahora, 'nota': nota})

                cur.execute("""
                    UPDATE tickets SET estado=%s, actualizado_en=%s, historial_estados=%s
                    WHERE id=%s
                """, (nuevo, ahora, json.dumps(historial), ticket_id))
            conn.commit()
            conn.close()
            return jsonify({'ok': True, 'estado': nuevo})
        except Exception as e:
            conn.rollback(); conn.close()
            return jsonify({'error': str(e)}), 500

    # Fallback memoria
    t = tickets_mem.get(ticket_id)
    if not t:
        return jsonify({'error': 'Ticket no encontrado'}), 404
    t['estado'] = nuevo
    t['actualizado_en'] = ahora
    t['historial_estados'].append({'estado': nuevo, 'fecha': ahora, 'nota': nota})
    return jsonify({'ok': True, 'estado': nuevo})

# ═════════════════════════════════════════════════════════════════════════════
# RUTAS — ADMIN
# ═════════════════════════════════════════════════════════════════════════════

@app.route('/admin/usuarios', methods=['GET'])
@login_required
def list_usuarios():
    user = current_user()
    if user['rol'] != 'admin':
        return jsonify({'error': 'Sin permisos'}), 403

    conn = get_conn()
    if conn:
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT id,username,nombre,rol,creado_en FROM usuarios ORDER BY id")
                rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return jsonify({'usuarios': rows})
        except Exception as e:
            conn.close()

    return jsonify({'usuarios': [
        {k:v for k,v in u.items() if k != 'password'}
        for u in usuarios_mem.values()
    ]})


@app.route('/status')
def status():
    return jsonify({
        'app':     'EdgarAI',
        'openai':  '✅' if OPENAI_API_KEY else '⚠️',
        'modelo':  OPENAI_MODEL,
        'db':      '✅ PostgreSQL' if (PSYCOPG2_AVAILABLE and DATABASE_URL) else '⚠️ Memoria',
    })

# ── Demo ──────────────────────────────────────────────────────────────────────
def _demo_response(message):
    msg = (message or '').lower()
    if any(w in msg for w in ['vpn','red','internet']):
        r = '**Diagnóstico VPN:**\n1. Verifica cliente VPN actualizado.\n2. Confirma credenciales.\n3. Revisa firewall (puerto 443/1194).'
    elif any(w in msg for w in ['lento','lenta']):
        r = '**Optimización:**\n1. Reinicia el equipo.\n2. Cierra programas (Ctrl+Shift+Esc).\n3. Verifica espacio en disco.'
    else:
        r = f'Modo demo activo. Configura `OPENAI_API_KEY` en `.env` para activar GPT-4o.'
    return jsonify({'response': r})

# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════
init_db()  # <- agrega esta línea aquí

if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG','true').lower() == 'true'
    print(f"""
╔══════════════════════════════════════════════╗
║        EdgarAI — Con Auth + PostgreSQL       ║
╠══════════════════════════════════════════════╣
║  URL:    http://localhost:{port}               ║
║  DB:     {'✅ PostgreSQL' if (PSYCOPG2_AVAILABLE and DATABASE_URL) else '⚠️  Memoria (configura DATABASE_URL)'}{'':>14}║
║  OpenAI: {'✅ Configurado' if OPENAI_API_KEY else '⚠️  Sin configurar'}{'':>23}║
╚══════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=debug)
