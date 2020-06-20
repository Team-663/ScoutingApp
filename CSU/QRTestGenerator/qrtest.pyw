# Import QRCode from pyqrcode
import os
import pyqrcode
import pygame
import png
import sys, time
from pyqrcode import QRCode

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


pygame.init()

DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 800

class qrtest:
    def __init__(self):
        self.qrlist = [
            "HJS.12.13.14.15.16.1.18.19.10.0.1.2",
            "EAS.22.23.24.25.26.1.28.29.20.0.1.2",
            "JWS.32.33.34.35.36.1.38.39.30.0.1.2",
            "AMS.42.43.44.45.46.1.48.49.40.0.1.2",
            "HJS.52.53.54.55.56.1.58.59.50.0.1.2",
            "EAS.62.63.64.65.66.1.68.69.60.0.1.2",
            "JWS.72.73.74.75.76.1.78.79.70.0.1.2"
        ]

        self.currentqr = 0
        self.qr = None
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('CSU Interface')

    def run(self):
        running = True
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
        text = font.render("CSU QR Test", True, (0, 0, 0))
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
        pygame.display.update()

    def stop(self):
        self.startupScreen()
        time.sleep(2)
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
            exit = font.render("Exit", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightestPurple, (900, 750, 100, 50))
            self.screen.blit(exit, (930, 765))
            send = font.render("Next", True, (0, 0, 0))
            pygame.draw.rect(self.screen, purple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
        elif 650 + 250 > mouse[0] > 650 and 750 + 50 > mouse[1] > 750:
            exit = font.render("Exit", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (900, 750, 100, 50))
            self.screen.blit(exit, (930, 765))
            send = font.render("Next", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
        else:
            exit = font.render("Exit", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (900, 750, 100, 50))
            self.screen.blit(exit, (930, 765))
            send = font.render("Next", True, (0, 0, 0))
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

        s = self.qrlist[self.currentqr]

        # Generate QR code
        url = pyqrcode.create(s)

        # Create and save the png file naming "myqr.png"
        png = 'myqr.png'
        url.png(png, scale = 6)

        if self.currentqr < len(self.qrlist) - 1:
            self.currentqr += 1
        else:
            self.currentqr = 0

        self.qr = png

        return png

if __name__ == "__main__":

    qrTest = qrtest()
    qrTest.run()
