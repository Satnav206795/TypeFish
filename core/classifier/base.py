from dataclasses import dataclass


@dataclass(frozen=True)
class Eval:
        cp: float
        mateIn: int
    
        @property
        def is_mate(self) -> bool:
            return self.mateIn is not None
       

@dataclass(frozen=True)
class Result:
        label: str
        reason: str
        bestMoveUCI: str
        moveMadeUCI:  str
        evalBefore: Eval
        evalAfter: Eval
