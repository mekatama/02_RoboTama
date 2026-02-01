import pyxel
from .particle import Particle  # 破壊時particle
from .particle_hit import ParticleHit  # 破壊時particle

# 弾クラス
class PlayerBullet:
    #定数
    SHOT_SPEED_X = 4        # shot speed x
    SHOT_SPEED_Y = 4        # shot speed y
    PARTICLE_INTERVAL = 2  # particleの発生間隔
    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y, dir, type):
        self.game = game
        self.x = x
        self.y = y
        self.dir = dir
        self.type = type        # 0:通常弾 1:近接攻撃
        self.life_time = 0      # 生存時間
        self.particle_time = 0  # particle発生タイマー
        self.hit_area = (2, 2, 5, 5)  # 当たり判定領域

     # 弾にダメージを与える
    def add_damage(self):
        # パーティクル出す
        for i in range(10):
            self.game.particles.append(
                Particle(self.game, self.x + 4, self.y + 4, self.dir,0)
            )
        # hitパーティクル出す
        self.game.particleHits.append(
            ParticleHit(self.game, self.x + 4, self.y + 4)
        )
        # 弾をリストから削除する
        if self in self.game.player_bullets:    # 自機の弾リストに登録されている時
            self.game.player_bullets.remove(self)

   # 弾を更新する
    def update(self):
        #生存時間カウント
        self.life_time += 1
        # 弾の座標を更新する(type 0:横 1:上 2:下)
        if self.type == 0:
            self.x += PlayerBullet.SHOT_SPEED_X * self.dir
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
                self.particle_time = PlayerBullet.PARTICLE_INTERVAL
        elif self.type == 1:
            self.x = self.x
            if self.life_time > 5:
                # 弾をリストから削除する
                if self in self.game.player_bullets:    # 自機の弾リストに登録されている時
                    self.game.player_bullets.remove(self)


        """
        # 弾が画面外に出たら弾リストから登録を削除する
        if (self.x <= -8 or
            self.x >= pyxel.width or
            self.y <= -8 or
            self.y >= pyxel.height
        ):
            self.game.player_bullets.remove(self)
        """
    # 弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.dir , 8, 0)
