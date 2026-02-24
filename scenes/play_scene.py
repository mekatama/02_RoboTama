import pyxel
from entities import Player, Enemy1

from collision import get_tile_type
from constants import (
    SCROLL_BORDER_X_RIGHT,
    SCROLL_BORDER_X_LEFT,
    TILE_ZAKO1_POINT,
    TILE_ZAKO2_POINT
)

# 当たり判定用の関数
#   タプルで設定した当たり判定領域を使用して判定
def check_collision(entity1, entity2):
    #キャラクター1の当たり判定座標を設定
    entity1_x1 = entity1.x + entity1.hit_area[0]
    entity1_y1 = entity1.y + entity1.hit_area[1]
    entity1_x2 = entity1.x + entity1.hit_area[2]
    entity1_y2 = entity1.y + entity1.hit_area[3]

    #キャラクター2の当たり判定座標を設定
    entity2_x1 = entity2.x + entity2.hit_area[0]
    entity2_y1 = entity2.y + entity2.hit_area[1]
    entity2_x2 = entity2.x + entity2.hit_area[2]
    entity2_y2 = entity2.y + entity2.hit_area[3]

    # キャラクター1の左端がキャラクター2の右端より右にある
    if entity1_x1 > entity2_x2: #成立すれば衝突していない
        return False
    # キャラクター1の右端がキャラクター2の左端より左にある
    if entity1_x2 < entity2_x1: #成立すれば衝突していない
        return False
    # キャラクター1の上端がキャラクター2の下端より下にある
    if entity1_y1 > entity2_y2: #成立すれば衝突していない
        return False
    # キャラクター1の下端がキャラクター2の上端より上にある
    if entity1_y2 < entity2_y1: #成立すれば衝突していない
        return False
    # 上記のどれでもなければ重なっている
    return True #衝突している

# プレイ画面クラス
class PlayScene:
    # プレイ画面を初期化する
    def __init__(self, game):
        self.game = game
        self.countEnemySpawn = 0    # 敵の生成用count
    # プレイ画面を開始する
    def start(self):
        # 変更前のマップに戻す
        pyxel.tilemaps[0].blt(0, 0, 2, 0, 0, 256, 16)
        # プレイ画面の状態を初期化する
        game = self.game        # ゲームクラス
        game.score = 0          # スコア
        game.player = Player(game, 100, 96)  # プレイヤー

    # プレイ画面を更新する
    def update(self):
        game = self.game
        player = game.player
        player_arm1 = game.player_arm1
        player_shield = game.player_shield
        player_bullets = game.player_bullets
        player_bombs = game.player_bombs
        enemies = game.enemies
        enemy_bullets = game.enemy_bullets
        particles = game.particles

        self.countEnemySpawn += 1
        if self.countEnemySpawn > 90:
            #敵を生成する
            self.game.enemies.append(
                Enemy1(self.game, 64, 96)
            )
            self.countEnemySpawn = 0

        # プレイヤーを更新する
        if player is not None: #NONE使用時は判定方法が特殊
            player.update()

        # arm1を更新する
        if player_arm1 is not None: #NONE使用時は判定方法が特殊
            player_arm1.update()

        # shieldを更新する
        if player_shield is not None: #NONE使用時は判定方法が特殊
            player_shield.update()

        # 弾(プレイヤー)を更新する
        for player_bullet in player_bullets.copy():
            player_bullet.update()
            # 弾(プレイヤー)と敵が接触したら消去
            for enemy in enemies.copy():
                if check_collision(enemy, player_bullet):
                    player_bullet.add_damage()  # 自機の弾にダメージを与える
                    enemy.add_damage()          # 敵にダメージを与える

        # 爆弾を更新する
        for player_bomb in player_bombs.copy():
            player_bomb.update()
            # 爆弾とplayerが接触したら消去
#            if player is not None and check_collision(player, bomb):
#                bomb.bomb_get()

        # 敵を更新する
        for enemy in enemies.copy():
            enemy.update()
            # 弾(プレイヤー)と敵が接触したらゲームオーバー
            if player is not None:
                if check_collision(enemy, player):
                    game.change_scene("gameover")
                    return

        # 敵の弾を更新する
        for enemy_bullet in enemy_bullets.copy():
            enemy_bullet.update()
            # 弾(enemy)とplayerが接触したら消去
            if player is not None and check_collision(player, enemy_bullet):
                enemy_bullet.add_damage()         # 敵の弾にダメージを与える
                game.change_scene("gameover")
                return
            # 弾(enemy)とshieldが接触したら消去
            if player_shield is not None and check_collision(player_shield, enemy_bullet):
                if player_shield.is_Shield == True:
                    enemy_bullet.add_damage()         # 敵の弾にダメージを与える
                    return

        # 破壊時particlesを更新する
        for particle in particles.copy():
            particle.update()
            # flag onで消す処理入れたい
            if particle.is_alive == False:
                if particle in particles:  # リストに登録されている時
                    particles.remove(particle)

        # [debug]キー入力をチェックする
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            # プレイ画面に切り替える
            self.game.change_scene("gameover")

    # プレイ画面を描画する
    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)
        # フィールドを描画する
        self.game.draw_field()
        # arm1を描画する
        self.game.draw_player_arm1()
        # プレイヤーを描画する
        self.game.draw_player()
        # shieldを描画する
        self.game.draw_player_shield()
        # 弾(プレイヤー)を描画する
        self.game.draw_player_bullets()
        # 爆弾を描画する
        self.game.draw_player_bombs()
        # 敵を描画する
        self.game.draw_enemies()
        # 敵の弾を描画する
        self.game.draw_enemy_bullets()
        # 破壊時particleを描画する
        self.game.draw_particles()

        # スコアを描画する
#        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

        # テキストを描画する
        pyxel.text(31, 108, "- PRESS ENTER -", 6)
