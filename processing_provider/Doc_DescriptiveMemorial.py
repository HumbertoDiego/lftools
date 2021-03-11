# -*- coding: utf-8 -*-

"""
***************************************************************************
    Doc_DescriptiveMemorial.py
    ---------------------
    Date                 : Sept 22
    Copyright            : (C) 2019 by Leandro França
    Email                : geoleandro.franca@gmail.com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Leandro França'
__date__ = 'Sept 22'
__copyright__ = '(C) 2019, Leandro França'

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProject,
                       QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingException,
                       QgsProcessingParameterFileDestination,
                       QgsApplication)
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from math import atan, pi, sqrt, floor
import math
from lftools.geocapt.imgs import Imgs, lftools_logo
from lftools.geocapt.cartography import FusoHemisf
from lftools.geocapt.topogeo import str2HTML, dd2dms, azimute
import os
from qgis.PyQt.QtGui import QIcon

class DescriptiveMemorial(QgisAlgorithm):
    """
    This algorithm takes three vector layers (point, line, and polygon)
    that define a specific ownership and creates an HTML file with the
    descriptive characteristics of the area.
    """
    HTML = 'HTML'
    INPUT1 = 'INPUT1'
    INPUT2 = 'INPUT2'
    INPUT3 = 'INPUT3'
    LOC = QgsApplication.locale()


    def translate(self, string):
        return QCoreApplication.translate('Processing', string)

    def tr(self, *string):
        # Traduzir para o portugês: arg[0] - english (translate), arg[1] - português
        if self.LOC == 'pt':
            if len(string) == 2:
                return string[1]
            else:
                return self.translate(string[0])
        else:
            return self.translate(string[0])

    def createInstance(self):
        return DescriptiveMemorial()

    def name(self):
        return 'descriptivememorial'

    def displayName(self):
        return self.tr('Descriptive Memorial', 'Memorial Descritivo')

    def group(self):
        return self.tr('Documents', 'Documentos')

    def groupId(self):
        return 'documents'

    def tags(self):
        return self.tr('area,perimeter,descriptive,memorial,property,topography,survey,real,estate,georreferencing,plan,cadastral,cadastre,documnt').split(',')

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/document.png'))

    def shortHelpString(self):
        txt_en = 'Elaboration of Descriptive Memorials based on vector layers that define a property.'
        txt_pt = 'Elaboração de Memorial Descritivo a partir de camadas vetorias que definem uma propriedade.'
        social_BW = Imgs().social_BW
        footer = '''<div align="center">
                      <img src="'''+ os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/tutorial/doc_descriptive_memorial.jpg') +'''">
                      </div>
                      <div align="right">
                      <div>''' + self.tr('This tool works properly only with data in "topogeo" modeling.',
                                         'Esta ferramenta funciona adequadamente com os dados na modelagem "topogeo".') + '''
                      </div>
                      <p align="right">
                      <b><a href="https://www.researchgate.net/publication/346925730_PROPOSICAO_METODOLOGICA_COM_EMPREGO_DE_SOFTWARE_LIVRE_PARA_A_ELABORACAO_DE_DOCUMENTOS_DE_LEVANTAMENTO_TOPOGRAFICO_DE_IMOVEIS_DA_UNIAO_Methodological_proposition_with_the_use_of_free_software_for_the_p" target="_blank">'''+self.tr('Click here for more informations!',
                                    'Clique aqui para saber mais sobre essa modelagem!') +'</a><br><br>'+ self.tr('Author: Leandro Franca', 'Autor: Leandro França')+'''</b>
                      </p>'''+ social_BW + '''</div>
                    </div>'''
        return self.tr(txt_en, txt_pt) + footer

    def initAlgorithm(self, config=None):
        # 'INPUTS'
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                'INPUT1',
                self.tr('Boundary Survey Points', 'Pontos de Limite'),
                types=[QgsProcessing.TypeVectorPoint]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                'INPUT2',
                self.tr('Neighborhood Dividing Line', 'Elemento Confrontante'),
                types=[QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                'INPUT3',
                self.tr('Property Polygon', 'Área do Imóvel'),
                types=[QgsProcessing.TypeVectorPolygon]
            )
        )
        # 'OUTPUTS'
        self.addParameter(
            QgsProcessingParameterFileDestination(
                'HTML',
                self.tr('Descriptive Memorial', 'Memorial Descritivo'),
                self.tr('HTML files (*.html)')
            )
        )


    def processAlgorithm(self, parameters, context, feedback):

        vertices = self.parameterAsSource(parameters,
                                                     'INPUT1',
                                                     context)
        limites = self.parameterAsSource(parameters,
                                                     'INPUT2',
                                                     context)
        area = self.parameterAsSource(parameters,
                                                     'INPUT3',
                                                     context)

        meses = {1: 'janeiro', 2:'fevereiro', 3: 'março', 4:'abril', 5:'maio', 6:'junho', 7:'julho', 8:'agosto', 9:'setembro', 10:'outubro', 11:'novembro', 12:'dezembro'}

        # VALIDAÇÃO DOS DADOS DE ENTRADA!!!
        # atributos codigo deve ser preenchido
        # ordem do numeros

        # Pegando informações dos confrontantes (limites)
        ListaDescr = []
        ListaCont = []
        soma = 0
        for linha in limites.getFeatures():
            Lin_coord = linha.geometry().asMultiPolyline()[0]
            ListaDescr += [[str2HTML(linha['descr_pnt_inicial']), str2HTML(linha['confrontante'])]]
            cont = len(Lin_coord)
            ListaCont += [(soma, cont-1)]
            soma += cont-1

        # Pegando o SRC do Projeto
        SRC = QgsProject.instance().crs().description()
        # Verificando o SRC
        if QgsProject.instance().crs().isGeographic():
            raise QgsProcessingException(self.tr('The Project CRS must be projected!', 'O SRC do Projeto deve ser Projetado!'))
        feedback.pushInfo(self.tr('Project CRS is {}.', 'SRC do Projeto é {}.').format(SRC))

        # Dados do levantamento
        for feat in area.getFeatures():
                feat1 = feat
                break

        geom = feat1.geometry()
        centroideG = geom.centroid().asPoint()

        # Validando dados de entrada
        # ponto_limite
        ordem_list = list(range(1,vertices.featureCount()+1))
        ordem_comp = []
        for feat in vertices.getFeatures():
            ordem_comp += [feat['ordem']]
            codigo_item = feat['codigo']
            if not codigo_item or codigo_item in ['', ' ']:
                raise QgsProcessingException(self.tr('The code attribute must be filled in for all features!', 'O atributo código deve ser preenchido para todas as feições!'))
        ordem_comp.sort()
        if ordem_list != ordem_comp:
            raise QgsProcessingException(self.tr('The point sequence field must be filled in correctly!', 'O campo de sequência dos pontos deve preenchido corretamente!'))
        # elemento_confrontante
        for feat in limites.getFeatures():
            att1 = feat['descr_pnt_inicial']
            if not att1 or att1 in ['', ' ']:
                raise QgsProcessingException(self.tr('The attribute of the starting point description must be filled in for all features!', 'O atributo de descrição do ponto inicial deve ser preenchido para todas as feições!'))
            att2 = feat['confrontante']
            if not att2 or att2 in ['', ' ']:
                raise QgsProcessingException(self.tr("The confrontant's name must be filled in for all features!", 'O nome do confrontante deve ser preenchido para todas as feições!'))
        # area_imovel
        Fields = area.fields()
        fieldnames = [field.name() for field in Fields]
        for fieldname in fieldnames:
            att = feat1[fieldname]
            if not att or att in ['', ' ']:
                raise QgsProcessingException(self.tr('All attributes of the class "area_imovel" must be filled!', 'Todos os atributos da classe "area_imovel" devem ser preenchido!'))

        # Transformar Coordenadas de Geográficas para o sistema UTM
        coordinateTransformer = QgsCoordinateTransform()
        coordinateTransformer.setDestinationCrs(QgsProject.instance().crs())
        coordinateTransformer.setSourceCrs(vertices.sourceCrs())

        pnts = {}

        for feat in vertices.getFeatures():
            geom = feat.geometry()
            if geom.isMultipart():
                pnts[feat['ordem']] = [coordinateTransformer.transform(geom.asMultiPoint()[0]), feat['tipo'], feat['codigo'] ]
            else:
                pnts[feat['ordem']] = [coordinateTransformer.transform(geom.asPoint()), feat['tipo'], feat['codigo'] ]

        # Cálculo dos Azimutes e Distâncias
        tam = len(pnts)
        Az_lista, Dist = [], []
        for k in range(tam):
            pntA = pnts[k+1][0]
            pntB = pnts[max((k+2)%(tam+1),1)][0]
            Az_lista += [(180/pi)*azimute(pntA, pntB)[0]]
            Dist += [sqrt((pntA.x() - pntB.x())**2 + (pntA.y() - pntB.y())**2)]


        texto_inicial = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
      <meta content="text/html; charset=ISO-8859-1"
     http-equiv="content-type">
      <title>'''+ self.tr('Descriptive memorial', 'Memorial descritivo') + '''</title>
    </head>
    <body>
    <div style="text-align: center;"><span style="font-weight: bold;"><br>
    <img src="data:image/png;base64,'''+ lftools_logo + '''">
    <br>'''+ self.tr(str2HTML('CARTOGRAPHY & SURVEYING'), str2HTML('CARTOGRAFIA & AGRIMENSURA')) + '''</span><br style="font-weight: bold;">
    <br></div>
    <p class="western"
     style="margin-bottom: 0.0001pt; text-align: center;"
     align="center"><b><u><span style="font-size: 12pt;">'''+ self.tr('DESCRIPTIVE MEMORIAL','MEMORIAL DESCRITIVO') + '''</span></u></b><o:p></o:p></p>
    <p class="western" style="margin-bottom: 0.0001pt;"><o:p>&nbsp;</o:p></p>
    <table class="MsoTableGrid"
     style="border: medium none ; border-collapse: collapse;"
     border="0" cellpadding="0" cellspacing="0">
      <tbody>
        <tr style="">
          <td style="padding: 0cm 5.4pt; width: 247.85pt;"
     valign="top" width="330">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>'''+ self.tr('Property',str2HTML('Imóvel')) + ''': </b>[IMOVEL]<o:p></o:p></p>
          </td>
          <td style="padding: 0cm 5.4pt; width: 176.85pt;"
     valign="top" width="236">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>''' + self.tr('Real estate registry', 'Registro') + ''':</b>
    [REGISTRO]<o:p></o:p></p>
          </td>
        </tr>
        <tr style="">
          <td colspan="2"
     style="padding: 0cm 5.4pt; width: 424.7pt;" valign="top"
     width="566">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>''' + self.tr('Owner', str2HTML('Proprietário')) + ''':</b>
    [PROPRIETARIO]<o:p></o:p></p>
          </td>
        </tr>
        <tr style="">
          <td style="padding: 0cm 5.4pt; width: 247.85pt;"
     valign="top" width="330">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>''' + self.tr('County', str2HTML('Município')) + ''':</b>
    [MUNICIPIO]<b><o:p></o:p></b></p>
          </td>
          <td style="padding: 0cm 5.4pt; width: 176.85pt;"
     valign="top" width="236">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>''' + self.tr('State', str2HTML('Estado')) + ''':
          </b>[UF]<o:p></o:p></p>
          </td>
        </tr>
        <tr style="">
          <td colspan="2"
     style="padding: 0cm 5.4pt; width: 424.7pt;" valign="top"
     width="566">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>''' + self.tr('Registration(s)', str2HTML('Matrícula(s)')) + ''':</b>
    [MATRICULAS]<o:p></o:p></p>
          </td>
        </tr>
        <tr style="">
          <td style="padding: 0cm 5.4pt; width: 247.85pt;"
     valign="top" width="330">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>''' + self.tr('Area', str2HTML('Área')) + ''' (m<sup>2</sup>): </b>[AREA]<o:p></o:p></p>
          </td>
          <td style="padding: 0cm 5.4pt; width: 176.85pt;"
     valign="top" width="236">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>''' + self.tr('Perimeter', str2HTML('Perímetro')) + ''' (m):</b> [PERIMETRO]<o:p></o:p></p>
          </td>
        </tr>
        <tr style="">
          <td colspan="2"
     style="padding: 0cm 5.4pt; width: 424.7pt;" valign="top"
     width="566">
          <p class="western" style="margin-bottom: 0.0001pt;"><b>''' + self.tr('Coordinate Reference System', str2HTML('Sistema de Referência de Coordenadas')) + ''':</b> [SRC]<b><o:p></o:p></b></p>
          </td>
        </tr>
      </tbody>
    </table>
    <p class="western" style="margin-bottom: 0.0001pt;"><o:p>&nbsp;</o:p></p>
    <p class="western"
     style="margin-bottom: 0.0001pt; text-align: justify;">'''+ self.tr('The description of this perimeter begins ', str2HTML('Inicia-se a descrição deste perímetro n'))

        texto_var1 = self.tr('at the vertex ', str2HTML('o vértice ')) + '''<b>[Vn]</b>, '''+ self.tr('with coordinates ', 'de coordenadas ') + '''<b>N [Nn]m </b>''' + self.tr('and','e') +''' <b>E [En]m</b>,
    [Descr_k], '''+ self.tr('from this, it continues to confront [Confront_k], with the following flat azimuths and distances: [Az_n] and [Dist_n]m up to ',
                   str2HTML('deste, segue confrontando com [Confront_k], com os seguintes azimutes planos e distâncias: [Az_n] e [Dist_n]m até '))

        texto_var2 = self.tr('the vertex ', str2HTML('o vértice ')) + '''<span> </span><b>[Vn]</b>, '''+ self.tr('with coordinates ', 'de coordenadas ') + '''<b>N [Nn]m </b>''' + self.tr('and','e')+''' <b>E [En]m</b>; '''+ self.tr('[Az_n] and [Dist_n]m up to ', str2HTML('[Az_n] e [Dist_n]m até '))

        texto_final = self.tr('the vertex ', str2HTML('o vértice ')) + '''<b>[P-01]</b>, '''+ self.tr('with coordinates', 'de coordenadas') + ''' <b>N [N1]m </b>''' + self.tr('and','e')+''' <b>E [E1]m</b>,
    ''' + self.tr('the starting point for the description of this perimeter. All coordinates described here are georeferenced to the Geodetic Reference System (SGR)',
         str2HTML('ponto inicial da descrição deste perímetro. Todas as coordenadas aqui descritas estão georreferenciadas ao Sistema Geodésico de Referência (SGR)')) + ''' <b>[GRS]</b>,
    ''' + self.tr('and are projected in the UTM system, zone [FUSO] and hemisphere [HEMISFERIO], from which all azimuths and distances, area and perimeter were calculated.',
         str2HTML('e encontram-se projetadas no Sistema UTM, fuso [FUSO] e hemisfério [HEMISFERIO], a partir das quais todos os azimutes e distâncias, área e perímetro foram calculados.')) + '''
     <o:p></o:p></p>
    <p class="western"
     style="margin-bottom: 0.0001pt; text-align: right;"
     align="right">[LOCAL], [DATA].<o:p></o:p></p>
    <p class="western" style="margin-bottom: 0.0001pt;"><o:p>&nbsp;</o:p></p>
    <p class="western"
     style="margin: 0cm 0cm 0.0001pt; text-align: center;"
     align="center">___________________________________________<o:p></o:p></p>
    <p class="western"
     style="margin: 0cm 0cm 0.0001pt; text-align: center;"
     align="center">[RESP_TEC]<o:p></o:p></p>
    <p class="western"
     style="margin: 0cm 0cm 0.0001pt; text-align: center;"
     align="center">[CREA]<o:p></o:p></p>
    <p class="western"
     style="margin: 0cm 0cm 0.0001pt; text-align: center;"
     align="center">''' + self.tr('TECHNICAL MANAGER', str2HTML('RESPONSÁVEL TÉCNICO')) + '''<o:p></o:p></p>
    <p class="MsoNormal"><o:p>&nbsp;</o:p></p>
    </body>
    </html>
    '''
        # Inserindo dados iniciais do levantamento
        itens = {'[IMOVEL]': str2HTML(feat1['imóvel']),
                '[PROPRIETARIO]': str2HTML(feat1['proprietário']),
                '[UF]': feat1['UF'],
                '[MATRICULAS]': str2HTML(feat1['matrícula']),
                '[AREA]': self.tr('{:,.2f}'.format(feat1['area']), '{:,.2f}'.format(feat1['area']).replace(',', 'X').replace('.', ',').replace('X', '.')),
                '[SRC]': SRC,
                '[REGISTRO]': str2HTML(feat1['cadastro']),
                '[MUNICIPIO]': str2HTML(feat1['município']),
                '[PERIMETRO]': self.tr('{:,.2f}'.format(feat1['perimetro']), '{:,.2f}'.format(feat1['perimetro']).replace(',', 'X').replace('.', ',').replace('X', '.')),
                    }

        for item in itens:
                texto_inicial = texto_inicial.replace(item, itens[item])

        LINHAS = texto_inicial
        for w,t in enumerate(ListaCont):
            linha0 = texto_var1
            itens =    {'[Vn]': pnts[t[0]+1][2],
                        '[En]': self.tr('{:,.2f}'.format(pnts[t[0]+1][0].x()), '{:,.2f}'.format(pnts[t[0]+1][0].x()).replace(',', 'X').replace('.', ',').replace('X', '.')),
                        '[Nn]': self.tr('{:,.2f}'.format(pnts[t[0]+1][0].y()), '{:,.2f}'.format(pnts[t[0]+1][0].y()).replace(',', 'X').replace('.', ',').replace('X', '.')),
                        '[Az_n]': str2HTML(self.tr(dd2dms(Az_lista[t[0]],2), dd2dms(Az_lista[t[0]],2).replace('.', ','))),
                        '[Dist_n]': self.tr('{:,.2f}'.format(Dist[t[0]]), '{:,.2f}'.format(Dist[t[0]]).replace(',', 'X').replace('.', ',').replace('X', '.')),
                        '[Descr_k]': ListaDescr[w][0],
                        '[Confront_k]': ListaDescr[w][1]
                        }
            for item in itens:
                linha0 = linha0.replace(item, itens[item])
            LINHAS += linha0
            LIN0 = ''
            for k in range(t[0]+1, t[0]+t[1]):
                linha1 = texto_var2
                itens = {'[Vn]': pnts[k+1][2],
                        '[En]': self.tr('{:,.2f}'.format(pnts[k+1][0].x()), '{:,.2f}'.format(pnts[k+1][0].x()).replace(',', 'X').replace('.', ',').replace('X', '.')),
                        '[Nn]': self.tr('{:,.2f}'.format(pnts[k+1][0].y()), '{:,.2f}'.format(pnts[k+1][0].y()).replace(',', 'X').replace('.', ',').replace('X', '.')),
                        '[Az_n]': str2HTML(self.tr(dd2dms(Az_lista[k],2), dd2dms(Az_lista[k],2).replace('.', ','))),
                        '[Dist_n]': self.tr('{:,.2f}'.format(Dist[k]), '{:,.2f}'.format(Dist[k]).replace(',', 'X').replace('.', ',').replace('X', '.'))
                        }
                for item in itens:
                    linha1 = linha1.replace(item, itens[item])
                LIN0 += linha1
            LINHAS += LIN0

        # Inserindo dados finais
        itens = {   '[P-01]': pnts[1][2],
                     '[N1]': self.tr('{:,.2f}'.format(pnts[1][0].y()), '{:,.2f}'.format(pnts[1][0].y()).replace(',', 'X').replace('.', ',').replace('X', '.')),
                     '[E1]': self.tr('{:,.2f}'.format(pnts[1][0].x()), '{:,.2f}'.format(pnts[1][0].x()).replace(',', 'X').replace('.', ',').replace('X', '.')),
                     '[GRS]': SRC.split(' /')[0],
                     '[FUSO]': str(FusoHemisf(centroideG)[0]),
                     '[HEMISFERIO]': FusoHemisf(centroideG)[1],
                     '[RESP_TEC]': str2HTML(feat1['Resp_Tecnico'].upper()),
                     '[CREA]': str2HTML(feat1['CREA']),
                     '[LOCAL]': str2HTML((feat1['município']).title() +' - ' + (feat1['UF']).upper()),
                     '[DATA]': self.tr((feat1['data_levantamento'].toPyDate()).strftime("%b %d, %Y"),
                                       (feat1['data_levantamento'].toPyDate()).strftime("%d de {} de %Y").format(meses[feat1['data_levantamento'].month()]))
                    }

        for item in itens:
                texto_final = texto_final.replace(item, itens[item])

        LINHAS += texto_final

        output = self.parameterAsFileOutput(parameters, self.HTML, context)
        arq = open(output, 'w')
        arq.write(LINHAS)
        arq.close()

        # Check for cancelation
        if feedback.isCanceled():
            return {}

        feedback.pushInfo(self.tr('Operation completed successfully!', 'Operação finalizada com sucesso!'))
        feedback.pushInfo(self.tr('Leandro França - Cartographic Engineer', 'Leandro França - Eng Cart'))

        return {self.HTML: output}