"""Leitura multipart com limite por bytes reais, reaproveitada da entrada validada."""
from collections.abc import AsyncIterator
from fastapi import Request
from starlette.datastructures import UploadFile
from starlette.formparsers import MultiPartException, MultiPartParser
from geovale.geografia.entrada import ErroEntrada, MAX_BYTES
MAX_CORPO = MAX_BYTES + 16_384

class MultipartCompleto(MultiPartParser):
    """Detecta também um envio interrompido antes do delimitador final."""

    finalizado = False

    def on_end(self) -> None:
        """Marca que o parser encontrou o encerramento do multipart."""
        self.finalizado = True


async def _fluxo_limitado(request: Request) -> AsyncIterator[bytes]:
    """Interrompe leitura por bytes reais, mesmo sem Content-Length confiável."""
    total = 0
    async for bloco in request.stream():
        total += len(bloco)
        if total > MAX_CORPO:
            raise ErroEntrada("CORPO_GRANDE", "O envio excede 1 MiB de arquivo e 16 KiB de overhead multipart.", status=413)
        yield bloco


async def _ler_arquivo(request: Request) -> tuple[bytes, str]:
    """Aceita somente um campo arquivo, fecha temporários e limita sua leitura."""
    tipo = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if tipo != "multipart/form-data":
        raise ErroEntrada("TRANSPORTE_INVALIDO", "Envie multipart/form-data com um único campo arquivo.", status=400)
    parser = MultipartCompleto(request.headers, _fluxo_limitado(request), max_files=1, max_fields=0)
    try:
        formulario = await parser.parse()
    except MultiPartException as exc:
        raise ErroEntrada("MULTIPART_INVALIDO", "O envio multipart está inválido. Use um único campo arquivo e seu delimitador completo.", status=400) from exc
    try:
        itens = formulario.multi_items()
        if not parser.finalizado or len(itens) != 1 or itens[0][0] != "arquivo" or not isinstance(itens[0][1], UploadFile):
            raise ErroEntrada("ARQUIVO_AUSENTE", "Envie exatamente um campo arquivo com o GeoJSON completo.", status=400)
        arquivo = itens[0][1]
        conteudo = bytearray()
        while bloco := await arquivo.read(65_536):
            conteudo.extend(bloco)
            if len(conteudo) > MAX_BYTES:
                raise ErroEntrada("ARQUIVO_GRANDE", "O arquivo excede o máximo de 1 MiB (1.048.576 bytes).", status=413)
        nome = (arquivo.filename or "").replace("\\", "/").rsplit("/", 1)[-1]
        return bytes(conteudo), nome
    finally:
        await formulario.close()
