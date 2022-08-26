from Bio.Align.Applications import MuscleCommandline
from Bio.Align.AlignInfo import SummaryInfo
from Bio import AlignIO

import platform
import tempfile
import requests
import zipfile
import struct
import io
import os


def download_muscle():
    bits = struct.calcsize('P') * 8
    system = platform.system()

    if not os.path.isdir('muscle'):
        os.mkdir('muscle')

    if os.path.isfile(f"./muscle/muscle-{system.lower()}-x{bits}.exe"):
        return

    url = 'https://drive5.com/muscle/downloads3.8.31/'
    match system:
        case 'Windows':
            url += 'muscle3.8.31_i86win32.exe'
        case 'Linux':
            url += f"muscle3.8.31_i86linux{bits}.tar.gz"
        case 'Darwin':
            url = f"muscle3.8.31_i86darwin{bits}.tar.gz"

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


# RNA Acquisition:
def get_transcriptions(gene_id):
    url = f"https://api.ncbi.nlm.nih.gov/datasets/v1alpha/gene/id/{gene_id}/" \
          f"download?include_annotation_type=FASTA_RNA,FASTA_PROTEIN"
    return requests.get(url)


def get_rna_from_transcriptions(gene_id) -> bytes:
    transcriptions_content = get_transcriptions(gene_id).content

    file = zipfile.ZipFile(io.BytesIO(transcriptions_content))
    return file.read('ncbi_dataset/data/rna.fna')


def save_temp_rna_file(rna_contents: bytes):
    temp_file, filename = tempfile.mkstemp()
    os.write(temp_file, rna_contents)
    return temp_file, filename
