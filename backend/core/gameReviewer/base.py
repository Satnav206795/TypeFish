from dataclasses import dataclass
import chess


#Evaluation
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
        bestMoveUCI: chess.Move
        moveMadeUCI:  chess.Move
        evalBefore: Eval
        evalAfter: Eval

@dataclass(frozen=True)
class GameReview:
      moves: list[Result]