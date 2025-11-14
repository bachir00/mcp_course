# Créér un environnment avec Uv

```bash
#Environemnt
 python -m venv mcp_env
  .\mcp_env\Scripts\Activate.ps1 --> powershell
   .\mcp_env\Scripts\Activate.bat --> cmd
#Acitver l'environnemnt selon votre system W7/Unix

#Install mcp
pip install "mcp[cli]"

#Give the path of your code to the server
(mcp_env) PS D:\CoursMCP> mcp dev server.py
Starting MCP inspector...
⚙️ Proxy server listening on 127.0.0.1:6277
🔑 Session token: 9fc29f021dc16f4b836a3623ba87aa1c9acfe21baa664195aa890c7a4c42a5f0
Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🔗 Open inspector with token pre-filled:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=9fc29f021dc16f4b836a3623ba87aa1c9acfe21baa664195aa890c7a4c42a5f0

#Once on the ui click to the connect button
Connect button
--> You'll see the avalaible tools, prompts, resources, sampling,....


######################## Test avec le weather ################""""
Execute the server with weather.py and test the args in the IU.
(mcp_env) PS D:\CoursMCP> mcp dev weather.py
{
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

# Configuration for Guardio MCP:
cours_url: https://huggingface.co/learn/mcp-course/unit1/gradio-mcp 

```bash
##### Application for Guardio's project #############
# Sentiments Analysis
https://huggingface.co/learn/mcp-course/unit2/gradio-server 
pip install "gradio[mcp]" textblob

#Execute the file with python and use the UI:
(mcp_env) PS D:\CoursMCP\GuardioMCP> python .\server.py
* Running on local URL:  http://127.0.0.1:7860
* Running on public URL: https://c4d429503771a11265.gradio.live

#Web Interface
http://127.0.0.1:7860
#Schema 
http://127.0.0.1:7860/gradio_api/mcp/schema


Nb: On a le guardio (serverur MCP) mais le guardio app dans un remote server est géré par hugging face

```

#  Configuration de Claud like an MCP Client
docs: https://modelcontextprotocol.io/docs/develop/build-server 
```bash
Après avoir déveoloppé les tools du serveur

# Go on Claud > sittings >> developer> and add the tool
#Open and modify the claud-desktop.json 
Configuration Avec python main on peut utiliser uv: si on a un env créé avec uv
# {
#   "mcpServers": {
#     "weather": {
#       "command": "python", #ou bien donner le chemni pour l'exécuter dans l'env virtuelle
#       "args": [
#         "D:\\CoursMCP\\weather.py" #path to the server file
#       ]
#     }
#   }
# }

Il faut dans le menu des outils avtiver le toll pour que claud puisse le use
Et puis demander une chose en utilisant le tool:
# EX: donne moi le weather du point 
# ```
# 40.7128, -74.0060
# ```

Claud va automatiquement démarrer le serveur avec la commande et le chemin fourni: Les logs vont etre dans un fichier logs de claud 
C:\Users\sirou\AppData\Roaming\Claude\logs\mcp-server-weather

```
#### Buiding an MCP client with Guardio
```bash
pip install "smolagents[mcp]" "gradio[mcp]" mcp fastmcp
# We'll use an MCP server from hugging(build with guardio)

Run the code in the environment && test tolls
#mcp_client_guardio

Deploying to Hugging Face Spaces
# https://huggingface.co/learn/mcp-course/unit2/gradio-client

# Create a new Space on Hugging Face:

Go to huggingface.co/spaces
Click “Create new Space”
Choose “Gradio” as the SDK
Name your space (e.g., “mcp-client”)
Update MCP Server URL in the code:

mcp_client = MCPClient(
    {"url": "https://abidlabs-mcp-tool-http.hf.space/gradio_api/mcp/sse", "transport": "sse"
    }
)
Create a requirements.txt file:

gradio[mcp]
smolagents[mcp]

# Push your code to the Space:
Note: While adding remote origin, Refer to password-git-deprecation for adding with AccessToken. 
https://huggingface.co/blog/password-git-deprecation
git init
git add app.py requirements.txt
git commit -m "Initial commit"
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/mcp-client
git push -u origin main



```
# Building Tiny Agents with MCP and the Hugging Face Hub
```bash
Let’s install the necessary packages to build our Tiny Agents.

Installation
npm install -g npx
npm i mcp-remote

