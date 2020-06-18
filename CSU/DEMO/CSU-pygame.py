import time, sys, os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

pygame.init()

def stop():
    pygame.quit()
    sys.exit()


def startupScreen(display):
    # blits the text to the screen an top of the background
    background(display)
    fontName = pygame.font.get_default_font()
    font = pygame.font.Font(fontName, 32)
    text = font.render("CSU Interface", True, (0, 0, 0))
    display.blit(text, (50, 100))
    pygame.display.update()


def background(display):
    # sets the background to the triangle thing
    lightPurple = (104, 20, 168)
    darkPurple = (71, 10, 145)
    darkestPurple = (45, 6, 112)
    display.fill((125, 125, 125))
    pygame.draw.polygon(display, lightPurple, ((0, 0), (450, 0), (0, 300)))
    pygame.draw.polygon(display, darkPurple, ((0, 0), (225, 0), (0, 100)))
    pygame.draw.polygon(display, darkestPurple, ((0, 0), (112, 0), (0, 25)))
    pygame.display.update()

def descriptions(display, message):
    fontName = pygame.font.get_default_font()
    font = pygame.font.Font(fontName, 25)
    smallFont = pygame.font.Font(fontName, 20)
    if message == 1:
        text = font.render("Enter the data code in the box below.", True, (0, 0, 0)) # TODO:add QR support
        smallText = smallFont.render("Or, scan the QR code.", True, (0, 0, 0))
    elif message == 2:
        text = font.render("Your code has been accepted!", True, (0, 0, 0))
        smallText = smallFont.render("Type \"yes\" in the box to send another code, and no to exit.", True, (0, 0, 0))
    elif message == 3:
        text = font.render("Your code has been rejected!", True, (0, 0, 0))
        smallText = smallFont.render("Type \"yes\" in the box to send another code, and no to exit.", True, (0, 0, 0))
    display.blit(text, (50, 100))
    display.blit(smallText, (50, 150))
    pygame.display.update()


COLOR_INACTIVE = (0, 0, 0)
COLOR_ACTIVE = (66, 66, 66)
FONT = pygame.font.Font(None, 25)


class InputBox: # Created by stackoverflow user skrx, get_text() added by me

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        global output

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(500, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, int(self.rect.y + (self.rect.h/3))))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text


if __name__ == "__main__":
    # Creates screen
    DISPLAY_WIDTH = 600
    DISPLAY_HEIGHT = 600
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('CSU Interface')
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    textinput = InputBox(x=50, y=300, w=500, h=50)
    # runs startup protocol
    running = True
    showingBox = True
    currentMessage = 1
    startupScreen(screen)
    time.sleep(2)
    background(screen)
    while running:
        background(screen)
        descriptions(screen, currentMessage)
        if currentMessage == 1:
            textinput.draw(screen)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                stop()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                output = textinput.get_text()
                print(output)
                if output.lower() == "stop":
                    startupScreen(screen)
                    time.sleep(2)
                    stop()
            textinput.handle_event(event)
        textinput.update()
        pygame.display.update()
        clock.tick(15)
