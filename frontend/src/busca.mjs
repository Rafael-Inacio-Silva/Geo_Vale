/** Uniformiza acentos e caixa sem alterar os nomes exibidos. */
function normalizar(texto) {
  return texto.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
}

/** Pesquisa o catálogo recebido, incluindo o nome anterior da mesma mina. */
export function filtrarMinas(minas, consulta) {
  const termos = normalizar(consulta).split(/\s+/).filter(Boolean);
  return minas.filter(mina => {
    const texto = normalizar([mina.nome, mina.nome_anterior, mina.empresa, mina.municipio, mina.uf].join(' '));
    return termos.every(termo => texto.includes(termo));
  });
}
