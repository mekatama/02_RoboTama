import pyxel

# 爆弾クラス
class Player_Arm1:
    #定数

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    # 爆弾を更新するgame.
    def update(self):
        pass

    # 爆弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 40, 40, 8, 8, 0)
