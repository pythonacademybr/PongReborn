from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock


# Definição do
class Pong(Widget):
    """
    Esse elemento contém todos os elementos do jogo (campo, raquetes e
    bolinha). Nele também está a lógica de colisão da bolinha com as
    paredes da janela à fim de atualizar o placar do jogo.
    """

    # Referencia o objeto Bola definido no nosso arquivo .kv
    bola = ObjectProperty(None)

    # Referencia os objetos Raquete definidos no nosso arquivo .kv
    raquete_1 = ObjectProperty(None)
    raquete_2 = ObjectProperty(None)

    def __init__(self, screen_manager=None):
        super(Pong, self).__init__()
        self.screen_manager = screen_manager

    # Põe a bola em jogo
    def servico(self, vel=(4, 0)):

        # Posiciona a bola no centro da tela
        self.bola.center = self.center

        # Seta a velocidade da bola
        self.bola.velocidade = vel

    # Atualiza nosso jogo
    def atualiza(self, dt):

        # Faz a bola se mover
        self.bola.movimenta()

        # Rebate a bola caso haja colisão com a bolinha
        self.raquete_1.rebate_bola(self.bola)
        self.raquete_2.rebate_bola(self.bola)

        # Verifica se a bola atingiu o topo da janela
        if (self.bola.y < 0) or (self.bola.top > self.height):
            self.bola.velocidade_y *= -1

        # Verifica se colidiu com o lado esquerdo da janela para atualizar o
        # placar do jogo
        if self.bola.x < self.x:
            # +1 para o placar da raquete_2
            self.raquete_2.placar += 1

            if self.raquete_2.placar >= 1:
                self.servico(vel=(0, 0))
                self.raquete_1.placar = 0
                self.raquete_2.placar = 0
                self.screen_manager.current = "vencedor_2"

                return

            # Reinicia o jogo com a bola saindo pelo lado esquerdo
            self.servico(vel=(4, 0))

        # Verifica se colidiu com o lado direito da janela para atualizar o
        # placar do jogo
        if self.bola.x > self.width:
            # +1 para o placar da raquete_1
            self.raquete_1.placar += 1

            if self.raquete_1.placar >= 1:
                self.servico(vel=(0, 0))
                self.raquete_1.placar = 0
                self.raquete_2.placar = 0
                self.screen_manager.current = "vencedor_1"

                return

            # Reinicia o jogo com a bola saindo pelo lado direito
            self.servico(vel=(-4, 0))

    # Captura o evento on_touch_move (arrastar de dedo na tela)
    def on_touch_move(self, touch):
        # Verifica se toque foi do lado esquerdo da tela
        if touch.x < self.width / 2:
            # Atualiza altura da raquete esquerda
            self.raquete_1.center_y = touch.y

        # Verifica se toque foi do lado direito da tela
        if touch.x > self.width - self.width / 2:
            # Atualiza altura da raquete direita
            self.raquete_2.center_y = touch.y

    def remove_btn(self, btn):

        # Remove o botão de iniciar jogo
        self.remove_widget(btn)

    def comeca_jogo(self):

        # Pôe a bola em jogo
        self.servico()

        # Agendamento da função "atualiza" a cada 1/120 = 0,008s
        Clock.schedule_interval(self.atualiza, 1.0/120.0)

    def reinicia_jogo(self):
        # Pôe a bola em jogo
        self.servico(vel=(4,0))

        self.raquete_1.placar = 0
        self.raquete_2.placar = 0
