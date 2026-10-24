/** Contrato resumido da jornada; fontes, matrizes e trilhas permanecem no servidor. */
export interface Criterio { id:string; nome:string; descricao:string }
export interface Opcao { id:string; nome:string; posicao:number; indice:number; explicacao:string; descricao:string }
export interface Estudo {
  id:string; versao:number; nome:string; localizacao:string; arquivo:string; area_ha:number; numero_partes:number;
  geometria:GeoJSON.Geometry; bbox:[number,number,number,number];
  imagem:null|{url:string; bounds:[[number,number],[number,number]]; credito:string};
  cobertura_disponivel:boolean; analisada:boolean;
  resumo:null|{declividade_mediana_graus:number; declividade_p90_graus:number; cobertura_predominante:string; ano_cobertura:number; pendencias:string[]};
  criterios:Criterio[]; pesos:number[]; origem_pesos:string; salvo_revisao:number|null; aviso:string; perfil:string;
  resultado:null|{ranking:Opcao[]; alcance:string; sem_discriminacao:boolean; sensivel_aos_pesos:boolean; calculado_em:string};
}
