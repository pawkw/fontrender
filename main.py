import pygame
from constants import *
from fontrender.font import PWFont


def main():
    # pygame.init()
    # pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame.display.set_caption('Font Renderer')
    with open('fonts/FreeSans.ttf', 'br') as bytefile:
        bytes = bytefile.read()
    if not bytes:
        print('Unable to load file.')
        exit(1)
    
    font = PWFont(bytes)
    
    print(f'  Scaler type: {font.scaler_type}')
    print(f'    numTables: {font.numTables}')
    print(f'  searchRange: {font.searchRange}')
    print(f'entrySelector: {font.entrySelector}')
    print(f'   rangeShift: {font.rangeShift}')
    print()

    for key, entry in font.directory_entries.items():
        print(f'entry: {key} location: {entry.offset}')


if __name__ == '__main__':
    main()