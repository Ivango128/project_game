from pygame import *
import math
font.init()

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.size_x = size_x
        self.size_y = size_y
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    # метод, в котором реализовано управление спрайтом по кнопкам стрелкам клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:  # идём направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)  # если коснулись сразу нескольких, то правый край - минимальный из возможных
        elif self.x_speed < 0:  # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)  # если коснулись нескольких стен, то левый край - максимальный
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # идем вниз
            for p in platforms_touched:
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:  # идём вверх
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)  # выравниваем верхний край по нижним краям стенок, на которые наехали

    def fire(self, x, y):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15, x, y)
        bullets.add(bullet)


class Enamy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, x_speed, start, end):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = x_speed
        self.start = start
        self.end = end
        self.direction = "left"
    
    def update(self):
        if self.rect.x <= self.start:
         self.direction = "right"
        if self.rect.x >= self.end:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, x_speed, end_x, end_y):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = x_speed
        self.end_x = end_x - player_x
        self.end_y = end_y - player_y
        self.end_a = abs(self.end_y/self.end_x)*10
        self.player_x = player_x
        self.player_y = player_y


    def update(self):
        if self.end_x < 0 and self.end_y < 0:
            self.rect.x -=10
            self.rect.y -=self.end_a

        elif self.end_x < 0 and self.end_y > 0:
            self.rect.x -= 10
            self.rect.y += self.end_a

        elif self.end_x > 0 and self.end_y < 0:
            self.rect.x += 10
            self.rect.y -= self.end_a

        elif self.end_x > 0 and self.end_y > 0:
            self.rect.x += 10
            self.rect.y += self.end_a

        if self.rect.x > win_width+self.size_x or self.rect.x < 0-self.size_x:
            self.kill()
        elif self.rect.y > win_height+self.size_y or self.rect.y < 0-self.rect.y:
            self.kill()

# Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)  # задаём цвет согласно цветовой схеме RGB

# создаём группу для стен
barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

# создаём стены картинки
w1 = GameSprite('wall1.jpg', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('wall2.jpg', 370, 100, 50, 400)

# добавляем стены в группу
barriers.add(w1)
barriers.add(w2)

# создаём спрайты
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)

monster = Enamy('enamy.png', win_width - 80, 180, 80, 80, 2, start = 470,  end = win_width - 85)
monster2 = Enamy('enamy.png', 0, 0, 80, 80, 4, 0, 300)

monsters.add(monster)
monsters.add(monster2)

final_sprite = GameSprite('hero.png', win_width - 85, win_height - 100, 80, 80)

win = font.SysFont('Arial', 60).render('Вы победили', True, (0,0,0))
lose = font.SysFont('Arial', 60).render('Вы проиграли', True, (0,0,0))

# переменная, отвечающая за то, как кончилась игра
finish = True
# игровой цикл
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            # elif e.key == K_SPACE:
            #     packman.fire()
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = mouse.get_pos()
            packman.fire(x, y)
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if finish != False:
        window.fill(back)  # закрашиваем окно цветом
        # рисуем объекты
        barriers.draw(window)
        bullets.draw(window)
        monsters.draw(window)

        final_sprite.reset()
        packman.reset()
        # включаем движение
        packman.update()
        monsters.update()
        bullets.update()

        # Проверка столкновения героя с врагом и финальным спрайтом
        if sprite.spritecollide(packman, monsters, True):
            finish = False
            window.blit(lose, (win_width/3, win_height/3))
            

        if sprite.collide_rect(packman, final_sprite):
            finish = False
            window.blit(win, (win_width/3, win_height/3))

        sprite.groupcollide(bullets, monsters, True, True)

        sprite.groupcollide(bullets, barriers, True, False)

        

    time.delay(50)
    display.update()
