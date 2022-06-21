from Bio.Align.Applications import MuscleCommandline
from Bio.Align.AlignInfo import SummaryInfo
from Bio import AlignIO

import platform
import requests
import struct
import os


def download_muscle():
    bits = struct.calcsize('P') * 8
    system = platform.system()

    if os.path.isfile(f"./muscle/muscle-{system.lower()}-x{bits}.exe"):
        return

    url = None
    match system:
        case 'Windows':
            url = 'https://drive5.com/muscle/downloads3.8.31/muscle3.8.31_i86win32.exe'
        case 'Linux':
            url = f"https://drive5.com/muscle/downloads3.8.31/muscle3.8.31_i86linux{bits}.tar.gz"
        case 'Darwin':
            url = f"https://drive5.com/muscle/downloads3.8.31/muscle3.8.31_i86darwin{bits}.tar.gz"

    if url:
        with open(f"./muscle/muscle-{system.lower()}-x{bits}.exe", mode='wb') as file:
            file.write(requests.get(url).content)


def get_muscle_command():
    bits = struct.calcsize('P') * 8
    system = platform.system()

    return os.path.join(os.path.curdir, 'muscle', f"muscle-{system.lower()}-x{bits}.exe")


def align_rna(muscle_command: str, input_file: str, output_file: str):
    MuscleCommandline(muscle_command, input=input_file, out=output_file)()
    return AlignIO.read(output_file, 'fasta')


def get_aligned_consensus(aligned) -> str:
    summary = SummaryInfo(aligned)
    return str(summary.gap_consensus(threshold=1.0, ambiguous='X', require_multiple=0))
