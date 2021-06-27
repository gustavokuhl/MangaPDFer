from genericpath import exists
import os
import re
import argparse
from PIL import Image, ImageFile
from pathlib import Path


def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]


ImageFile.LOAD_TRUNCATED_IMAGES = True

parser = argparse.ArgumentParser(description="Converte todo um Path para PDF")
parser.add_argument('-p', '--path')
args = parser.parse_args()

path = Path(args.path) if args.path else Path('/home/noname/Documents/Mangas/Berserk')
for root, diretorios, imagens in os.walk(path):
    if len(imagens) == 0:
        diretorios.sort(key=natural_keys)
        if not os.path.exists(path / 'pdfs'):
            os.mkdir(path / 'pdfs')
    elif 'pdfs' in root:
        continue
    else:
        #pdf_filename = 'cap_' + os.path.basename(root).split('#')[1].replace('.', '-') + '.pdf'
        pdf_filename = os.path.basename(root) + '.pdf'
        save_path = Path(path / 'pdfs' / pdf_filename)
        if os.path.exists(save_path): # Evita de baixar novamente algo
            continue

        imagens.sort()
        PIL_imagens = []
        for imagem in imagens:
            PIL_imagem = Image.open(root + '/' + imagem)
            PIL_imagem.convert("RGB")

            fill_color = 'black'  # your background
            if PIL_imagem.mode in ('RGBA', 'LA'):
                background = Image.new(PIL_imagem.mode[:-1], PIL_imagem.size, fill_color)
                background.paste(PIL_imagem, PIL_imagem.split()[-1])
                PIL_imagem = background

            PIL_imagens.append(PIL_imagem)
        try:
            PIL_imagens[0].save(save_path,
                                save_all=True,
                                append_images=PIL_imagens)
        except:
            os.remove(save_path) # Remove arquivo corrompido
            raise
        
