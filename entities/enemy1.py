import pyxel
import math
#from collision import in_collision, push_back
from .enemy_bullet import Enemy_Bullet  # enemyのBulletクラス 
from .enemy_score import Enemy_Score  # enemyのScoreクラス 
from .particle import Particle  # 破壊時particle

# 敵クラス
class Enemy1:
    #定数
    KIND_A = 0  # 敵A(前進のみ)
    KIND_B = 1  # 敵B(画面内に少し入って停止から攻撃loop)
    KIND_C = 2  # 敵C(前進と攻撃をloop)
    SHOT_INTERVAL_B = 100      # 弾の発射間隔
    SHOT_INTERVAL_C = 40   # 弾の発射間隔
    enemy_bullets = []     # 敵の弾のリスト

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y, dir, kind):
        self.game = game
        self.x = x
        self.y = y
        self.dir = dir                  # 1:right -1:left
        self.stop_time = 0              # 生存時間
        self.shot_timer = 0             # 弾発射までの残り時間
        self.armor = 1                  # 装甲
        self.kind = kind                # enemy種
        self.hp = self.armor + 1
        self.stiffness = 0              # 硬直時間のカウント
        self.is_walk = True             #
        self.is_damaged = False         # ダメージを受けたかどうか
        self.is_charge = False          # 体当たりされたflag
        self.hit_area = (0, 0, 16, 16)  # 当たり判定の領域 (x1,y1,x2,y2) 

    # 敵にダメージを与える
    def add_damage(self):
        if self.armor > 0:  # 装甲が残っている時
            self.armor -= 1
            self.hp -= 1
            self.is_damaged = True
            # ダメージ音を再生する
#            pyxel.play(2, 1, resume=True)   # チャンネル2で割り込み再生させる
            return                          # 処理終了
        # scoreを生成する
        self.game.enemy_scores.append(
            Enemy_Score(self.game, self.x + 8, self.y, 10)
        )
        # 爆発エフェクトを生成する
        self.game.particles.append(
            Particle(self.game, self.x + 8, self.y + 8, 0, 6)
        )
        # 爆発(ランダム)エフェクトを生成する
        for i in range(4):
            self.game.particles.append(
                Particle(self.game, self.x + 8, self.y + 8, 0, 7)
            )
        # 破片
        for i in range(2):
            self.game.particles.append(
                Particle(self.game, self.x + 4, self.y + 8, 1, 4)
            )
        for i in range(2):
            self.game.particles.append(
                Particle(self.game, self.x + 4, self.y + 8, -1, 4)
            )
        """
        # アイテムを生成する
        # ■■■■後からランダムにする■■■■
        Item(self.game, self.x, self.y)
        """
        # 敵をリストから削除する
        if self in self.game.enemies:  # 敵リストに登録されている時
            self.game.enemies.remove(self)
        # スコアを加算する
#        self.game.score += self.level * 10
            
    # 敵を更新する
    def update(self):
        # 停止判定をカウントする
        self.stop_time += 1
        # playerの体当たり後の硬直時間
        if self.is_charge == True:
            self.stiffness += 1
            if self.stiffness > 60:
                self.is_charge = False
                self.stiffness = 0  # 初期化

        # 敵A
        if self.kind == Enemy1.KIND_A and self.is_charge == False:
            if self.dir == -1:
                self.x -= 1 # walk
            elif self.dir == 1:
                self.x += 1 # walk

        # 敵B
        elif self.kind == Enemy1.KIND_B and self.is_charge == False:
            # 弾の発射間隔timer制御
            if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
                self.shot_timer -= 1
            # walk判定
            if self.stop_time > 20:
                self.is_walk = False
            # 行動分岐        
            if self.is_walk == True:
                if self.dir == -1:
                    self.x -= 1 # walk
                elif self.dir == 1:
                    self.x += 1 # walk
            else:
                # 攻撃
                if self.shot_timer == 0 :
                    # 向きで分岐
                    if self.dir == 1:
                        self.game.enemy_bullets.append(
                            Enemy_Bullet(self.game, self.x + 16, self.y + 4, self.dir)
                        )
                    else:
                        self.game.enemy_bullets.append(
                            Enemy_Bullet(self.game, self.x - 8, self.y + 4, self.dir)
                        )
                    # 次の弾発射までの残り時間を設定する
                    self.shot_timer = Enemy1.SHOT_INTERVAL_B

        # 敵C
        elif self.kind == Enemy1.KIND_C and self.is_charge == False:
            # walk判定
            if self.stop_time == 20:
                self.is_walk = False
            elif self.stop_time == 60:
                self.is_walk = True
                self.stop_time = 0  # 初期化
            # 行動分岐        
            if self.is_walk == True:
                if self.dir == -1:
                    self.x -= 1 # walk
                elif self.dir == 1:
                    self.x += 1 # walk
            else:
                # 弾の発射間隔timer制御
                if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
                    self.shot_timer -= 1
                # 攻撃
                if self.shot_timer == 0 :
                    # 向きで分岐
                    if self.dir == 1:
                        self.game.enemy_bullets.append(
                            Enemy_Bullet(self.game, self.x + 16, self.y + 4, self.dir)
                        )
                    else:
                        self.game.enemy_bullets.append(
                            Enemy_Bullet(self.game, self.x - 8, self.y + 4, self.dir)
                        )
                    # 次の弾発射までの残り時間を設定する
                    self.shot_timer = Enemy1.SHOT_INTERVAL_C
        # 仮walk
#        self.x -= 1
#        self.dir = 1
        # [仮]Aキー入力で攻撃
        if pyxel.btnp(pyxel.KEY_A):
            self.game.enemy_bullets.append(
                Enemy_Bullet(self.game, self.x, self.y + 4, self.dir)
            )

    # 敵を描画する
    def draw(self):
        # 4フレーム周期で0と16を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 16
        if self.is_walk == True:
            if self.is_damaged:
                #ダメージ演出
                self.is_damaged = False
                for i in range(1, 15):
                    pyxel.pal(i, 15)    #カラーパレットの色を置き換える
                pyxel.blt(self.x, self.y, 0, 32 + u, 56, 16 * self.dir, 16, 0)
                pyxel.pal() #カラーパレット元に戻す
            else:
                pyxel.blt(self.x, self.y, 0, 32 + u, 56, 16 * self.dir, 16, 0)
        else:
            if self.is_damaged:
                #ダメージ演出
                self.is_damaged = False
                for i in range(1, 15):
                    pyxel.pal(i, 15)    #カラーパレットの色を置き換える
                pyxel.blt(self.x, self.y, 0, 32 + u, 40, 16 * self.dir, 16, 0)
                pyxel.pal() #カラーパレット元に戻す
            else:
                pyxel.blt(self.x, self.y, 0, 32 + u, 40, 16 * self.dir, 16, 0)

        pyxel.text(self.x - 4,  self.y - 6, "HP:%i" %self.hp, 7)
