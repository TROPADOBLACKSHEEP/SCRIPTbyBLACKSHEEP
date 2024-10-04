import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import os
import logging

class Colors:
    RESET = '\033[0m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'

def print_banner(title):
    """Exibe um banner formatado com o título fornecido."""
    print(f"\n{'=' * 50}")
    print(f"{title:^50}")
    print(f"{'=' * 50}")

def exibir_banner():
    """Exibe um banner inicial de boas-vindas com informações do script."""
    print(f"""
{Colors.RED}  
            ┏━━┳━┓╋┏┳━━━┳━━━┓┏━━┳━━━┳━━━━┳┓╋╋┏┓     
            ┗┫┣┫┃┗┓┃┃┏━━┫┏━┓┃┗┫┣┫┏━┓┃┏┓┏┓┃┗┓┏┛┃     
            ╋┃┃┃┏┓┗┛┃┗━━┫┃╋┃┃╋┃┃┃┗━┛┣┛┃┃┗┻┓┃┃┏┛     
            ╋┃┃┃┃┗┓┃┃┏━━┫┃╋┃┃╋┃┃┃┏━━┛╋┃┃╋╋┃┗┛┃      
            ┏┫┣┫┃╋┃┃┃┃╋╋┃┗━┛┃┏┫┣┫┃╋╋╋╋┃┃╋╋┗┓┏┛      
            ┗━━┻┛╋┗━┻┛╋╋┗━━━┛┗━━┻┛╋╋╋╋┗┛╋╋╋┗┛   
                   ⧳⦕ ᴘʏ ᴄᴏɴғɪɡ ʙʏ ʙʟᴀᴄᴋsʜᴇᴇᴘ_ʙ ⦖⧳ .           
{Colors.RESET}
""")

def save_info_to_file(user_info, server_info, counts, filename, folder_path, base_url):
    """
    Salva as informações obtidas em um arquivo de texto dentro da pasta especificada no armazenamento interno.
    
    :param user_info: Dicionário com informações do usuário.
    :param server_info: Dicionário com informações do servidor.
    :param counts: Dicionário com contagens de streams.
    :param filename: Nome do arquivo onde as informações serão salvas.
    :param folder_path: Caminho da pasta onde o arquivo será salvo.
    """
    try:
        # Criar a pasta no armazenamento interno se não existir
        os.makedirs(folder_path, exist_ok=True)
        
        # Criar o caminho completo do arquivo
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, "w") as file:
            file.write("=" * 50 + "\n")
            file.write(f"{'Informações do Usuário':^50}\n")
            file.write("=" * 50 + "\n")
            file.write(f"🟢 STATUS: {user_info.get('status', 'Desconhecido')}\n")
            file.write(f"👥 USUÁRIO: {user_info.get('username', 'Desconhecido')}\n")
            file.write(f"🔐 SENHA: {user_info.get('password', 'Desconhecido')}\n")
            
            # Convert timestamps to integer if they are strings
            created_at = user_info.get('created_at')
            exp_date = user_info.get('exp_date')

            if isinstance(created_at, str):
                created_at = int(created_at)
            if isinstance(exp_date, str):
                exp_date = int(exp_date)

            file.write(f"🗓️ DATA DE CRIAÇÃO: {datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if created_at else 'Desconhecido'}\n")
            file.write(f"📅 DATA DE EXPIRAÇÃO: {datetime.fromtimestamp(exp_date).strftime('%Y-%m-%d %H:%M:%S') if exp_date else 'Desconhecido'}\n")
            file.write(f"🔆 CONEXÕES MÁXIMAS: {user_info.get('max_connections', 'Desconhecido')}\n")
            file.write(f"🔅 CONEXÕES ATIVAS: {user_info.get('active_cons', 'Desconhecido')}\n")
            
            file.write("\n" + "=" * 50 + "\n")
            file.write(f"{'Informações do Servidor':^50}\n")
            file.write("=" * 50 + "\n")
            file.write(f"🔗 HOST: {server_info.get('url', 'Desconhecido')}\n")
            file.write(f"🛜 PORTA: {server_info.get('port', 'Desconhecido')}\n")
            file.write(f"🌐 PORTA HTTPS: {server_info.get('https_port', 'Desconhecido')}\n")
            file.write(f"💻 PROTOCOLO: {server_info.get('server_protocol', 'Desconhecido')}\n")
            file.write(f"🖱️ PORTA RTMP: {server_info.get('rtmp_port', 'Desconhecido')}\n")
            file.write(f"🕛 HORA ATUAL: {server_info.get('time_now', 'Desconhecido')}\n")
            file.write(f"🔄 ACESSE: http://{server_info.get('url', 'Desconhecido')}/client_area/index.php?username={user_info.get('username', 'Desconhecido')}&password={user_info.get('password', 'Desconhecido')}&submit\n")
            
            file.write("\n" + "=" * 50 + "\n")
            file.write(f"{'Formatos Permitidos':^50}\n")
            file.write("=" * 50 + "\n")
            file.write(f"🔰 FORMATO DA LISTA:\n")
            allowed_formats = user_info.get('allowed_output_formats', [])
            for format in allowed_formats:
                file.write(f"🔗 {base_url}&format={format}\n")

            file.write("\n" + "=" * 50 + "\n")
            file.write(f"{'Contagem de Streams':^50}\n")
            file.write("=" * 50 + "\n")
            file.write(f"📊 Live Streams: {counts.get('live streams', 0)}\n")
            file.write(f"📊 Series: {counts.get('series', 0)}\n")
            file.write(f"📊 Vod Streams: {counts.get('vod streams', 0)}\n")
        
        print(f"Informações salvas em {file_path}")
    except IOError as e:
        print(f"Erro ao salvar informações em {file_path}: {e}")

