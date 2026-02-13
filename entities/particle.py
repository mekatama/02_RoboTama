import pyxel
import math

#■Particle
class Particle:
    #定数
    START_RADIUS = 3    # 弾軌跡開始時の半径
    END_RADIUS = 1      # 弾軌跡終了時の半径

    def __init__(self, game, x, y, dir, type):
        self.x = x
        self.y = y
        self.dir = dir      # playerの方向
        self.type = type    # 0:全方位 1:弾軌跡 2:dash 3:walk 4:破片
        self.timer = 0
        self.count = 0
        self.speed = 2.5    # 速度
        self.speed_walk = 1.5 #速度
        self.aim = 0        # 攻撃角度
        self.rot = 0        # 破片の回転
        self.vx = 1.5         # 放物線用
        self.vy = -2         # 放物線用
        self.gravity = 0.2  # 放物線用
        self.is_alive = True
        self.radius = Particle.START_RADIUS  # 弾軌跡の半径

    def update(self):
        if self.type == 0:
            #一定間隔で角度決定→消滅
            self.count += 1
            if self.count == 1:
                self.aim = pyxel.rndf(0, 2 * math.pi)
            if self.count >= 1 + pyxel.rndi(1, 20):
                self.is_alive = False
            #座標
            self.x += self.speed * math.cos(self.aim)
            self.y += self.speed * -math.sin(self.aim)
        elif self.type == 1:
            # 半径を小さくする
            self.radius -= 0.3
            # 半径が最小になったらエフェクトリストから登録を削除する
            if self.radius < Particle.END_RADIUS:
                 self.is_alive = False
        elif self.type == 2:
            # dash方向の逆に表示
            self.count += 1
            if self.count == 1:
                if self.dir == -1:
                    self.aim = pyxel.rndf(0, 0.9)
                elif self.dir == 1:
                    self.aim = pyxel.rndf(2.2, 3.1)
            if self.count >= 1 + pyxel.rndi(1, 20):
                self.is_alive = False
            #座標
            self.x += self.speed * math.cos(self.aim)
            self.y += self.speed * -math.sin(self.aim)
        elif self.type == 3:
            # walkに合わせて表示
            self.count += 1
            if self.count == 1:
                if self.dir == -1:
                    self.aim = pyxel.rndf(0, 0.9)
                elif self.dir == 1:
                    self.aim = pyxel.rndf(2.2, 3.1)
            if self.count >= 1 + pyxel.rndi(1, 5):
                self.is_alive = False
            #座標
            self.x += self.speed_walk * math.cos(self.aim)
            self.y += self.speed_walk * -math.sin(self.aim)
        elif self.type == 4:
            if self.count == 0:
                self.rnd_x = pyxel.rndf(-1, 1)
                self.rnd_y = pyxel.rndf(-1, 1)
                print(self.rnd_x)

            self.count += 1
            self.vy += self.gravity
            self.x += (self.vx + self.rnd_x) * self.dir
            self.y += (self.vy + self.rnd_y)
#            self.x += (self.vx + pyxel.rndf(0, 0.5)) * self.dir
#            self.y += (self.vy + pyxel.rndf(0, 1.0))

            if self.count > 25 + pyxel.rndi(-5, 5):
                self.is_alive = False
            #座標

    def draw(self):
        self.rot += 10
        if self.type == 0 or self.type == 2 or self.type == 3:
            pyxel.pset(self.x, self.y, 7)
        elif self.type == 1:
            pyxel.circ(self.x, self.y, self.radius, 7)
        elif self.type == 4:
            pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.dir , 8, 0, self.rot)
