import pygame
import os
import re

class Word:
    def __init__(self, word):
        word_list = word.replace('.png', '').split('-')
        self.word = dict()
        self.word['en'] = word_list[0]
        self.word['ru'] = word_list[1]
        self.filename = os.path.join('images', word)

    def draw(self, lang, screen):
        self.chars = []
        screen.fill((200, 255, 200))
        img_surf = pygame.image.load(self.filename)
        # ругается на неправильный формат - надо исправить и еще сделать авторесайз на 400 точек
        img_rect = img_surf.get_rect(bottomright=(400, 400))
        screen.blit(img_surf, img_rect)
        for i, char in enumerate(list(self.word[lang])):
            self.chars.append(Char(char.upper(), (0, 100, 0), (50 * (i + 1), 500)))
            self.chars[-1].draw(screen)


class Char:    
    def __init__(self, char, color, coords):
        self.text = char
        self.color = color
        self.coords = coords

    def draw(self, screen):        
        self.surf = game.font.render(self.text, 1, self.color)
        self.place = self.surf.get_rect(center=self.coords)
        screen.blit(self.surf, self.place)
        pygame.display.update()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.font = pygame.font.Font(None, 72)
        self.lang = 'en'
        self.word_list = self.word_list_gen()
        self.word_idx = 0
        self.word = self.word_list[self.word_idx]

    def word_list_gen(self):
        # Создает список имен файлов формата 'слово на английском'-'слово на русском'.png
        word_list = []
        with os.scandir('images') as entries_list:
            for entry in entries_list:
                if re.match( r'\w*\-\w*\.png', entry.name) is not None:
                    word_list.append(Word(entry.name))
                else:
                    print(f'{entry.name} не соответствует формату')
        return word_list

    def redraw(self):
         self.word.draw(self.lang,  self.screen)
         self.char_idx = 0
         self.won = False

    def run(self):        
        self.redraw()
        while True:
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                current_char = self.word.chars[self.char_idx]
                if event.type == pygame.KEYDOWN:                    
                    if event.unicode == current_char.text.lower():
                        current_char.color = (100, 0, 0)
                        current_char.draw(self.screen)
                        if self.char_idx < len(self.word.chars) - 1:
                            self.char_idx += 1
                        elif not self.won:
                            self.won = True
                            print('YOU WON!')
                            # тут будет какой-то звук или картинка, про победу

                    if event.key == pygame.K_UP and self.lang == 'en':
                        self.lang = 'ru'
                        self.redraw()
                    elif event.key == pygame.K_DOWN and self.lang == 'ru':
                        self.lang = 'en'
                        self.redraw()
                    elif event.key == pygame.K_RIGHT and self.word_idx < len(self.word_list) - 1:
                        self.word_idx += 1
                        self.word = self.word_list[self.word_idx]
                        self.redraw()
                    elif event.key == pygame.K_LEFT and self.word_idx > 0:
                        self.word_idx -= 1
                        self.word = self.word_list[self.word_idx]
                        self.redraw()

if __name__ == '__main__':
    game = Game()
    game.run()
