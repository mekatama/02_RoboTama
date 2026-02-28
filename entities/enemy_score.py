import pyxel

#■Enemy_Score
class Enemy_Score:
    #定数

    def __init__(self, game, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.count = 0
        self.is_alive = True

    def update(self):
        self.count += 1
        if self.count < 20:
            self.y -= 1
        elif self.count >= 20:
            self.is_alive = False

    def draw(self):
#        pyxel.text(self.x,  self.y, "Score", 7)
        pyxel.text(self.x, self.y, f"+{self.score:2}", 7)
