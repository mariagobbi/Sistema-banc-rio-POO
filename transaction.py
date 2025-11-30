from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transaction:
    timestamp: str
    tipo: str
    origem_num: Optional[int]
    destino_num: Optional[int]
    valor: float
    taxa: float
    saldo_origem_pos: Optional[float]
    saldo_destino_pos: Optional[float]

    @classmethod
    def create(cls, tipo: str, origem_num: Optional[int], destino_num: Optional[int],
               valor: float, taxa: float, saldo_origem_pos: Optional[float],
               saldo_destino_pos: Optional[float]):
        ts = datetime.now().isoformat(timespec='seconds')
        return cls(ts, tipo, origem_num, destino_num, round(valor, 2), round(taxa, 2),
                   None if saldo_origem_pos is None else round(saldo_origem_pos, 2),
                   None if saldo_destino_pos is None else round(saldo_destino_pos, 2))