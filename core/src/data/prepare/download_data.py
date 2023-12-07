import hashlib
import os
from utils.env_utils import read_env_var
from data.scrapers.pinterest_scraper import download_images_from_board


def filter_unique_images(dir: str, logging_enabled: bool = False) -> None:
    unique_hashes = {}
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        img_hash = hashlib.sha1(open(path, 'rb').read()).digest()
        if img_hash not in unique_hashes:
            unique_hashes[img_hash] = filename
        else:
            os.remove(path)
            if logging_enabled:
                print(
                    f'Removed duplicate image: {filename} was a copy of {unique_hashes[img_hash]}')


def print_downloaded_data_size(data_dir: str):
    total = 0
    styles = os.listdir(data_dir)
    for style in styles:
        style_dir = os.path.join(data_dir, style)
        style_size = len(os.listdir(style_dir))
        total += style_size
        print(f'{style}: {style_size} images')
    print(f'\nTotal: {len(styles)} styles, {total} images')


_styles_boards = {
    'formal': {
        'women-800': 'https://www.pinterest.com/couturebenz/elegant-and-formal-outfits/',
        'women-50': 'https://in.pinterest.com/m_asmakhan/formal-outfits-for-women/',
        'women-120': 'https://www.pinterest.com/oelshayal/formal-outfits/',
        'men-100': 'https://www.pinterest.com/elvis890714/formal-style/',
        'men-200': 'https://www.pinterest.com/bowselectie/mens-formal-wear/',
        'men-90': 'https://in.pinterest.com/nchandu1407/formal-dresses-for-men/'
    },
    'classic': {
        'women-340': 'https://www.pinterest.com/vettacapsule/classic-style-inspiration/',
        'women-170-formal-ish': 'https://www.pinterest.com/melovemaj94/office-wear-mood-board/',
        'men-140-formal-ish': 'https://nl.pinterest.com/Eclectique00/men-classic-style/',
        'men-260-formal-ish': 'https://www.pinterest.com/lilsidpoitier/classic-mens-fashion/'
    },
    'casual': {
        'women-100': 'https://www.pinterest.com/maisondecinq/fashion-casual-looks/',
        'women-1010': 'https://www.pinterest.com/justatinabit/casual-outfits/',
        'men-250': 'https://www.pinterest.com/famousoutfits/mens-casual-outfits/',
        'men-130': 'https://www.pinterest.com/cladwellapp/mens-capsule-casual/'
    },
    'streetwear': {
        'women-300': 'https://www.pinterest.com/mintyninja/streetwear-girls/',
        'women-50': 'https://www.pinterest.com/tylervanloon/womens-streetwear/',
        'men-860': 'https://www.pinterest.com/Shaquilleovoxo/mens-fashion-urban-street-style/',
        'men-45': 'https://www.pinterest.com/mdtanzil/hip-hop/',
        'men-7': 'https://www.pinterest.com/www584053932/hiphop-style/'
    },
    'sport': {
        'women-480': 'https://www.pinterest.de/diesemary18/sport-outfit-women/',
        'men-670': 'https://www.pinterest.com/JochePapo/mens-outfits-sport/',
        'men-180': 'https://www.pinterest.com/edbryant9605/mens-sport-style/'
    },
    'bohemian': {
        'women-190': 'https://www.pinterest.com/vettacapsule/bohemian-style-inspiration/',
        'women-460': 'https://www.pinterest.com/SarahGreenmanCreative/bohemian-fashion/',
        'men-40': 'https://www.pinterest.com/lavha/mens-fashion-bohemian/',
        'men-50': 'https://www.pinterest.com/forestfrantz/bohemian-style-men/',
        'men-100': 'https://www.pinterest.com/sweetd1180/bohemian-men/'
    },
    'glamorous': {
        'women-380': 'https://www.pinterest.com/SuperBlonde4Eva/glamour-dresses/',
        'women-790': 'https://www.pinterest.com/dallasshaw/r-u-n-w-a-y/',
        'men-270': 'https://www.pinterest.com.au/styleglamour/glam-looks-for-guys/',
        'men-330': 'https://www.pinterest.com/OpulentLifestyle2/mens-fashion-runway/'
    },
    'minimalist': {
        'women-600': 'https://www.pinterest.com/alexandraevjen/minimalist/',
        'women-210': 'https://www.pinterest.com/vettacapsule/minimal-style-inspiration/',
        'men-180': 'https://id.pinterest.com/laurensiusadi_/mens-minimalist-style/',
        'men-30': 'https://www.pinterest.com/shaneryan1023/minimalist-male/'
    },
    'vintage': {
        'women-290': 'https://www.pinterest.com/goodchloe/vintage-outfits/',
        'women-890': 'https://www.pinterest.com/joslinpett/vintage-fall/',
        'men-40': 'https://www.pinterest.com/reallyrell83/mens-vintage-style/',
        'men-120': 'https://www.pinterest.com/bowlingconcepts/retro-mens-fashion/',
        'men-60': 'https://www.pinterest.com/TrendyButler/vintage-inspired-fall-fashion/'
    },
    'rock-n-roll': {
        'women-340': 'https://www.pinterest.com/theraggshop/rock-n-roll/',
        'women-450': 'https://www.pinterest.com/soumisou/rock-and-roll-fashion/',
        'women-190': 'https://www.pinterest.com/blondedaydreams/rock-n-roll/',
        'men-50': 'https://www.pinterest.com/amonttag24/rock-n-roll-fashion-mens/',
        'men-310': 'https://www.pinterest.co.uk/peteearl/mens-rock-fashion/'
    },
    'western': {
        'women-440': 'https://www.pinterest.com/tealfeathers1/womens-western-wear/',
        'women-180': 'https://www.pinterest.com/beagarcia621/western-outfits/',
        'women-100': 'https://www.pinterest.com/elucerom/cowboy-look/',
        'men-490': 'https://www.pinterest.com/seanhardman040/mens-western-wear/',
        'men-30': 'https://www.pinterest.com/superman1893/mens-western-wear/'
    },
    'preppy/ivy-league': {
        'women-180': 'https://www.pinterest.de/kigalein/preppy-style/',
        'women-310': 'https://www.pinterest.com/ashleyday17/ivy-league-style/',
        'men-210': 'https://www.pinterest.com/jbrentsr/ivy-league-style/',
        'men-290': 'https://www.pinterest.com/vehnasa/preppy-mens-fashion/'
    },
    'flapper': {
        'women-770': 'https://www.pinterest.com/lloyd3615/flapper-dress/',
        'women-350': 'https://www.pinterest.com/jensosa/1920s-style/'
    },
    'old-hollywood': {
        'women-220': 'https://pinterest.com/claudia92040/classic-hollywood-fashion/',
        'women-30': 'https://www.pinterest.com/ClassicCriticsCorner/old-hollywood-fashion/',
        'women-40': 'https://www.pinterest.com/pearlsonly/old-hollywood-glamour/',
        'men-50': 'https://www.pinterest.com/jimresonable/1950s-mens-style/',
        'men-22': 'https://www.pinterest.com/cgiselem/1950s-men-fashion/',
        'men-180': 'https://www.pinterest.com/stephrubio51/1950s-mens-fashion/'
    },
    '70s': {
        'women-1010': 'https://www.pinterest.com/jasonchapin/70s-outfits/',
        'women-80': 'https://www.pinterest.com/vickievedder/disco-outfits/',
        'women-10': 'https://www.pinterest.com/PleaseSayTheM/70s-disco-looks/',
        'men-110': 'https://www.pinterest.com/mary9539/70s-fashion-for-men/',
        'men-80': 'https://www.pinterest.com/conner1140/70s-mens-fashion/',
        'men-270': 'https://www.pinterest.com/lindawhitcomb37/1960s-70s-mens-fashion/'
    },
    'neon': {
        'women-280': 'https://www.pinterest.com/manaems/neon-fashion/',
        'women-80': 'https://www.pinterest.com/theblkcloud/neon/',
        'women-180': 'https://www.pinterest.com/MissMaryYounker/neon-pop/',
        'men-10': 'https://gr.pinterest.com/harmon4082/neon-outfits/'
    },
    '80s/new-wave': {
        'women-240': 'https://www.pinterest.de/natibominable/fashion-in-the-80s/',
        'women-210': 'https://www.pinterest.com/mayakule/80s-fashion-casual/',
        'women-20': 'https://www.pinterest.com/msyraatzenberg/new-wave-fashion-inspo/',
        'women-300-mix': 'https://www.pinterest.com/melagogo/80s-fashion/',
        'men-70': 'https://www.pinterest.com/conner1140/80s-mens-fashion/'
    },
    'techwear': {
        'all-250': 'https://www.pinterest.com/thebibliofile/techwear/',
        'women-40': 'https://www.pinterest.com/techstreetx/techwear-girls/',
        'men-340': 'https://www.pinterest.com/frostola/future-techwear/',
        'men-20': 'https://www.pinterest.com/alanezi1387/techwear-men/'
    },
    'grunge/punk-rock': {
        'women-1050': 'https://www.pinterest.com/santiagoduran/punk-rock-fashion/',
        'men-100': 'https://www.pinterest.com/tgo_eden/mens-grunge-fashion/',
        'men-20': 'https://www.pinterest.com/sing247/grunge-fashion-mens/',
        'men-170-punks': 'https://www.pinterest.com/jjeanne333/punk-guys/'
    },
    'gothic': {
        'women-500': 'https://www.pinterest.com/welcominggrave/gothic-outfits/',
        'women-490': 'https://www.pinterest.com/gothauctions/gothic-fashion/',
        'women-80': 'https://www.pinterest.co.uk/cgibson1057/gothic-fashion-women/',
        'men-190': 'https://www.pinterest.com/deityatlanta/goth-men/'
    }
}

if __name__ == '__main__':
    root_data = read_env_var('DATA_DIR')
    data_dir = os.path.join(root_data, 'img_fashion_styles')

    for style, boards in _styles_boards.items():
        style_dir = os.path.join(data_dir, style)
        print(f"Started downloading images for style {style}", end='\n\n')
        for board_name, board_url in boards.items():
            download_images_from_board(
                board_url,
                output_dir=style_dir,
                board_name=board_name,
                num_of_workers=10,
                logging_enabled=True
            )
            print()
            print(
                f"Successfully downloaded board [{board_name}] {board_url}", end='\n--------\n')
        filter_unique_images(style_dir, logging_enabled=True)
