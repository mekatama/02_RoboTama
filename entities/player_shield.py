import pyxel

# arm1クラス
class Player_Shield:
    #定数

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    # 更新する
    def update(self):
        if self.game.player.dir == 1:
            self.x = self.game.player.x + 9
        elif self.game.player.dir == -1:
            self.x = self.game.player.x - 1

        self.y = self.game.player.y + 8

    # 描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 8 % 2 * 8
        pyxel.blt(self.x, self.y, 0, 16 + u, 56, 8 * self.game.player.dir, 16, 0)
