import pyxel
from collision import get_tile_type, in_collision, push_back
from constants import TILE_EXIT, TILE_GEM, TILE_BOMB, TILE_SPIKE, TILE_WALL, TILE_ROAD

from .player_arm1 import Player_Arm1 # playerのarm1クラス 
from .player_bullet import PlayerBullet # playerのBulletクラス 
from .particle import Particle  # 破壊時particle

# プレイヤークラス
class Player:
    #定数
    MOVE_SPEED = 0.7          # 移動速度
    DASH_SPEED = 3         # 特殊移動速度
    SHOT_INTERVAL = 20      # 弾の発射間隔
    DASH_INTERVAL = 40       # dash間隔
    HP = 3                  # 初期HP

    # プレイヤーを初期化する
    def __init__(self, game, x, y):
        self.game = game        # ゲームへの参照
        self.x = x              # X座標
        self.y = y              # Y座標
        self.dir = 1            # 1:right -1:left
        self.type = 0           # 0:横 1:上 2:下
        self.isWalk = False     # Walk flag
        self.isDash = False     # Dash flag
        self.isDashInput = False# Dash入力 flag
        self.shot_timer = 0     # 弾発射までの残り時間
        self.dash_timer = 0     # dash時間
        self.hp = Player.HP     # HP
        self.hit_area = (0, 0, 16, 16)  # 当たり判定の領域 (x1,y1,x2,y2) 
        game.player_arm1 = Player_Arm1(game, self.x + 16, self.y + 16)  # プレイヤー

    # プレイヤーを更新する
    def update(self):
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            if self.isDash == False:
                self.isWalk = True
                self.x -= Player.MOVE_SPEED
                # particle発生
                self.game.particles.append(
                    Particle(self.game, self.x + 12, self.y + 16, self.dir,3)
                )
            else:
                self.x -= Player.DASH_SPEED
            self.dir = -1
            self.type = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            if self.isDash == False:
                self.isWalk = True
                self.x += Player.MOVE_SPEED
                self.game.particles.append(
                    Particle(self.game, self.x + 4, self.y + 16, self.dir,3)
                )
            else:
                self.x += Player.DASH_SPEED
            self.dir = 1
            self.type = 0
        #key入力が終わったら
        if pyxel.btnr(pyxel.KEY_RIGHT) or pyxel.btnr(pyxel.KEY_LEFT):
            self.isWalk = False
            self.type = 0

        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1
        
        # dash時間の制御
        if self.dash_timer > 0:
            self.dash_timer -= 1
            # particle発生
            self.game.particles.append(
                Particle(self.game, self.x + 8, self.y + 16, self.dir,2)
            )
        else:
            self.isDash = False
        
        # dash入力の制御
        if self.dash_timer > -15:
            self.dash_timer -= 1
        else:
            self.isDashInput = False

        # Sキー入力でdash
        if pyxel.btnp(pyxel.KEY_S) and self.isDashInput == False:
                self.isWalk = False
                self.isDash = True
                self.isDashInput = True
                self.dash_timer = Player.DASH_INTERVAL

        # auto攻撃
        if self.shot_timer == 0:
            # 向きで分岐
            if self.dir == 1:
                self.game.player_bullets.append(
                    PlayerBullet(self.game, self.x + 16, self.y + 2, self.dir, self.type)
                )
            else:
                self.game.player_bullets.append(
                    PlayerBullet(self.game, self.x - 8, self.y + 2, self.dir, self.type)
                )
            # 次の弾発射までの残り時間を設定する
            self.shot_timer = Player.SHOT_INTERVAL

        # 自機が画面外に出ないようにする(一画面用)
        self.x = max(self.x, 0)                 #大きい数値を使う
        self.x = min(self.x, pyxel.width - 8)   #小さい数値を使う
        self.y = max(self.y, 0)                 #大きい数値を使う
        self.y = min(self.y, pyxel.height - 8)   #小さい数値を使う
                    
    # プレイヤーを描画する
    def draw(self):
        # 4フレーム周期で0と16を交互に繰り返す
        u = pyxel.frame_count  // 8 % 2 * 16
        if self.isWalk == True:
            pyxel.blt(self.x, self.y, 0, 0 + u, 40, 16 * self.dir, 16, 0)
        elif self.isDash == True:
            pyxel.blt(self.x, self.y, 0, 16, 24, 16 * self.dir, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0 + u, 24, 16 * self.dir, 16, 0)
        pyxel.text(self.x - 4,  self.y - 6, "HP:%i" %self.hp, 7)
