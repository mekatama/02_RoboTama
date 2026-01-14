import pyxel

# arm1クラス
class Player_Arm1:
    #定数

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    # arm1を更新する
    def update(self):
            self.x = self.game.player.x + 8
            self.y = self.game.player.y + 4

    # arm1を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 40, 40, 8, 8, 0)
