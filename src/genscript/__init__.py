from dataclasses import dataclass, field


@dataclass
class GenscriptResult:
    genbank: field(default_factory=list)
    gene_names: field(default_factory=list)
    amount: int
