import tempfile
import requests
import zipfile
import io
import os


def get_transcriptions(gene_id):
    url = f"https://api.ncbi.nlm.nih.gov/datasets/v1alpha/gene/id/{gene_id}/" \
          f"download?include_annotation_type=FASTA_RNA,FASTA_PROTEIN"
    return requests.get(url)


def get_rna_from_transcriptions(gene_id) -> str:
    transcriptions_content = get_transcriptions(gene_id).content

    file = zipfile.ZipFile(io.BytesIO(transcriptions_content))
    return file.read('ncbi_dataset/data/rna.fna')


def save_temp_rna_file(rna_contents: str):
    temp_file, filename = tempfile.mkstemp()
    os.write(temp_file, rna_contents)
    return temp_file, filename
