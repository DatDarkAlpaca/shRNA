from dataclasses import dataclass, field


@dataclass
class SiDirectResult:
    si_rna: field(default_factory=list)
    target_sequences: field(default_factory=list)
    tm_guides: field(default_factory=list)
