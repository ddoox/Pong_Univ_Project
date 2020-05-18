import pygame
import sys
import time
from pygame.locals import *


# wczytanie argumentów
Plik = open("config")
ConfigArgumenty = []

for line in Plik:
    k = line.split(":")
    n = k[1].split("/")
    ConfigArgumenty.append(int(n[0]))



pygame.init()

OknoSzerokosc = ConfigArgumenty[0]
OknoWysokosc = ConfigArgumenty[1]
Czarny = (0, 0, 0)
Bialy = (255, 255, 255)

# inicjacja okna gry

Okno = pygame.display.set_mode((OknoSzerokosc, OknoWysokosc), 0, 32)
pygame.display.set_caption('Pong')

# paletka gracza/dolna
PaletkaGraczSzerokosc = OknoSzerokosc * 0.1
PaletkaGraczWysokosc = OknoWysokosc * 0.05
PaletkaGraczPozycjaPoczatkowa = (OknoSzerokosc / 2, OknoWysokosc - 2 * PaletkaGraczWysokosc)
PaletkaGracz = pygame.Surface([PaletkaGraczSzerokosc, PaletkaGraczWysokosc])
PaletkaGracz.fill(Bialy)
PaletkaGraczProstokat = PaletkaGracz.get_rect()
PaletkaGraczProstokat.x = PaletkaGraczPozycjaPoczatkowa[0]
PaletkaGraczProstokat.y = PaletkaGraczPozycjaPoczatkowa[1]