# For Python, you need to install the latest version of huggingface_hub with the mcp extra to get all the necessary components.

pip install "huggingface_hub[mcp]>=0.32.0"

#login with hugging face (not need to configure the github credentials)
huggingface-cli login

# Tiny Agents MCP Client in the Command Line
Create file agent.json

{
	"model": "Qwen/Qwen2.5-72B-Instruct",
	# "provider": "nebius",
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

#Cmd
# Lancer d'abord le serveur mcp 
(mcp_env) PS D:\CoursMCP\GuardioMCP>  python .\mcp_server.py  
# Lancer le host: tiny-agent → 🤗 est le client mcp 
(mcp_env) PS D:\CoursMCP\GuardioMCP> tiny-agents run agent.json
Agent loaded with 1 tools:
 • letter_counter
» Count how many times the letter 'a' appears in "banana"
<Tool call_MA8wX6jgnOfblzrRAbrCuQlm>letter_counter {"letter": "a", "word": "banana"
}

Tool call_MA8wX6jgnOfblzrRAbrCuQlm
3

The letter 'a' appears 3 times in the word "banana".
» 

#Documentsion of tiny-agent
https://huggingface.co/docs/huggingface.js/main/en/tiny-agents/README
https://huggingface.co/blog/python-tiny-agents 

```

# Local Tiny Agents with AMD NPU and iGPU Acceleration

```bash
Avec lemonade server We can run a model local, it will be accelerated
############Test avec Guardio server ############################

# Lancer d'abord le serveur mcp 
(mcp_env) PS D:\CoursMCP\GuardioMCP>  python .\mcp_server.py  
# Lancer le host tiny-agent → 🤗 est le client mcp 
(mcp_env) PS D:\CoursMCP\GuardioMCP> tiny-agents run agent_limonade.json

#Inference avec un modèle local accéléré par lemonade Server 
Lancer le serveur mcp et lancer le client avec tinny et lemonade va utiliser le modèle pour faire inférence. 

{
  "model": "user.jan-nano",
  "endpointUrl": "http://localhost:8000/api/",
  "servers": [
    {
      "type": "stdio",
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": [
        "mcp-remote",
        "http://localhost:7860/gradio_api/mcp/sse"
      ]
    }
  ]
}


################## Test avec Desktop Commander 
################ Creating an assistant to handle sensitive information locally
#Insall Desktop Commnader --> https://github.com/wonderwhy-er/DesktopCommanderMCP
npx @wonderwhy-er/desktop-commander@latest setup

#cmd pour lancer lemonade server
lemonade-server serve # docs: [text](https://lemonade-server.ai/docs/server/server_integration/) && [github link](https://github.com/lemonade-sdk/lemonade)


file configuration avec desktop-commander
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
 créer ces fichiers 
#  Create a file called job_description.md
# touch candidates/john_resume.md

tiny-agent → 🤗 est le client mcp 

(mcp_env) PS D:\CoursMCP\GuardioMCP> tiny-agents run .\agent_desktop_commader.json
Agent loaded with 25 tools:
 • get_config
 • set_config_value


et demander ces questions
#  » Read the contents of C:\Users\your_username\file-assistant\job_description.md
# » Inside the same folder you can find a candidates folder. Check for john_resume.md and let me know if he is a good fit for the job.
# » Create a file called "invitation.md" in the "file-assistant" folder and write a short invitation to John to come in for an interview.


```

#  Unit 3
# Module 1: Build MCP Server(We use tiny-agent not claud-code(payant))

```bash
git clone https://github.com/huggingface/mcp-course.git 
# Navigate to the starter code directory
cd mcp-course/projects/unit3/build-mcp-server/starter
#installer les dépendances avec python pas avec uv
pip install .
pip install -e ".[dev]"
############ Faire l'implementtaion des outils
# Testing Your Implementation
python validate_starter.py
pytest test_server.py -v

Configuration de agent_pr.json avec lemonade server(pour llm)
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
# Exécution::
PS D:\CoursMCP> .\mcp_env\Scripts\Activate.ps1; cd "d:\CoursMCP\mcp-course\projects\unit3\build-mcp-server\starter"; tiny-agents run agent_pr.json

Une fois lancée poser les questions 
# Analyze my git changes
# What PR templates are available?
# Suggest a template for my feature change

```


