import type {Feature, FeatureCollection, LineString, MultiLineString, MultiPolygon, Polygon} from 'geojson';

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
  bases: {camada: string; nome: string; metadado: string; legenda: string}[];
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

export type AreaManual = Feature<Polygon, {origem: string; finalidade: string; vertices: number}>;
export interface LegendaTrilha {id: string; nome: string; cor: string; opacidade: number; largura: number}
export type TrilhasGeoJSON = FeatureCollection<LineString | MultiLineString, {nome: string; id: number | null; cor: string; opacidade: number; largura: number}> & {fora_cobertura: boolean; legenda: LegendaTrilha[]};

export interface ProcessoANM {
  properties: {processo: string; numero: number; ano: number; titular: string; fase: string; area_ha: number; substancia: string; uf: string};
  fonte: {nome: string; url: string; consultado_em: string};
}
export interface PropriedadesReferencia {
  id: string; nome: string; cor: string; tipo: 'referencia' | 'influencia';
  origem: 'referencia_documental' | 'referencia_osm'; aproximada: true; finalidade: string; vertices: number;
  pagina_pdf?: number; figura?: string; data_mapa?: string;
  fonte?: {osm_id: number; osm_version: number; osm_timestamp: string; url: string; consultado_em: string};
}
export type AreaReferencia = Feature<Polygon, PropriedadesReferencia>;
export type ReferenciasTerritoriais = FeatureCollection<Polygon | MultiPolygon, PropriedadesReferencia> & {
  mina_id: string;
  fonte: {titulo: string; url: string; aviso: string; preparado_em: string; metodo: string};
};
export type AreaConfirmada = AreaManual | AreaReferencia;
export interface EstadoANM {dados: ProcessoANM | null; carregando: boolean; erro: string}

export type LimiteMunicipal = FeatureCollection<Polygon | MultiPolygon, {codigo_ibge: string}> & {fonte: {nome: string; url: string; qualidade: string; ano_referencia: null; consultado_em: string}};