# piłka
PilkaSzerokosc = PaletkaGraczWysokosc
PilkaWysokosc = PaletkaGraczWysokosc
PilkaPredkoscX = 11
PilkaPredkoscY = 11
Pilka = pygame.Surface([PilkaSzerokosc, PilkaWysokosc], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(Pilka, Bialy, [0, 0, PilkaSzerokosc, PilkaWysokosc])
PilkaProstokat = Pilka.get_rect()
PilkaProstokat.x = OknoSzerokosc / 2
PilkaProstokat.y = OknoWysokosc / 2

# klatki
FPS = 60
ZegarFPS = pygame.time.Clock()  # zegar

# paletka AI/drugiego gracza górna
PaletkaAiPozycjaPoczatkowa = (OknoSzerokosc / 2, PaletkaGraczWysokosc)
PaletkaAi = pygame.Surface([PaletkaGraczSzerokosc, PaletkaGraczWysokosc])
PaletkaAi.fill(Bialy)
PaletkaAiProstokat = PaletkaAi.get_rect()
PaletkaAiProstokat.x = PaletkaAiPozycjaPoczatkowa[0]
PaletkaAiProstokat.y = PaletkaAiPozycjaPoczatkowa[1]
PaletkaAiPredkosc = ConfigArgumenty[2]

# punkty
PunktyGracz = '0'
PunktyAi = '0'
CzcionkaObiekt = pygame.font.Font('freesansbold.ttf', int(OknoWysokosc / 5))

PauzaStatus = 0

def wyswietl_punkty_gracz():
    TekstGracz = CzcionkaObiekt.render(PunktyGracz, True, (255, 255, 255))
    TekstGraczProstokat = TekstGracz.get_rect()
    TekstGraczProstokat.center = (OknoSzerokosc / 2, OknoWysokosc * 0.75)
    Okno.blit(TekstGracz, TekstGraczProstokat)


def wyswietl_punkty_Ai():
    TekstAi = CzcionkaObiekt.render(PunktyAi, True, (255, 255, 255))
    TekstAiProstokat = TekstAi.get_rect()
    TekstAiProstokat.center = (OknoSzerokosc / 2, OknoWysokosc / 4)
    Okno.blit(TekstAi, TekstAiProstokat)

# przytrzymanie klawisza powoduje ruch
pygame.key.set_repeat(1, 2)

# główna pętla programu
while True:
    # obsługa zdarzeń
    for event in pygame.event.get():
        # zamknięcie okna
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # ruch myszy
        if event.type == MOUSEMOTION:
            MyszX, MyszY = event.pos  # współrzędna x i y kursora

            # oblicz przesunięcie paletki gracza
            PaletkaGraczPrzesuniecie = MyszX - (PaletkaGraczSzerokosc / 2)

            # wykraczanie poza okno gry
            if PaletkaGraczPrzesuniecie > OknoSzerokosc - PaletkaGraczSzerokosc:
                PaletkaGraczPrzesuniecie = OknoSzerokosc - PaletkaGraczSzerokosc
            if PaletkaGraczPrzesuniecie < 0:
                PaletkaGraczPrzesuniecie = 0
            # zaktualizuj położenie paletki w poziomie
            PaletkaGraczProstokat.x = PaletkaGraczPrzesuniecie


        if event.type == pygame.KEYDOWN: # naciśnięcia klawiszy
            if ConfigArgumenty[3] == 0:
               if event.key == pygame.K_LEFT:
                    PaletkaAiProstokat.x -= ConfigArgumenty[4]
                    if PaletkaAiProstokat.x < 0:
                        PaletkaAiProstokat.x = 0
            if ConfigArgumenty[3] == 0:
                if event.key == pygame.K_RIGHT:
                    PaletkaAiProstokat.x += ConfigArgumenty[4]
                    if PaletkaAiProstokat.x > OknoSzerokosc - PaletkaGraczSzerokosc:
                        PaletkaAiProstokat.x = OknoSzerokosc - PaletkaGraczSzerokosc

            # zmiana prędkości piłki
            if event.key == pygame.K_1:
                PilkaPredkoscX = 3
                PilkaPredkoscY = 3
            if event.key == pygame.K_2:
                PilkaPredkoscX = 6
                PilkaPredkoscY = 6
            if event.key == pygame.K_3:
                PilkaPredkoscX = 7
                PilkaPredkoscY = 7
            if event.key == pygame.K_4:
                PilkaPredkoscX = 8
                PilkaPredkoscY = 8
            if event.key == pygame.K_5:
                PilkaPredkoscX = 10
                PilkaPredkoscY = 10
            if event.key == pygame.K_6:
                PilkaPredkoscX = 13
                PilkaPredkoscY = 13
            if event.key == pygame.K_7:
                PilkaPredkoscX = 15
                PilkaPredkoscY = 15
            if event.key == pygame.K_8:
                PilkaPredkoscX = 17
                PilkaPredkoscY = 17
            if event.key == pygame.K_9:
                PilkaPredkoscX = 20
                PilkaPredkoscY = 20

            # reset punktów
            if event.key == pygame.K_r:
                PunktyGracz = '0'
                PunktyAi = '0'
            # wyjście
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            # pauza
            if event.key == pygame.K_p:
                if PauzaStatus:
                    PilkaPredkoscX = BackupX
                    PilkaPredkoscY = BackupY
                    PauzaStatus = 0
                    time.sleep(0.1)
                else:
                    BackupX = PilkaPredkoscX
                    BackupY = PilkaPredkoscY
                    PilkaPredkoscX = 0
                    PilkaPredkoscY = 0
                    PauzaStatus = 1
                    time.sleep(0.1)


    # ruch piłki
    # przesuń piłkę po obsłużeniu zdarzeń
    PilkaProstokat.move_ip(PilkaPredkoscX, PilkaPredkoscY)

    # odbijanie od ścian
    if PilkaProstokat.right >= OknoSzerokosc:
        PilkaPredkoscX *= -1
    if PilkaProstokat.left <= 0:
        PilkaPredkoscX *= -1

    # naliczanie punktów
    if PilkaProstokat.top <= 0:
        PilkaProstokat.x = OknoSzerokosc / 2
        PilkaProstokat.y = OknoWysokosc / 2
        PunktyGracz = str(int(PunktyGracz) + 1)

    if PilkaProstokat.bottom >= OknoWysokosc:
        PilkaProstokat.x = OknoSzerokosc / 2
        PilkaProstokat.y = OknoWysokosc / 2
        PunktyAi = str(int(PunktyAi) + 1)

    if ConfigArgumenty[3]:      # AI on

        if PilkaProstokat.centerx > PaletkaAiProstokat.centerx:
            PaletkaAiProstokat.x += PaletkaAiPredkosc
        elif PilkaProstokat.centerx < PaletkaAiProstokat.centerx:
          PaletkaAiProstokat.x -= PaletkaAiPredkosc

    # zmiana kierunku odbijania na przeciwny dla AI
    if PilkaProstokat.colliderect(PaletkaAiProstokat):
        PilkaPredkoscY *= -1
        PilkaProstokat.top = PaletkaAiProstokat.bottom

    if PilkaProstokat.colliderect(PaletkaGraczProstokat):
        PilkaPredkoscY *= -1
        PilkaProstokat.bottom = PaletkaGraczProstokat.top

    # rysowanie


    Okno.fill(Czarny)

    wyswietl_punkty_gracz()
    wyswietl_punkty_Ai()

    # paletki, piłka
    Okno.blit(PaletkaGracz, PaletkaGraczProstokat)
    Okno.blit(PaletkaAi, PaletkaAiProstokat)
    Okno.blit(Pilka, PilkaProstokat)

    # zaktualizuj okno i wyświetl
    pygame.display.update()

    # zaktualizuj zegar po narysowaniu obiektów
    ZegarFPS.tick(FPS)
