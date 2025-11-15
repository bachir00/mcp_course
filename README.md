# 🚀 Projet MCP (Model Context Protocol) - Guide Complet

## 📋 Configuration de l'Environnement

### Création de l'environnement virtuel Python

```bash
# Créer l'environnement virtuel
python -m venv mcp_env

# Activation selon votre système :
.\mcp_env\Scripts\Activate.ps1    # PowerShell
.\mcp_env\Scripts\Activate.bat     # CMD
source mcp_env/bin/activate        # Linux/Unix

# Installation de MCP
pip install "mcp[cli]"
```

### 🔧 Test du serveur MCP avec l'inspecteur

```bash
# Démarrer l'inspecteur MCP
(mcp_env) PS D:\CoursMCP> mcp dev server.py

# Sortie attendue :
Starting MCP inspector...
⚙️ Proxy server listening on 127.0.0.1:6277
🔑 Session token: 9fc29f021dc16f4b836a3623ba87aa1c9acfe21baa664195aa890c7a4c42a5f0
Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🔗 Open inspector with token pre-filled:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=9fc29f021dc16f4b836a3623ba87aa1c9acfe21baa664195aa890c7a4c42a5f0

# Dans l'interface web, cliquez sur "Connect"
# Vous verrez tous les tools, prompts, resources disponibles
```

### 🌤️ Test avec l'exemple Weather

```bash
# Tester le serveur weather.py
(mcp_env) PS D:\CoursMCP> mcp dev weather.py

# Données de test :
{
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

## 🛡️ Configuration Guardio MCP

**Cours de référence :** https://huggingface.co/learn/mcp-course/unit1/gradio-mcp

### Analyse de sentiments avec Gradio

```bash
# Installation des dépendances pour Guardio
pip install "gradio[mcp]" textblob

# Démarrage du serveur Guardio
(mcp_env) PS D:\CoursMCP\GuardioMCP> python .\server.py

# Sortie attendue :
* Running on local URL:  http://127.0.0.1:7860
* Running on public URL: https://c4d429503771a11265.gradio.live

# Interfaces disponibles :
# Interface web : http://127.0.0.1:7860
# Schéma MCP   : http://127.0.0.1:7860/gradio_api/mcp/schema
```

<!-- ** Note importante :** Le serveur Guardio MCP est local, mais l'application Guardio distante est hébergée sur Hugging Face. -->

## 🤖 Configuration de Claude comme Client MCP

**Documentation :** https://modelcontextprotocol.io/docs/develop/build-server

### Intégration avec Claude Desktop

```bash
# Après avoir développé les tools du serveur MCP

# 1. Aller dans Claude > Settings > Developer
# 2. Modifier le fichier claude-desktop.json
# Configuration avec Python (ou uv si environnement créé avec uv) :

{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": [
        "D:\\CoursMCP\\weather.py"
      ]
    }
  }
}

# 3. Activer le tool dans le menu des outils de Claude
# 4. Tester avec une requête
```

### 🧪 Test d'utilisation

```bash
# Exemple de requête à Claude :
"Donne-moi la météo du point :"
40.7128, -74.0060

# Claude démarrera automatiquement le serveur MCP
# Les logs se trouvent dans :
# C:\Users\sirou\AppData\Roaming\Claude\logs\mcp-server-weather
```

### 🏗️ Construction d'un Client MCP avec Guardio

```bash
# Installation des dépendances
pip install "smolagents[mcp]" "gradio[mcp]" mcp fastmcp

# Utilisation d'un serveur MCP depuis Hugging Face (construit avec Guardio)
# Exécuter le code dans l'environnement et tester les outils
# Fichier : mcp_client_guardio
```

### 🚀 Déploiement sur Hugging Face Spaces

**Guide :** https://huggingface.co/learn/mcp-course/unit2/gradio-client

```bash
# 1. Créer un nouveau Space sur Hugging Face :
# - Aller sur huggingface.co/spaces
# - Cliquer "Create new Space"
# - Choisir "Gradio" comme SDK
# - Nommer le space (ex: "mcp-client")

