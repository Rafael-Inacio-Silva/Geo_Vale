import type {FeatureCollection, LineString, MultiLineString, MultiPolygon, Polygon} from 'geojson';

export interface Mina {
  id: string;
  nome: string;
  nome_anterior: string;
  empresa: string;
  municipio: string;
  uf: string;
  complexo: string;
  latitude: number;
  longitude: number;
  referencia_localizacao: string;
  fontes: Record<string, string>;
  codigo_municipio_ibge: string;
  processo_anm: {numero: number; ano: number};
}

export interface Fundo {
  id: string;
  nome: string;
  url: string;
  credito: string;
  zoom_maximo: number;
}

export interface CamadaTerritorial {
  id: string;
  nome: string;
  tipo: 'wms' | 'geojson';
  cobertura: [[number, number], [number, number]];
  alcance: string;
  cor: string;
  opacidade: number;
  ordem: number;
  url: string;
  credito: string;
  bases: {camada: string; nome: string; metadado: string; legenda: string; mapa?: false}[];
}

export type CamadasAtivas = Record<string, number>;
export type EstadoCamada = 'carregando' | 'pronta' | 'erro' | 'fora' | 'vazia';

export interface ConfiguracaoMapa {
  estado: {nome: string; centro: [number, number]; zoom: number};
  minas: Mina[];
  fundos: Fundo[];
  camadas: CamadaTerritorial[];
}

export type LimiteMG = FeatureCollection<Polygon | MultiPolygon> & {
  fonte: {nome: string; consultado_em: string};
  aviso: string | null;
};

export interface LegendaTrilha {id: string; nome: string; cor: string; opacidade: number; largura: number}
export type TrilhasGeoJSON = FeatureCollection<LineString | MultiLineString, {nome: string; id: number | null; cor: string; opacidade: number; largura: number}> & {fora_cobertura: boolean; legenda: LegendaTrilha[]};

export interface ProcessoANM {
  properties: {processo: string; numero: number; ano: number; titular: string; fase: string; area_ha: number; substancia: string; uf: string};
  fonte: {nome: string; url: string; consultado_em: string};
}
export type InfluenciaTerritorial = FeatureCollection<Polygon | MultiPolygon, {
  id: 'mina' | 'influencia'; nome: string; cor: string; origem: string;
  aproximada: true; fonte?: {url: string};
}> & {mina_id: string; fonte: {titulo: string; url: string; aviso: string; preparado_em: string; metodo: string}};

export interface EstadoANM {dados: ProcessoANM | null; carregando: boolean; erro: string}

export type LimiteMunicipal = FeatureCollection<Polygon | MultiPolygon, {codigo_ibge: string}> & {fonte: {nome: string; url: string; qualidade: string; ano_referencia: null; consultado_em: string}};


export interface TerritorioPreparado {completo: boolean}

export interface UsoSugerido {uso: string; nome: string; cor: string; nota: number; permitido: number}
export interface SetorSugerido {
  id: string; ha: number; descricao: string; ranking: UsoSugerido[]; margem: number; cavidades: number; montante: string[];
  robustez: {estavel: boolean; muda_com: string[]}; explicacao: string; geometria: Polygon | MultiPolygon;
}
export interface SugestaoUso {
  criterios: {id: string; nome: string; curto: string; peso: number; peso_ahp: number}[];
  origem_pesos: 'AHP' | 'engenheiro'; razao_consistencia: number; minimo_ha: number; fora_ha: number; variacao: number;
  usos: {id: string; nome: string; cor: string}[]; setores: SetorSugerido[];
}
