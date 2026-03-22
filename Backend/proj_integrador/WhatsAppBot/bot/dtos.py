from dataclasses import dataclass, field
from typing import Optional

class UsuarioContextoDTO:
    wa_id: str
    nome: Optional[str] = None
    cpf: Optional[str] = None

@dataclass
class AgendamentoDTO:
    usuario_wa_id: str
    data: Optional[str] = None
    horario: Optional[str] = None