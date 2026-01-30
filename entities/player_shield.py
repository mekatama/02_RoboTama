import pyxel

# arm1クラス
class Player_Shield:
    #定数

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.dir = 1
        self.is_Shield = False
        self.hit_area = (0, 0, 8, 16)  # 当たり判定の領域 (x1,y1,x2,y2) 

    # 更新する
    def update(self):
        if self.game.player.dir == 1:
            self.x = self.game.player.x + 15
        elif self.game.player.dir == -1:
            self.x = self.game.player.x - 7

        self.y = self.game.player.y

    # 描画する
    def draw(self):
        if self.is_Shield == True:
            # 4フレーム周期で0と8を交互に繰り返す
            u = pyxel.frame_count  // 8 % 2 * 8
            pyxel.blt(self.x, self.y, 0, 16 + u, 56, 8 * self.game.player.dir, 16, 0)
