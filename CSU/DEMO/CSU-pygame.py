import time, sys, os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

pygame.init()


def stop():
    startupScreen(screen)
    time.sleep(2)
    pygame.quit()
    sys.exit()


def startupScreen(display):
    # blits the text to the screen an top of the background
    background(display)
    fontName = pygame.font.get_default_font()
    font = pygame.font.Font(fontName, 32)
    text = font.render("CSU Interface", True, (0, 0, 0))
    display.blit(text, (150, 200))
    pygame.display.update()


def background(display):
    # sets the background to the triangle thing
    lightPurple = (104, 20, 168)
    darkPurple = (71, 10, 145)
    darkestPurple = (45, 6, 112)
    display.fill((125, 125, 125))
    pygame.draw.polygon(display, lightPurple, ((0, 0), (650, 0), (0, 450)))
    pygame.draw.polygon(display, darkPurple, ((0, 0), (425, 0), (0, 225)))
    pygame.draw.polygon(display, darkestPurple, ((0, 0), (212, 0), (0, 100)))
    pygame.display.update()


def descriptions(display, message):
    fontName = pygame.font.get_default_font()
    font = pygame.font.Font(fontName, 25)
    smallFont = pygame.font.Font(fontName, 20)
    if message == 1:
        text = font.render("Enter the data code in the box below.", True, (0, 0, 0))  # TODO:add QR support
        smallText = smallFont.render("Or, scan the QR code.", True, (0, 0, 0))
    elif message == 2:
        text = font.render("Your code has been accepted!", True, (0, 0, 0))
        smallText = smallFont.render("", True, (0, 0, 0))
    elif message == 3:
        text = font.render("Your code has been rejected!", True, (0, 0, 0))
        smallText = smallFont.render("", True, (0, 0, 0))
    display.blit(text, (150, 200))
    display.blit(smallText, (150, 250))
    pygame.display.update()


COLOR_ACTIVE = (0, 0, 0)
COLOR_INACTIVE = (66, 66, 66)
FONT = pygame.font.Font(None, 25)


class InputBox:  # Created by stackoverflow user skrx, get_text() added by me

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        global output

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect. self.rect.collidepoint(event.pos)
            if self.rect.x+self.rect.w > event.pos[0] > self.rect.x and self.rect.y+self.rect.h > event.pos[1] > self.rect.y:
                # Toggle the active variable.
                self.active = True
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
        width = max(900, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, int(self.rect.y + (self.rect.h / 3))))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text


def decrypt(display, data):
    data = data.split(".")
    if len(data) == 1:
        background(display)
        descriptions(display, 3)
        pygame.display.update()
        time.sleep(5)
        background(display)
        descriptions(display, 1)


def buttons(display):  # displays and manages buttons
    lightestPurple = (122, 48, 191)
    lightPurple = (71, 6, 150)
    purple = (56, 5, 110)
    fontName = pygame.font.get_default_font()
    font = pygame.font.Font(fontName, 20)
    # checks if mouse is on button
    mouse = pygame.mouse.get_pos()
    if 900+100 > mouse[0] > 900 and 750+50 > mouse[1] > 750:
        exit = font.render("Exit", True, (0, 0, 0))
        pygame.draw.rect(display, lightestPurple, (900, 750, 100, 50))
        display.blit(exit, (930, 765))
        send = font.render("Send to Spreadsheet", True, (0, 0, 0))
        pygame.draw.rect(display, purple, (650, 750, 250, 50))
        display.blit(send, (670, 765))
    elif 650+250 > mouse[0] > 650 and 750+50 > mouse[1] > 750:
        exit = font.render("Exit", True, (0, 0, 0))
        pygame.draw.rect(display, lightPurple, (900, 750, 100, 50))
        display.blit(exit, (930, 765))
        send = font.render("Send to Spreadsheet", True, (0, 0, 0))
        pygame.draw.rect(display, lightPurple, (650, 750, 250, 50))
        display.blit(send, (670, 765))
    else:
        exit = font.render("Exit", True, (0, 0, 0))
        pygame.draw.rect(display, lightPurple, (900, 750, 100, 50))
        display.blit(exit, (930, 765))
        send = font.render("Send to Spreadsheet", True, (0, 0, 0))
        pygame.draw.rect(display, purple, (650, 750, 250, 50))
        display.blit(send, (670, 765))
    pygame.display.update()
    # detect clicks
    click = pygame.mouse.get_pressed()
    if 900+100 > mouse[0] > 900 and 750+50 > mouse[1] > 750:
        if click[0] == 1:
            stop()
    elif 650+250 > mouse[0] > 650 and 750+50 > mouse[1] > 750:
        if click[0] == 1:
            print("Sending to sheet!") # TODO: Add sending to spreadsheet



if __name__ == "__main__":
    # Creates screen
    DISPLAY_WIDTH = 1000
    DISPLAY_HEIGHT = 800
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('CSU Interface')
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    textinput = InputBox(x=50, y=400, w=900, h=50)
    # runs startup protocol
    running = True
    showingBox = True
    currentMessage = 1
    startupScreen(screen)
    time.sleep(2)
    background(screen)
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                stop()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                output = textinput.get_text()
                decrypt(screen, output)
            textinput.handle_event(event)

            background(screen)
            descriptions(screen, currentMessage)
            buttons(screen)
            if currentMessage == 1:
                textinput.draw(screen)
            textinput.update()
            pygame.display.update()
        clock.tick(15) # TODO:Find out how to stop flickering
