import subprocess
import sys
import os
import logging
import requests
import webbrowser
from io import BytesIO
from threading import Thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.image import Image as CoreImage
from kivy.utils import platform
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.config import Config

# Função para instalar pacotes
def instalar_pacote(pacote):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

# Lista de pacotes necessários
pacotes = ["requests", "kivy"]

# Verifica e instala pacotes necessários
for pacote in pacotes:
    try:
        __import__(pacote)
    except ImportError:
        print(f"{pacote} não encontrado. Instalando...")
        instalar_pacote(pacote)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

# Definindo a taxa de FPS
Config.set('graphics', 'max_fps', '60')

class TelaTerminal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=15)
        self.terminal = TextInput(size_hint=(1, 0.8), readonly=True, multiline=True)
        self.layout.add_widget(self.terminal)
        self.outro_widget = Button(text="Outro widget", size_hint=(1, 0.3))
        self.layout.add_widget(self.outro_widget)
        self.add_widget(self.layout)

    def atualizar_terminal(self, mensagem):
        self.terminal.text += mensagem + '\n'
        self.terminal.cursor = (0, 0)

class TelaChecker(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.versao_local = "v1.3"
        self.url_menu_json = 'https://raw.githubusercontent.com/TROPADOBLACKSHEEP/SCRIPTbyBLACKSHEEP/refs/heads/main/SCRIPTversion/version.json'
        self.layout = BoxLayout(orientation='vertical', padding=15)

        with self.layout.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = RoundedRectangle(size=self.layout.size, pos=self.layout.pos, radius=[10])

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.label_funcionalidade = Label(text="", size_hint=(1, None), height=100)
        self.label_funcionalidade.bind(size=self.label_funcionalidade.setter('text_size'))
        self.layout.add_widget(self.label_funcionalidade)

        python_version = "Python: 3.11.4 [GCC 11.4.0]"
        self.label_python_version = Label(text=python_version, size_hint=(1, None), height=30, color=(1, 1, 0, 1))
        self.layout.add_widget(self.label_python_version)

        self.criar_pasta_download()
        self.imagem = self.baixar_e_exibir_imagem('https://raw.githubusercontent.com/TROPADOBLACKSHEEP/SCRIPTbyBLACKSHEEP/refs/heads/main/SCRIPTimage/SCRIPT-BY-BLACKSHEEP-02-10-2024.png')
        self.imagem.allow_stretch = True
        self.imagem.size_hint_y = 0.3
        self.layout.add_widget(self.imagem)

        button_spinner_layout = BoxLayout(size_hint=(1, None), height=80)
        self.adicionar_botoes(button_spinner_layout)
        self.layout.add_widget(button_spinner_layout)

        self.barra_progresso = ProgressBar(max=100, size_hint=(1, None), height=50)
        self.layout.add_widget(self.barra_progresso)

        self.label_status = Label(text='OBAA.. SAIU ATUALIZAÇÃO DO SCRIPT :D', size_hint=(1, None), height=1050, color=(1, 1, 1, 1))
        self.layout.add_widget(self.label_status)

        self.label_versao = Label(text=f"{self.versao_local}", size_hint=(1, None), height=30, color=(0, 1, 0, 1))
        self.layout.add_widget(self.label_versao)

        self.add_widget(self.layout)

        self.popup_download = None
        self.popup = None
        self.verificar_atualizacao()

    def _update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def criar_pasta_download(self):
        self.pasta_download = os.path.join('/storage/emulated/0', 'TROPADOBLACKSHEEP') if platform == 'android' else os.path.join(os.path.expanduser("~"), "TROPADOBLACKSHEEP")
        os.makedirs(self.pasta_download, exist_ok=True)

    def baixar_e_exibir_imagem(self, url):
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            img_data = BytesIO(resposta.content)
            textura = CoreImage(img_data, ext='png').texture
            imagem = Image(texture=textura)
            imagem.allow_stretch = True
            return imagem
        except Exception as e:
            logging.error(f"Erro ao baixar a imagem: {str(e)}")
            return Label(text="Imagem não disponível. Tente mais tarde.", color=(1, 1, 1, 1))

    def adicionar_botoes(self, layout):
        retro_background_color = (255/255, 0, 255/255, 1)  # Verde escuro
        text_color = (1, 1, 1, 1)

        botoes = [
            ('SCRIPTS', self.mostrar_popup_scripts),
            ('COMBOS', self.mostrar_popup_comb),
            ('ADD-ONS', self.mostrar_popup_kodi),
            ('TELEGRAM', self.mostrar_popup_telegram),
            ('SOBRE', self.mostrar_popup_sobre)  # Botão "SOBRE"
        ]

        for texto, metodo in botoes:
            button = Button(text=texto, size_hint=(0.95, 1), on_press=metodo,
                            background_color=retro_background_color, color=text_color, font_size=18, height=60)
            layout.add_widget(button)

    def verificar_atualizacao(self):
        Thread(target=self._verificar_atualizacao_thread).start()

    def _verificar_atualizacao_thread(self):
        try:
            resposta = requests.get(self.url_menu_json)
            resposta.raise_for_status()
            dados = resposta.json()

            if dados['version'] != self.versao_local:
                Clock.schedule_once(lambda dt: self.mostrar_popup_nova_versao(dados['version'], dados['script_url']), 0)
            else:
                Clock.schedule_once(lambda dt: self.atualizar_status('OBA.. O SCRIPT JÁ ESTÁ ATUALIZADO AGORA VOCÊ PODE BAIXAR SEUS ARQUIVOS.'), 0)
        except Exception as e:
            logging.error(f"Erro ao verificar atualização: {str(e)}")

    def atualizar_status(self, mensagem):
        self.label_status.text = mensagem
        logging.info(mensagem)

    def mostrar_popup_nova_versao(self, nova_versao, script_url):
        content = BoxLayout(orientation='vertical', padding=15)

        imagem = self.baixar_e_exibir_imagem('https://raw.githubusercontent.com/TROPADOBLACKSHEEP/SCRIPTbyBLACKSHEEP/refs/heads/main/SCRIPTimage/atualizacao.png')
        content.add_widget(imagem)

        content.add_widget(Label(text=f'Uma nova versão ({nova_versao}) está disponível!', size_hint_y=None, height=40))
        
        btn_atualizar = Button(text='Atualizar Agora', size_hint_y=None, height=60)
        btn_atualizar.bind(on_press=lambda x: self.baixar_script(script_url))
        content.add_widget(btn_atualizar)

        close_btn = Button(text='Fechar', size_hint_y=None, height=60)
        close_btn.bind(on_press=self.fechar_popup)
        content.add_widget(close_btn)

        self.popup = Popup(title='Atualização Disponível', content=content, size_hint=(0.7, 0.3))
        self.popup.open()

    def fechar_popup(self, instance):
        if self.popup:
            self.popup.dismiss()
            self.popup = None

        if self.popup_download:
            self.popup_download.dismiss()
            self.popup_download = None

    def baixar_script(self, url):
        Thread(target=self._baixar_script_thread, args=(url,)).start()

    def _baixar_script_thread(self, url):
        self.atualizar_status('Baixando script atualizado...')
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()

            nome_arquivo = os.path.basename(url)
            caminho_arquivo = os.path.join(self.pasta_download, nome_arquivo)

            with open(caminho_arquivo, 'wb') as f:
                f.write(resposta.content)

            Clock.schedule_once(lambda dt: self.atualizar_status('Script atualizado. Reiniciando...'), 0)
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.atualizar_status(f'Erro ao baixar o script: {str(e)}'), 0)

    def carregar_dados_github(self):
        url = 'https://raw.githubusercontent.com/TROPADOBLACKSHEEP/SCRIPTbyBLACKSHEEP/refs/heads/main/SCRIPTmenu/Menu.json'
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            dados = resposta.json()
            return dados
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {str(e)}")
            return None

    def mostrar_popup_scripts(self, instance):
        dados = self.carregar_dados_github()
        if dados:
            if not dados.get('scripts'):
                self.atualizar_status("Nenhum script disponível para download.")
                return
            self.mostrar_popup_download("SCRIPTS", dados['scripts'], "Scripts disponíveis para execução", 
                                         'https://raw.githubusercontent.com/TROPADOBLACKSHEEP/SCRIPTbyBLACKSHEEP/refs/heads/main/SCRIPTimage/SCRITP-PY-03-10-2024.png')

    def mostrar_popup_comb(self, instance):
        dados = self.carregar_dados_github()
        if dados:
            if not dados.get('combos'):
                self.atualizar_status("Nenhum combo disponível para download.")
                return
            self.mostrar_popup_download("COMBOS", dados['combos'], "Combos disponíveis para download", 
                                         'https://raw.githubusercontent.com/TROPADOBLACKSHEEP/SCRIPTbyBLACKSHEEP/refs/heads/main/SCRIPTimage/COMBO-TXT-03-10-2024.png')

    def mostrar_popup_kodi(self, instance):
        dados = self.carregar_dados_github()
        if dados:
            if not dados.get('addons'):
                self.atualizar_status("Nenhum add-on disponível para download.")
                return
            self.mostrar_popup_download("ADD-ONS", dados['addons'], "Add-ons disponíveis para download", 
                                         'https://raw.githubusercontent.com/TROPADOBLACKSHEEP/SCRIPTbyBLACKSHEEP/refs/heads/main/SCRIPTimage/ADD-ONS-zip-03-10-2024.png')

    def mostrar_popup_download(self, titulo, lista_downloads, descricao, imagem_url):
        layout = BoxLayout(orientation='vertical', padding=15)
        layout.add_widget(Label(text=descricao, size_hint_y=None, height=40))

        imagem = self.baixar_e_exibir_imagem(imagem_url)
        layout.add_widget(imagem)

        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.do_scroll_x = False

        box_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        box_layout.bind(minimum_height=box_layout.setter('height'))

        for item in lista_downloads:
            button = Button(text=item['name'], size_hint_y=None, height=140)
            button.bind(on_press=lambda btn, url=item['url']: self.baixar_item(url))
            box_layout.add_widget(button)

        scroll_view.add_widget(box_layout)
        layout.add_widget(scroll_view)

        close_button = Button(text='Fechar', size_hint_y=None, height=60)
        close_button.bind(on_press=self.fechar_popup)
        layout.add_widget(close_button)

        self.popup_download = Popup(title=titulo, content=layout, size_hint=(0.6, 0.7))
        self.popup_download.open()

    def baixar_item(self, url):
        self.fechar_popup(None)  # Fecha o popup imediatamente após clicar
        Thread(target=self._baixar_item_thread, args=(url,)).start()

    def _baixar_item_thread(self, url):
        self.atualizar_status('Baixando item...')
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()

            nome_arquivo = os.path.basename(url)
            caminho_arquivo = os.path.join(self.pasta_download, nome_arquivo)

            with open(caminho_arquivo, 'wb') as f:
                f.write(resposta.content)

            Clock.schedule_once(lambda dt: self.atualizar_status(f'Item {nome_arquivo} baixado com sucesso!'), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.atualizar_status(f'Erro ao baixar o item: {str(e)}'), 0)

    def mostrar_popup_telegram(self, instance):
        content = BoxLayout(orientation='vertical', padding=15)

        telegram_url = "https://t.me/BLACKSHEEP_B"  # Substitua pelo link do seu canal

        imagem = self.baixar_e_exibir_imagem('https://raw.githubusercontent.com/TROPADOBLACKSHEEP/SCRIPTbyBLACKSHEEP/refs/heads/main/SCRIPTimage/redesocial.png')
        imagem.bind(on_touch_down=lambda instance, touch: self.redirecionar_telegram(touch, telegram_url))
        content.add_widget(imagem)

        close_btn = Button(text='Fechar', size_hint_y=None, height=60)
        close_btn.bind(on_press=self.fechar_popup)
        content.add_widget(close_btn)

        self.popup = Popup(title='Telegram', content=content, size_hint=(0.6, 0.4))
        self.popup.open()

    def redirecionar_telegram(self, touch, url):
        if touch.is_mouse_scrolling:  # Evitar a abertura ao rolar
            return False
        webbrowser.open(url)

    def mostrar_popup_sobre(self, instance):
        content = BoxLayout(orientation='vertical', padding=15)

        texto_sobre = (
            "Este aplicativo foi desenvolvido para oferecer uma\n"
            "interface intuitiva e acessível a usuários que buscam gerenciar e baixar\n"
            "scripts e recursos relacionados ao IPTV.\n"
            "Com um design amigável, o aplicativo permite que você verifique atualizações de\n"
            "scripts, baixe addons e combos, e acesse rapidamente conteúdo relevante.\n"
            "Os principais recursos incluem:\n"
            "Atualizações em Tempo Real:\n"
            "Receba notificações sobre novas versões de scripts e\n"
            "atualizações diretamente no aplicativo.\n"
            "Gerenciamento de Downloads: Baixe scripts, combos e addons com facilidade, armazenando-os em uma pasta dedicada.\n"
            "Acesso a Recursos: Navegue por uma lista de scripts e addons disponíveis, facilitando o uso de ferramentas IPTV.\n"
            "Integração com Telegram: Conecte-se a nossa comunidade via Telegram para suporte e novidades.\n\n"
            "Desenvolvido por BLACKSHEEP_B, este aplicativo é uma ferramenta indispensável para quem deseja otimizar sua experiência com IPTV.\n\n"
            "COPYRIGHT © TROPADOBLACKSHEEP."
        )
        label_sobre = Label(text=texto_sobre, size_hint_y=1, halign="left", valign="middle", color=(0.5, 1, 0.5, 1))
        label_sobre.bind(size=label_sobre.setter('text_size'))
        content.add_widget(label_sobre)

        imagem = self.baixar_e_exibir_imagem('https://raw.githubusercontent.com/Checkstatusiptv/Checkm3u/refs/heads/main/GITHUB-29-09-2024.png')
        imagem.size_hint_y = 0.2  # Reduzindo o tamanho da imagem
        content.add_widget(imagem)

        close_btn = Button(text='Fechar', size_hint_y=None, height=60)
        close_btn.bind(on_press=self.fechar_popup)
        content.add_widget(close_btn)

        self.popup = Popup(title='Sobre o Aplicativo', content=content, size_hint=(0.7, 0.7))
        self.popup.open()

class GerenciadorTela(ScreenManager):
    pass

class MeuApp(App):
    def build(self):
        self.tela_manager = GerenciadorTela()
        self.tela_manager.add_widget(TelaChecker(name='tela_checker'))
        self.tela_manager.add_widget(TelaTerminal(name='tela_terminal'))
        return self.tela_manager

if __name__ == '__main__':
    MeuApp().run()