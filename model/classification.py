from dataclasses import dataclass

@dataclass
class Classification:
    GeneID: str
    Localization: str
    Chromosome: int

    def __str__(self):
        return f"{self.GeneID}"

    def __lt__(self, other):
        return self.GeneID < other.GeneID

    def __hash__(self):
        return hash(self.GeneID)

    def __repr__(self):
        return str(self)
