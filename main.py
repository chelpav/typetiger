import pygame
import os
import re

class Word:
    def __init__(self, word):
        word_list = word.split('-')
        self.word = dict()
        self.word['en'] = word_list[0]
        self.word['ru'] = word_list[1]
        self.filename = f'images//{word}.png'        

    def draw(self, lang):
        self.chars = []
        game.screen.fill((200, 255, 200))  
        img_surf = pygame.image.load(self.filename)
        img_rect = img_surf.get_rect(bottomright=(400, 400))
        game.screen.blit(img_surf, img_rect)
        for i, char in enumerate(list(self.word[lang])):                  
            self.chars.append(Char(char.upper(), (0, 100, 0), (50 * (i + 1), 500)))
            self.chars[-1].draw()
        

class Char:    
    def __init__(self, char, color, coords):
        self.text = char
        self.color = color
        self.coords = coords

    def draw(self):        
        self.surf = game.font.render(self.text, 1, self.color)
        self.place = self.surf.get_rect(center=self.coords)
        game.screen.blit(self.surf, self.place)
        pygame.display.update()

class Game:
    def __init__(self):
        pygame.init()       
        self.screen = pygame.display.set_mode((600, 600))
        self.font = pygame.font.Font(None, 72)
        self.lang = 'en'
        self.word_list = self.word_list_gen()        

    def word_list_gen(self):
        word_list = []
        with os.scandir('images') as listOfEntries:
            for entry in listOfEntries:
                if re.match( r'\w*\-\w*\.png', entry.name) is not None:                    
                    word_list.append(Word(entry.name.replace('.png', '')))
                else:
                    print(f'{entry.name} не соответствует формату')
        return word_list

    def redraw(self):
         self.word.draw(self.lang)
         self.char_idx = 0
         self.won = False

    def run(self):
        self.word_idx = 0
        self.word = self.word_list[self.word_idx]
        self.word.draw(self.lang)
        self.won = False

        self.char_idx = 0
        while True:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                current_char = self.word.chars[self.char_idx]
                if event.type == pygame.KEYDOWN:                
                    if event.unicode == current_char.text.lower():
                        current_char.color = (100, 0, 0)
                        current_char.draw()
                        if self.char_idx < len(self.word.chars) - 1:
                            self.char_idx += 1
                        elif not self.won:
                            self.won = True
                            print('YOU WON!')
                        
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


