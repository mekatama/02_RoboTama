import pyxel
from .particle import Particle  # 破壊時particle
# from .particle_hit import ParticleHit  # 破壊時particle

# 弾クラス
class Enemy_Bullet:
    #定数
    SHOT_SPEED_X = 2        # shot speed x
    PARTICLE_INTERVAL = 4   # particleの発生間隔

    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y, dir):
        self.game = game
        self.x = x
        self.y = y
        self.dir = dir
        self.particle_time = 0  # particle発生タイマー
        self.life_time = 0  #生存時間
        self.hit_area = (2, 2, 5, 5)  # 当たり判定領域

     # 弾にダメージを与える
    def add_damage(self):
        # hitパーティクル出す
        if self.dir == 1:
            self.game.particles.append(
                Particle(self.game, self.x + 6, self.y + 4, 0, 5)
            )
        else:
            self.game.particles.append(
                Particle(self.game, self.x, self.y + 4, 0, 5)
            )

        # 弾をリストから削除する
        if self in self.game.enemy_bullets:    # 自機の弾リストに登録されている時
            self.game.enemy_bullets.remove(self)

   # 弾を更新する
    def update(self):
        #生存時間カウント
        self.life_time += 1
        # 弾の座標を更新する
        self.x += Enemy_Bullet.SHOT_SPEED_X * self.dir

        # particle発生間隔
        if self.particle_time > 0:
            self.particle_time -= 1
        # particle発生
        if self.particle_time == 0:
            tmp_x = self.x
            tmp_y = self.y
            if self.dir == 1:
                self.game.particles.append(
                    Particle(self.game, tmp_x - 2, tmp_y + 4, self.dir, 1)
                )
            elif self.dir == -1:
                self.game.particles.append(
                    Particle(self.game, tmp_x + 10, tmp_y + 4, self.dir, 1)
                )
            # 次の弾発射までの残り時間を設定する
            self.particle_time = Enemy_Bullet.PARTICLE_INTERVAL

        # 弾が画面外に出たら弾リストから登録を削除する
        if (self.x <= -8 or
            self.x >= pyxel.width or
            self.y <= -8 or
            self.y >= pyxel.height
        ):
            self.game.enemy_bullets.remove(self)
        
    # 弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.dir, 8, 0)
