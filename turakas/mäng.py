import pygame
import random
import operator
from .nupud import Nupud
from .constants import WIDTH, HEIGHT, BG, KÄSI, TAGUS, KÕRGUS, LAIUS, POSX, POSY, KOHAD, TAPMISKOHAD, KOHAD1, KOHAD2
from .pakk import PAKK, MASTID
from .kaardipilt import Kaart



KAARDID1 = []
KAARDID2 = []
KÄIMAS = []
TAPMAS = []
VÄLI = []
VÄLIVÄÄRTUS = []
TRUMP = []
VALID =[]

lõpp = Nupud(1170, 850 - KÕRGUS, 0.6)
võta = Nupud(1170, 850-KÕRGUS/2, 0.6)


class Mäng():

    def __init__(self):
        self.mängija1_alles = KÄSI
        self.mängija2_alles = KÄSI
        
    def draw_bg(self, win):
        laius = BG.get_width()  
        kõrgus = BG.get_height()
        for x in range(WIDTH//laius +1):
            for y in range(HEIGHT//kõrgus +1):
                win.blit(BG, (x*500,y*500))
        
    def loo_käed(self):
        random.shuffle(PAKK)
        for i in range(KÄSI*2):
            kaart = PAKK[0]
            PAKK.remove(kaart)
            if i % 2 == 0:
                KAARDID1.append(Kaart(kaart.mast, kaart.väärtus, None))
            else:
                KAARDID2.append(Kaart(kaart.mast, kaart.väärtus, None))

        temp_trump = PAKK[0]
        PAKK.remove(temp_trump)
        PAKK.append(temp_trump)
        self.trump = Kaart(temp_trump.mast, temp_trump.väärtus, None)
        TRUMP.append(self.trump)
        MASTID.insert(0, MASTID.pop(MASTID.index(self.trump.kaart.mast)))

    def uus_kaart(self, mängija):
        if mängija == 1:
            while len(KAARDID1) < KÄSI and len(PAKK) != 0:
                kaart = PAKK.pop(0)
                KAARDID1.append(Kaart(kaart.mast, kaart.väärtus, None))
        else:
            while len(KAARDID2) < KÄSI and len(PAKK) != 0:
                kaart = PAKK.pop(0)
                KAARDID2.append(Kaart(kaart.mast, kaart.väärtus, None))
            
    def draw(self, win):
        self.draw_bg(win)
        KAARDID1.sort(key=operator.attrgetter("kaart.tugevus"), reverse=True)
        KAARDID2.sort(key=operator.attrgetter("kaart.tugevus"), reverse=True)
        KAARDID1.sort(key=lambda mast: MASTID.index(mast.kaart.mast))
        KAARDID2.sort(key=lambda mast: MASTID.index(mast.kaart.mast))

        lõpp.draw(win)
        võta.draw(win)


        self.kaartide_kohad()
        for i, kaard in enumerate(KAARDID1):
            kaard.pos = KOHAD1[0][i]
            win.blit(TAGUS, kaard.pos)

        for i, kaard in enumerate(KAARDID2):
            kaard.pos = KOHAD2[0][i]
            win.blit(kaard.pilt, kaard.pos)

        self.draw_trump(win, TRUMP[0])
        self.kaartide_arv(win)
        if KÄIMAS:
            for i, kaart in enumerate(KÄIMAS):
                win.blit(kaart.pilt, KOHAD[i])
        
        if TAPMAS:
            for i, kaart in enumerate(TAPMAS):
                win.blit(kaart.pilt, TAPMISKOHAD[i])
        
        for nonii in VALID:
            if not nonii.kaart:
                pygame.draw.rect(win, (0, 0, 0), pygame.Rect((nonii.pos[0]-2, nonii.pos[1]-2), (LAIUS+6, KÕRGUS+12)),  4, 3)

            elif nonii.kaart.mast in ["Ärtu", "Ruutu"]:
                pygame.draw.rect(win, (0, 0, 0), pygame.Rect((KOHAD[KÄIMAS.index(nonii)][0]-2, KOHAD[KÄIMAS.index(nonii)][1]-2), (LAIUS+6, KÕRGUS+12)),  4, 3)
            else:
                pygame.draw.rect(win, (255, 0, 0), pygame.Rect((KOHAD[KÄIMAS.index(nonii)][0]-2, KOHAD[KÄIMAS.index(nonii)][1]-2), (LAIUS+6, KÕRGUS+12)),  4, 3)

    def kaardid_maha(self, käik):
        TAPMAS.clear()
        KÄIMAS.clear()
        VÄLI.clear()
        VÄLIVÄÄRTUS.clear()
        if käik == 2:
            self.uus_kaart(2)
            self.uus_kaart(1)
        else:
            self.uus_kaart(1)
            self.uus_kaart(2)
    
    def kaartide_kohad(self):
        if len(KAARDID1) > 10 and len(KAARDID1) < 19:
            KOHAD1.clear()
            KOHAD1.append([(100 + i*(80-(len(KAARDID1)-10)*5), 50) for i in range(30)])
        if len(KAARDID2) > 10 and len(KAARDID2) < 19:
            KOHAD2.clear()
            KOHAD2.append([(100 + i*(80-(len(KAARDID2)-10)*5), 850-KÕRGUS) for i in range(30)])

    def saab_tappa(self, kaart1, kaart2):
        trumbimast = TRUMP[0].kaart.mast
        tapjamast = kaart1.kaart.mast
        maasmast = kaart2.kaart.mast

        if maasmast == trumbimast:
            if (tapjamast == maasmast and kaart1.kaart.tugevus > kaart2.kaart.tugevus): 
                return True
        else: 
            if (tapjamast == maasmast and kaart1.kaart.tugevus > kaart2.kaart.tugevus) or tapjamast == trumbimast:
                return True
        return False

    def get_validmoves(self, kaart):
        for kard in KÄIMAS:
            if self.saab_tappa(kaart, kard) and kard.tappa:
                VALID.append(kard)
        
    def kaartide_arv(self, win):
        if len(PAKK) > 0:
            roboto = pygame.font.Font("Roboto/Roboto-Light.ttf", 30)
            arv = roboto.render(str(len(PAKK)), False, (0,0,0))
            win.blit(arv, (95, 450-KÕRGUS/2-30))

    def draw_trump(self, win, trump):
        trumbipilt = pygame.transform.rotozoom(trump.pilt, -90, 1)
        if len(PAKK) > 0:
            win.blit(trumbipilt, (50, 450-(LAIUS/2)))
        if len(PAKK) > 1:
            win.blit(TAGUS, (50, 450-(KÕRGUS/2)))
        if not PAKK:
            trump_temp = pygame.image.load(f"img/{trump.kaart.mast}.png")
            trump = pygame.transform.scale(trump_temp, (LAIUS*0.674, LAIUS*0.674))
            win.blit(trump, (100, 450-0.337*LAIUS))