# 2. Mettre à jour l'URL du serveur MCP dans le code :
mcp_client = MCPClient(
    {"url": "https://abidlabs-mcp-tool-http.hf.space/gradio_api/mcp/sse", "transport": "sse"}
)

# 3. Créer requirements.txt :
gradio[mcp]
smolagents[mcp]

# 4. Pousser le code sur le Space :
git init
git add app.py requirements.txt
git commit -m "Initial commit"
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/mcp-client
git push -u origin main
```

**⚠️ Note :** Pour l'authentification Git, consulter : https://huggingface.co/blog/password-git-deprecation

## 🔧 Construction de Tiny Agents avec MCP et Hugging Face Hub

### Installation des dépendances

```bash
# Installation Node.js
npm install -g npx
npm i mcp-remote

# Installation Python avec support MCP
pip install "huggingface_hub[mcp]>=0.32.0"

# Connexion à Hugging Face (pas besoin de configurer GitHub)
huggingface-cli login
```

### Configuration du Client Tiny Agents

Créer le fichier `agent.json` :

```json
{
  "model": "Qwen/Qwen2.5-72B-Instruct",
  "servers": [
    {
      "type": "stdio",
      "command": "npx",
      "args": [
        "mcp-remote", 
        "http://localhost:7860/gradio_api/mcp/sse"
      ]
    }
  ]
}
```

### 🚀 Utilisation

```bash
# 1. Lancer d'abord le serveur MCP
(mcp_env) PS D:\CoursMCP\GuardioMCP> python .\mcp_server.py  

# 2. Lancer tiny-agents (🤗 client MCP)
(mcp_env) PS D:\CoursMCP\GuardioMCP> tiny-agents run agent.json

# Sortie attendue :
Agent loaded with 1 tools:
 • letter_counter

# Exemple d'utilisation :
» Count how many times the letter 'a' appears in "banana"
<Tool call_MA8wX6jgnOfblzrRAbrCuQlm>letter_counter {"letter": "a", "word": "banana"}

Tool call_MA8wX6jgnOfblzrRAbrCuQlm
3

The letter 'a' appears 3 times in the word "banana".
```

**📚 Documentation :**
- [Tiny Agents Guide](https://huggingface.co/docs/huggingface.js/main/en/tiny-agents/README)
- [Python Tiny Agents Blog](https://huggingface.co/blog/python-tiny-agents)

## 🌐 Tiny Agents Locaux avec Accélération AMD NPU et iGPU

### Test avec serveur Guardio + Lemonade Server

```bash
# Avec lemonade server, on peut faire tourner un modèle local accéléré

# Configuration avec Desktop Commander
# Installation : https://github.com/wonderwhy-er/DesktopCommanderMCP
npx @wonderwhy-er/desktop-commander@latest setup

# Démarrer lemonade server
lemonade-server serve 
# Docs: https://lemonade-server.ai/docs/server/server_integration/
# GitHub: https://github.com/lemonade-sdk/lemonade
```

### Configuration avec Desktop Commander

Créer le fichier `agent_desktop_commander.json` :

```json
{
  "model": "user.jan-nano",
  "endpointUrl": "http://localhost:8000/api/",
  "servers": [
    {
      "type": "stdio",
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": [
        "-y",
        "@wonderwhy-er/desktop-commander"
      ]
    }
  ]
}
```

### 📁 Création des fichiers de test

```bash
# Créer les fichiers pour les tests
# job_description.md
# candidates/john_resume.md
```

### 🧪 Tests d'utilisation

```bash
# Lancer tiny-agents
(mcp_env) PS D:\CoursMCP\GuardioMCP> tiny-agents run .\agent_desktop_commander.json

# Sortie attendue :
Agent loaded with 25 tools:
 • get_config
 • set_config_value
 # ... et autres tools

