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
    
    print(f'  Scaler type: {font.offset_table['scaler_type']}')
    print(f'    numTables: {font.offset_table['numTables']}')
    print(f'  searchRange: {font.offset_table['searchRange']}')
    print(f'entrySelector: {font.offset_table['entrySelector']}')
    print(f'   rangeShift: {font.offset_table['rangeShift']}')



if __name__ == '__main__':
    main()