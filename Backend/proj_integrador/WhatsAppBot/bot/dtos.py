from dataclasses import dataclass, field
from typing import Optional

@dataclass
class UsuarioContextoDTO:
    wa_id: str
    nome: Optional[str] = None


@dataclass
class AgendamentoDTO:
    usuario_wa_id: str
    data: Optional[str] = None
    horario: Optional[str] = None