# Exemples de requêtes :
» Read the contents of C:\Users\your_username\file-assistant\job_description.md
» Inside the same folder you can find a candidates folder. Check for john_resume.md and let me know if he is a good fit for the job.
» Create a file called "invitation.md" in the "file-assistant" folder and write a short invitation to John to come in for an interview.
```

## 📚 Unit 3 - Cours MCP Avancé

### Module 1: Construction de Serveur MCP

**Note :** Nous utilisons tiny-agents au lieu de Claude Code (payant)

```bash
# Cloner le dépôt du cours
git clone https://github.com/huggingface/mcp-course.git 

# Naviguer vers le code de démarrage
cd mcp-course/projects/unit3/build-mcp-server/starter

# Installer les dépendances avec Python (pas uv)
pip install .
pip install -e ".[dev]"

# Après implémentation des outils
# Tests de validation
python validate_starter.py
pytest test_server.py -v
```

### Configuration Agent PR avec Lemonade Server

Créer le fichier `agent_pr.json` :

```json
{
  "model": "user.jan-nano",
  "endpointUrl": "http://localhost:8000/api/",
  "servers": [
    {
      "type": "stdio",
      "command": "python",
      "args": [
        "d:\\CoursMCP\\mcp-course\\projects\\unit3\\build-mcp-server\\starter\\server.py"
      ]
    }
  ]
}
```

### 🚀 Exécution

```bash
PS D:\CoursMCP> .\mcp_env\Scripts\Activate.ps1; cd "d:\CoursMCP\mcp-course\projects\unit3\build-mcp-server\starter"; tiny-agents run agent_pr.json

# Questions de test :
» Analyze my git changes
» What PR templates are available?
» Suggest a template for my feature change
```

### Module 2: Intégration GitHub Actions

**Workflow :** GitHub Actions → Webhook → JSON File → MCP Tools → tiny-agents → user

```bash
# Le serveur webhook est déjà fourni :
# D:\CoursMCP\mcp-course\projects\unit3\github-actions-integration\starter\webhook_server.py

# Implémenter les outils du serveur MCP :
# D:\CoursMCP\mcp-course\projects\unit3\github-actions-integration\starter\server.py
# ⚠️ Attention avec les commandes git pour l'utilisation du même terminal
```

### Configuration de l'agent Module 2

```json
{
  "model": "user.jan-nano",
  "endpointUrl": "http://localhost:8000/api/",
  "servers": [
    {
      "type": "stdio",
      "command": "python",
      "args": [
        "-u",
        "server.py"
      ]
    }
  ]
}
```

### 🌐 Services à lancer

```bash
# 1. Serveur webhook
(mcp_env) PS D:\CoursMCP> cd "d:\CoursMCP\mcp-course\projects\unit3\github-actions-integration\starter"; python webhook_server.py

# 2. Serveur MCP avec tiny-agents
(mcp_env) PS D:\CoursMCP\mcp-course\projects\unit3\github-actions-integration\starter> tiny-agents run agent_config.json

# Sortie attendue :
Agent loaded with 5 tools:
 • analyze_file_changes
 • get_pr_templates
 • suggest_template

# 3. Lemonade server (dans un autre terminal)
PS D:\CoursMCP> lemonade-server serve

# 4. Cloudflare Tunnel pour GitHub
cloudflared tunnel --url http://localhost:8080
# URL finale : https://deutsche-alternate-undefined-hundred.trycloudflare.com/webhook/github
```

**⚠️ Important :** L'URL de cloudflared est temporaire. Si vous redémarrez cloudflared, l'URL change et il faut la mettre à jour sur GitHub.

### Configuration GitHub

```bash
# Dans votre repo GitHub :
# Settings → Webhooks → Add webhook
# URL → L'URL Cloudflare + /webhook/github
# Content type → application/json
# Events → Workflow runs, Check runs, Push, etc.