def get_stream_data(url):
    try:
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        username = params.get('username', [None])[0]
        password = params.get('password', [None])[0]

        if not username or not password:
            print_banner("Erro")
            print(f"{Colors.RED}❌ Erro: Usuário ou senha não encontrados na URL.{Colors.RESET}")
            return None

        global base_url
        base_url = f"http://{parsed_url.hostname}:{parsed_url.port or 80}/player_api.php"
        headers = {'Content-Type': 'application/json'}
        api_params = {'username': username, 'password': password}
        
        response = requests.get(base_url, params=api_params, headers=headers)
        response.raise_for_status()
        data = response.json()

        user_info = data.get('user_info', {})
        server_info = data.get('server_info', {})

        if user_info.get('status') == 'Active':
            created_at = user_info.get('created_at')
            exp_date = user_info.get('exp_date')

            if isinstance(created_at, str):
                created_at = int(created_at)
            if isinstance(exp_date, str):
                exp_date = int(exp_date)

            print_banner("Informações do Usuário")
            print(f"{Colors.GREEN}🟢 STATUS:{Colors.RESET} {user_info.get('status', 'Desconhecido')}")
            print(f"{Colors.GREEN}👥 USUÁRIO:{Colors.RESET} {username}")
            print(f"{Colors.GREEN}🔐 SENHA:{Colors.RESET} {password}")
            print(f"{Colors.GREEN}🗓️ DATA DE CRIAÇÃO:{Colors.RESET} {datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if created_at else 'Desconhecido'}")
            print(f"{Colors.GREEN}📅 DATA DE EXPIRAÇÃO:{Colors.RESET} {datetime.fromtimestamp(exp_date).strftime('%Y-%m-%d %H:%M:%S') if exp_date else 'Desconhecido'}")
            print(f"{Colors.GREEN}🔆 CONEXÕES MÁXIMAS:{Colors.RESET} {user_info.get('max_connections', 'Desconhecido')}")
            print(f"{Colors.GREEN}🔅 CONEXÕES ATIVAS:{Colors.RESET} {user_info.get('active_cons', 'Desconhecido')}")

            print_banner("Informações do Servidor")
            print(f"{Colors.YELLOW}🔗 HOST:{Colors.RESET} {server_info.get('url', 'Desconhecido')}")
            print(f"{Colors.YELLOW}🛜 PORTA:{Colors.RESET} {server_info.get('port', 'Desconhecido')}")
            print(f"{Colors.YELLOW}🌐 PORTA HTTPS:{Colors.RESET} {server_info.get('https_port', 'Desconhecido')}")
            print(f"{Colors.YELLOW}💻 PROTOCOLO:{Colors.RESET} {server_info.get('server_protocol', 'Desconhecido')}")
            print(f"{Colors.YELLOW}🖱️ PORTA RTMP:{Colors.RESET} {server_info.get('rtmp_port', 'Desconhecido')}")
            print(f"{Colors.YELLOW}🕛 HORA ATUAL:{Colors.RESET} {server_info.get('time_now', 'Desconhecido')}")
            print(f"{Colors.YELLOW}🔄 ACESSE:{Colors.RESET} http://{server_info.get('url', 'Desconhecido')}/client_area/index.php?username={username}&password={password}&submit")

            print_banner("Formatos Permitidos")
            print(f"{Colors.BLUE}🔰 FORMATO DA LISTA:{Colors.RESET}")
            for format in user_info.get('allowed_output_formats', []):
                print(f"{Colors.BLUE}🔗 {base_url}&format={format}{Colors.RESET}")

            # Fetch additional data
            actions = ['get_live_streams', 'get_series', 'get_vod_streams']
            counts = {'live streams': 0, 'series': 0, 'vod streams': 0}

            print_banner("Contagem de Streams")
            for action in actions:
                action_url = f"{base_url}?action={action}"
                response = requests.get(action_url, params=api_params, headers=headers)
                response.raise_for_status()
                action_data = response.json()
                counts[action.replace('get_', '').replace('_', ' ')] = len(action_data)
                print(f"{Colors.BLUE}📊 {action.replace('get_', '').replace('_', ' ').title()}:{Colors.RESET} {counts[action.replace('get_', '').replace('_', ' ')]}")

            panel_name = parsed_url.hostname.split('.')[0]  # Extrai o nome do painel da URL
            filename = f"info_{panel_name}.txt"
            folder_path = '/storage/emulated/0/informacoes_painel'  # Caminho no armazenamento interno

            save_info_to_file(user_info, server_info, counts, filename, folder_path, base_url)

            return counts
        else:
            print_banner("Erro")
            print(f"{Colors.RED}❌ Erro: Conta inativa ou sem informações.{Colors.RESET}")
            return None

    except requests.RequestException as e:
        print_banner("Erro")
        print(f"{Colors.RED}❌ Erro: Não foi possível completar a solicitação. Detalhes: {e}{Colors.RESET}")
        return None
    except (ValueError, TypeError) as e:
        print_banner("Erro")
        print(f"{Colors.RED}❌ Erro: Dados inválidos recebidos. Detalhes: {e}{Colors.RESET}")
        return None

def get_user_url():
    """Solicita ao usuário a URL para verificação e retorna a URL limpa."""
    url = input("Digite a URL para verificar: ")
    return url.strip()

def main():
    exibir_banner()  # Exibe o banner no início do script
    
    url = get_user_url()
    
    print_banner("Início da Verificação")
    
    print(f"\nVerificando URL: {url}")
    counts = get_stream_data(url)
    if counts:
        # As informações já foram exibidas e salvas dentro da função get_stream_data.
        # Não há necessidade de exibir resumo total aqui.
        pass

if __name__ == "__main__":
    main()
