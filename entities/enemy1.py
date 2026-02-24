import pyxel
import math
#from collision import in_collision, push_back
from .enemy_bullet import Enemy_Bullet  # enemyのBulletクラス 
from .particle import Particle  # 破壊時particle

# 敵クラス
class Enemy1:
    #定数
    KIND_A = 0  # 敵A(空中)
    KIND_B = 1  # 敵B(地上停止)
    KIND_C = 2  # 敵C(地上移動)
    enemy_bullets = []     # 敵の弾のリスト

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.dir = 1                    # 1:right -1:left
        self.life_time = 0              # 生存時間
        self.armor = 2                  # 装甲
        self.is_walk = False            #
        self.is_damaged = False         # ダメージを受けたかどうか
        self.hit_area = (0, 0, 16, 16)  # 当たり判定の領域 (x1,y1,x2,y2) 

    # 敵にダメージを与える
    def add_damage(self):
        if self.armor > 0:  # 装甲が残っている時
            self.armor -= 1
            self.is_damaged = True
            # ダメージ音を再生する
#            pyxel.play(2, 1, resume=True)   # チャンネル2で割り込み再生させる
            return                          # 処理終了
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
        # 生存時間をカウントする
        self.life_time += 1
        # 仮walk
#        self.x -= 1
        self.dir = 1
        self.is_walk = False
        # [仮]Aキー入力で攻撃
        if pyxel.btnp(pyxel.KEY_A):
            self.game.enemy_bullets.append(
                Enemy_Bullet(self.game, self.x, self.y + 4, self.dir)
            )
        """
        # 敵A(空中)を更新する
        if self.kind == Zako1.KIND_A:
            pass

        # 敵B(地上停止)を更新する
        elif self.kind == Zako1.KIND_B:
            pass

        # 敵C(地上移動)を更新する
        elif self.kind == Zako1.KIND_C:
            pass
        """
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