# Développer un petit workflow avec vérification du README pour tester
# Pusher le workflow et le README
```

### 🧪 Test de l'agent MCP complet

```bash
# Exemple de question :
» Call get_workflow_status for Simple CI
<Tool epfNp9F7SOpIYsoWuBKO2pLFvUNJ4rJg>get_workflow_status {"workflow_name":"Simple CI"}

# Réponse attendue :
{
  "workflows": {
    "Simple CI": {
      "name": "Simple CI",
      "status": "completed",
      "conclusion": "success",
      "last_run": "2025-11-14T11:27:19.025573",
      "repository": "bachir00/mcp_course",
      "run_id": 19363165948,
      "html_url": "https://github.com/bachir00/mcp_course/actions/runs/19363165948",
      "head_branch": "main",
      "triggering_actor": "bachir00"
    }
  },
  "workflow_count": 1,
  "filter": "Simple CI",
  "last_updated": "2025-11-14T12:25:30.086457"
}
```

### Module 3: Notifications Slack

**Workflow :** GitHub Actions → Webhooks → MCP Server → Slack Notifications  
**Flux de données :** github_events.json → Analyse intelligente → Messages formatés

### Configuration du webhook Slack

```bash
# 1. Aller sur https://api.slack.com/apps
# 2. Créer une nouvelle app → "From scratch"
# 3. Choisir votre workspace
# 4. Aller dans "Features (sidebar)" → "Incoming Webhooks"
# 5. Activer les incoming webhooks
# 6. Cliquer "Add New Webhook to Workspace"
# 7. Choisir un canal (ex: #dev-notifications)
# 8. Copier l'URL du webhook

# Test du webhook
curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello from MCP Course!"}' "VOTRE_URL_WEBHOOK"

# ⚠️ Attention : Valider le payload selon votre terminal (cmd/powershell/linux)
```

### Configuration des variables d'environnement

```bash
# IMPORTANT : L'URL webhook est sensible - ne jamais la mettre dans le code !
# Dans PowerShell avec Python env :
$env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/VOTRE/URL/WEBHOOK"
```

### 🛠️ Implémentation

```bash
# Fichier principal :
# D:\CoursMCP\mcp-course\projects\unit3\slack-notification\starter\server.py

# Serveur webhook (même que Module 2) :
# D:\CoursMCP\mcp-course\projects\unit3\slack-notification\starter\webhook_server.py

# Configuration identique à Module 2 :
# - Même github_events.json
# - Même cloudflare tunnel
# - On ajoute juste l'outil d'envoi de messages Slack après configuration
```

**📌 Note importante :** Les petits LLMs peuvent avoir des problèmes avec de longs prompts. Il faut faire une réduction et rassembler certains outils.

---

## 🔗 Liens Utiles

- **MCP Documentation :** https://modelcontextprotocol.io/docs/develop/build-server
- **Hugging Face MCP Course :** https://huggingface.co/learn/mcp-course/
- **Tiny Agents :** https://huggingface.co/docs/huggingface.js/main/en/tiny-agents/README
- **Lemonade Server :** https://lemonade-server.ai/docs/server/server_integration/
- **Desktop Commander MCP :** https://github.com/wonderwhy-er/DesktopCommanderMCP

---

## 📦 Dépendances Principales

Voir `requirements.txt` et `requirements_mcp_project.txt` pour la liste complète des packages.

**Core MCP :**
- `fastmcp==2.11.2`
- `mcp==1.10.1`
- `python-dotenv==1.2.1`
- `GitPython==3.1.45`
- `requests==2.32.5`

---

## 🚨 Notes de Sécurité

- ❌ **Ne jamais commiter** les fichiers `.env` 
- ❌ **Ne jamais exposer** les URLs de webhook Slack
- ✅ **Toujours utiliser** des variables d'environnement pour les données sensibles
- ✅ **Vérifier** le `.gitignore` avant chaque push