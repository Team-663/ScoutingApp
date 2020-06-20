import os
import sys
import time
import json
import xlsxwriter
import datetime
import pygame

DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 800

pygame.init()
fontName = pygame.font.get_default_font()
font = pygame.font.Font(fontName, 25)

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class csu:
    def __init__(self):
        # get path to file
        self.path = str(os.path.dirname(__file__))
        self.userPath = os.path.expanduser("~")
        self.dataFile = os.path.join(self.path, "data.json")
        self.documents = os.path.join(self.userPath, "Documents")
        self.scoutData = None

        # all the pygame stuff happens here
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('CSU Interface')
        self.logo = pygame.image.load(os.path.join(self.path, "logo.png"))
        pygame.display.set_icon(self.logo)

        self.localTime = datetime.datetime.now()

        try:
            with open(self.dataFile, "r") as j:
                try:
                    self.scoutData = json.loads(j.read())
                    j.close()
                except json.decoder.JSONDecodeError:
                    self.scoutData = []
                # print(self.scoutData)
        except FileNotFoundError:
            self.scoutData = []

    def stop(self):
        self.startupScreen()
        with open(self.dataFile, "w") as outfile:
            json.dump(self.scoutData, outfile)
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def startupScreen(self):
        # blits the text to the screen on top of the background
        self.background()
        fontName = pygame.font.get_default_font()
        font = pygame.font.Font(fontName, 32)
        text = font.render("CSU Interface", True, (0, 0, 0))
        self.screen.blit(text, (150, 200))
        pygame.display.update()

    def background(self):
        # sets the background to the triangle thing
        lightPurple = (104, 20, 168)
        darkPurple = (71, 10, 145)
        darkestPurple = (45, 6, 112)
        self.screen.fill((125, 125, 125))
        pygame.draw.polygon(self.screen, lightPurple, ((0, 0), (650, 0), (0, 450)))
        pygame.draw.polygon(self.screen, darkPurple, ((0, 0), (425, 0), (0, 225)))
        pygame.draw.polygon(self.screen, darkestPurple, ((0, 0), (212, 0), (0, 100)))
        image = pygame.image.load(os.path.join(self.path, "logo.png"))
        self.screen.blit(image, (-10, 617))
        pygame.display.update()

    def descriptions(self, message):
        smallFont = pygame.font.Font(fontName, 20)
        if message == 1:
            text = font.render("Enter the data code in the box below.", True, (0, 0, 0))
            smallText = smallFont.render("Or, scan the QR code.", True, (0, 0, 0))
        elif message == 2:
            text = font.render("Your code has been accepted!", True, (0, 0, 0))
            smallText = smallFont.render("", True, (0, 0, 0))
        elif message == 3:
            text = font.render("Your code has been rejected!", True, (0, 0, 0))
            smallText = smallFont.render("It was too short.", True, (0, 0, 0))
        elif message == 4:
            text = font.render("Your code has been rejected!", True, (0, 0, 0))
            smallText = smallFont.render("It was too long.", True, (0, 0, 0))
        self.screen.blit(text, (150, 200))
        self.screen.blit(smallText, (150, 250))
        pygame.display.update()

    def parseInput(self, data):
        self.localTime = datetime.datetime.now()
        splitData = data.split(".")
        splitData.insert(0, self.localTime.strftime("%Y-%m-%d %H:%M:%S"))
        if len(splitData) < 14:
            self.background()
            self.descriptions(3)
            pygame.display.update()
            time.sleep(3)
            self.background()
            self.descriptions(1)
        elif len(splitData) == 14:
            self.background()
            self.descriptions(2)
            pygame.display.update()
            time.sleep(3)
            self.background()
            self.descriptions(1)
            self.scoutData.append(splitData)
            # print(self.scoutData)
        elif len(splitData) > 14:
            self.background()
            self.descriptions(4)
            pygame.display.update()
            time.sleep(3)
            self.background()
            self.descriptions(1)

    def buttons(self):  # displays and manages buttons
        lavender = (152, 100, 204)
        lightestPurple = (122, 48, 191)
        lightPurple = (71, 6, 150)
        purple = (56, 5, 110)
        fontName = pygame.font.get_default_font()
        font = pygame.font.Font(fontName, 20)
        # checks if mouse is on button
        mouse = pygame.mouse.get_pos()
        if 900 + 100 > mouse[0] > 900 and 750 + 50 > mouse[1] > 750:
            text = font.render("Exit", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lavender, (900, 750, 100, 50))
            self.screen.blit(text, (930, 765))
            send = font.render("Send to Spreadsheet", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
            newFile = font.render("New Datafile", True, (0, 0, 0))
            pygame.draw.rect(self.screen, purple, (500, 750, 150, 50))
            self.screen.blit(newFile, (515, 765))
        elif 650 + 250 > mouse[0] > 650 and 750 + 50 > mouse[1] > 750:
            text = font.render("Exit", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightestPurple, (900, 750, 100, 50))
            self.screen.blit(text, (930, 765))
            send = font.render("Send to Spreadsheet", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightestPurple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
            newFile = font.render("New Datafile", True, (0, 0, 0))
            pygame.draw.rect(self.screen, purple, (500, 750, 150, 50))
            self.screen.blit(newFile, (515, 765))
        elif 500 + 150 > mouse[0] > 500 and 750 + 50 > mouse[1] > 750:
            text = font.render("Exit", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightestPurple, (900, 750, 100, 50))
            self.screen.blit(text, (930, 765))
            send = font.render("Send to Spreadsheet", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
            newFile = font.render("New Datafile", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (500, 750, 150, 50))
            self.screen.blit(newFile, (515, 765))
        else:
            text = font.render("Exit", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightestPurple, (900, 750, 100, 50))
            self.screen.blit(text, (930, 765))
            send = font.render("Send to Spreadsheet", True, (0, 0, 0))
            pygame.draw.rect(self.screen, lightPurple, (650, 750, 250, 50))
            self.screen.blit(send, (670, 765))
            newFile = font.render("New Datafile", True, (0, 0, 0))
            pygame.draw.rect(self.screen, purple, (500, 750, 150, 50))
            self.screen.blit(newFile, (515, 765))
        pygame.display.update()
        # detect clicks
        click = pygame.mouse.get_pressed()
        if 900 + 100 > mouse[0] > 900 and 750 + 50 > mouse[1] > 750 and click[0] == 1:
            self.stop()
        elif 650 + 250 > mouse[0] > 650 and 750 + 50 > mouse[1] > 750 and click[0] == 1:
            self.sendToSheet()
        elif 500 + 150 > mouse[0] > 500 and 750 + 50 > mouse[1] > 750 and click[0] == 1:
            self.newDatafile()

    def sendToSheet(self):
        self.localTime = datetime.datetime.now()
        filename = f'Scouting Data {self.localTime.strftime("%Y-%m-%d")}.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(self.documents, filename))
        worksheet = workbook.add_worksheet("Form Responses")
        header_format = workbook.add_format({"bold": True})
        header_format.set_text_wrap()
        header = ("Timestamp", "Name", "Match", "Team", "Autonomous Power Cell Scoring [Bottom Port Goals]",
                  "Autonomous Power Cell Scoring [Outer Port Goals]",
                  "Autonomous Power Cell Scoring [Inner Port Goals]", "Crossed Autoline?", "Teleop Bottom Port Goals",
                  "Teleop Outer Port Goals", "Teleop Inner Port Goals",
                  "Control Panel [Rotation Control]", "Control Panel [Position Control]", "Climbing/Parking")
        worksheet.write_row(0, 0, header, cell_format=header_format)
        worksheet.freeze_panes(1, 0)

        for col in range(len(header)):
            worksheet.set_column(col, col, width=20)
        worksheet.set_row(0, 40)

        row = 1
        for data in self.scoutData:
            for i in range(len(data)):
                value = data[i]
                if i == 7:
                    if value == "1":
                        value = "Yes"
                    else:
                        value = "No"
                if i == 11 or i == 12:
                    if value == "0":
                        value = "Did Not Attempt"
                    elif value == "1":
                        value = "Failed"
                    else:
                        value = "Succeeded"
                if i == 13:
                    if value == "0":
                        value = "Did Not Attempt"
                    elif value == "1":
                        value = "Parked"
                    elif value == "2":
                        value = "Climbed - Not Level"
                    else:
                        value = "Climbed - Level"
                worksheet.write(row, i, value)
            row += 1

        workbook.close()
        # print("sent")

    def newDatafile(self):
        self.localTime = datetime.datetime.now()
        newFile = "ArchivedData_" + self.localTime.strftime("%Y-%m-%d") + ".json"
        os.chdir(self.path)
        os.rename("data.json", newFile)

    def run(self):
        # Creates screen
        textinput = InputBox(x=50, y=400, w=900, h=50)
        # runs startup protocol
        running = True
        showingBox = True
        currentMessage = 1
        self.startupScreen()
        time.sleep(2)
        self.background()
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.stop()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    csuInput = textinput.get_text()
                    self.parseInput(csuInput)
                textinput.handle_event(event)

                self.background()
                self.descriptions(currentMessage)
                self.buttons()
                if currentMessage == 1:
                    textinput.draw(self.screen)
                textinput.update()
                pygame.display.update()
            self.clock.tick(15)


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
            if self.rect.x + self.rect.w > event.pos[0] > self.rect.x and self.rect.y + self.rect.h > \
                    event.pos[1] > self.rect.y:
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


if __name__ == "__main__":
    mycsu = csu()

    mycsu.run()
