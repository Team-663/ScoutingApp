# Import QRCode from pyqrcode
import os
import pyqrcode
import pygame
import png
import random, string, sys, time
from pyqrcode import QRCode

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()

DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 800


class qrTest:
    def __init__(self):
        self.qr = None
        self.qrstring = None
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('CSU QR Test')

    def run(self):
        running = True
        self.nextQR()
        self.startupScreen()
        time.sleep(2)
        self.background()
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.stop()

                self.background(self.qr)
                self.buttons()
                pygame.display.update()
            self.clock.tick(15)

    def startupScreen(self):
        # blits the text to the screen an top of the background
        self.background()
        fontName = pygame.font.get_default_font()
        font = pygame.font.Font(fontName, 32)
        text = font.render('CSU QR Test', True, (0, 0, 0))
        self.screen.blit(text, (150, 200))
        pygame.display.update()

    def background(self, qr = None):
        # sets the background to the triangle thing
        lightPurple = (104, 20, 168)
        darkPurple = (71, 10, 145)
        darkestPurple = (45, 6, 112)
        self.screen.fill((125, 125, 125))
        pygame.draw.polygon(self.screen, lightPurple, ((0, 0), (650, 0), (0, 450)))
        pygame.draw.polygon(self.screen, darkPurple, ((0, 0), (425, 0), (0, 225)))
        pygame.draw.polygon(self.screen, darkestPurple, ((0, 0), (212, 0), (0, 100)))
        if qr:
            image = pygame.image.load(qr)
            self.screen.blit(image, (400, 300))
            fontName = pygame.font.get_default_font()
            font = pygame.font.Font(fontName, 32)
            text = font.render(self.qrstring, True, (0, 0, 0))
            self.screen.blit(text, (150, 200))
        pygame.display.update()

    def stop(self):
        self.startupScreen()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    def buttons(self):  # displays and manages buttons
        lightestPurple = (122, 48, 191)
        lightPurple = (71, 6, 150)
        purple = (56, 5, 110)
        fontName = pygame.font.get_default_font()
        font = pygame.font.Font(fontName, 20)
        # checks if mouse is on button
        mouse = pygame.mouse.get_pos()
        if 900 + 100 > mouse[0] > 900 and 750 + 50 > mouse[1] > 750:
            text = font.render('Exit', True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightestPurple, (900, 750, 100, 50))
            self.screen.blit(text, (930, 765))
            send = font.render('Next', True, (0, 0, 0))
            pygame.draw.rect(self.screen, purple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
        elif 650 + 250 > mouse[0] > 650 and 750 + 50 > mouse[1] > 750:
            text = font.render('Exit', True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (900, 750, 100, 50))
            self.screen.blit(text, (930, 765))
            send = font.render('Next', True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
        else:
            text = font.render('Exit', True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (900, 750, 100, 50))
            self.screen.blit(text, (930, 765))
            send = font.render('Next', True, (0, 0, 0))
            pygame.draw.rect(self.screen, purple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
        pygame.display.update()
        # detect clicks
        click = pygame.mouse.get_pressed()
        if 900 + 100 > mouse[0] > 900 and 750 + 50 > mouse[1] > 750 and click[0] == 1:
            self.stop()
        elif 650 + 250 > mouse[0] > 650 and 750 + 50 > mouse[1] > 750 and click[0] == 1:
            self.nextQR()

    def nextQR(self):

        # "HJS.12.13.14.15.16.1.18.19.10.0.1.2"

        s = self.randomUser()
        s += f'.{str(random.randint(0,100))}'
        s += f'.{str(random.randint(0,100))}'
        s += f'.{str(random.randint(0,100))}'
        s += f'.{str(random.randint(0,100))}'
        s += f'.{str(random.randint(0,100))}'
        s += f'.{str(random.randint(0,1))}'
        s += f'.{str(random.randint(0,100))}'
        s += f'.{str(random.randint(0,100))}'
        s += f'.{str(random.randint(0,100))}'
        s += f'.{str(random.randint(0,1))}'
        s += f'.{str(random.randint(0,1))}'
        s += f'.{str(random.randint(0,1))}'

        # Generate QR code
        self.qrstring = s
        qrcode = pyqrcode.create(self.qrstring)

        # Create and save the png file naming "myqr.png"
        png = 'myqr.png'
        qrcode.png(png, scale = 6)

        self.qr = png

        return

    def randomUser(self):
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(3))


if __name__ == "__main__":

    qrt = qrTest()
    qrt.run()
