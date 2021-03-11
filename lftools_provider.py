# -*- coding: utf-8 -*-

"""
/***************************************************************************
 LFTools
                                 A QGIS plugin
 Tools for cartographic production and spatial analysis.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-01
        copyright            : (C) 2021 by Leandro Franca
        email                : geoleandro.franca@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Leandro Franca'
__date__ = '2021-02-18'
__copyright__ = '(C) 2021 by Leandro Franca'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'
import os
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from lftools.processing_provider.Cart_inom2utm import Inom2utmGrid
from lftools.processing_provider.Cart_coord2utm import Coord2UTMGrid
from lftools.processing_provider.Cart_extent2utm import Extent2UTMGrid
from lftools.processing_provider.Survey_closedPolygonal import ClosedPolygonal
from lftools.processing_provider.Survey_Estimate3dCoord import Estimate3dCoord
from lftools.processing_provider.Survey_helmert2D import Helmert2D
from lftools.processing_provider.Survey_LocalTangentPlane import LocalTangentPlane
from lftools.processing_provider.Survey_traverseAdjustment import TraverseAdjustment
from lftools.processing_provider.Survey_azimuthDistance import AzimuthDistance
from lftools.processing_provider.Stat_confidenceEllipse import ConfidenceEllipse
from lftools.processing_provider.Stat_randomDist import RandomDist
from lftools.processing_provider.Easy_coord2layer import CoordinatesToLayer
from lftools.processing_provider.Easy_measures_layers import MeasureLayers
from lftools.processing_provider.Rast_Bands2RGB import Bands2RGB
from lftools.processing_provider.Rast_compressJPEG import CompressJPEG
from lftools.processing_provider.Rast_createHolesInRaster import CreateHolesInRaster
from lftools.processing_provider.Rast_defineNullCell import DefineNullCell
from lftools.processing_provider.Rast_extractRasterBand import ExtractRasterBand
from lftools.processing_provider.Rast_fillRasterwithPatches import FillRasterwithPatches
from lftools.processing_provider.Rast_inventoryRaster import InventoryRaster
from lftools.processing_provider.Rast_loadRasterByLocation import LoadRasterByLocation
from lftools.processing_provider.Rast_mosaicRaster import MosaicRaster
from lftools.processing_provider.Rast_removeAlphaBand import RemoveAlphaBand
from lftools.processing_provider.Rast_rescaleTo8bits import RescaleTo8bits
from lftools.processing_provider.Rast_supervisedClassification import SupervisedClassification
from lftools.processing_provider.Reamb_ImportPhotos import ImportPhotos
from lftools.processing_provider.Vect_DirectionalMerge import DirectionalMerge
from lftools.processing_provider.Vect_ExtendLines import ExtendLines
from lftools.processing_provider.Vect_PolygonAngles import CalculatePolygonAngles
from lftools.processing_provider.Vect_reverseVertexOrder import ReverseVertexOrder
from lftools.processing_provider.Vect_sequencePoints import SequencePoints
from lftools.processing_provider.Doc_AreaPerimeter import AreaPerimterReport
from lftools.processing_provider.Doc_DescriptiveMemorial import DescriptiveMemorial
from lftools.processing_provider.Doc_MarkInformation import SurveyMarkDoc
from lftools.processing_provider.Doc_DescriptiveTable import DescriptiveTable
from lftools.processing_provider.Post_Restore import Restore
from lftools.processing_provider.Post_Backup import Backup
from lftools.processing_provider.Post_CloneDB import CloneDB
from lftools.processing_provider.Post_DeleteDB import DeleteDB
from lftools.processing_provider.Post_RenameDB import RenameDB
from lftools.processing_provider.Post_ImportRaster import ImportRaster
from lftools.processing_provider.Post_ChangeEnconding import ChangeEnconding

class LFToolsProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):

        self.addAlgorithm(Inom2utmGrid())
        self.addAlgorithm(Coord2UTMGrid())
        self.addAlgorithm(Extent2UTMGrid())
        self.addAlgorithm(ClosedPolygonal())
        self.addAlgorithm(Estimate3dCoord())
        self.addAlgorithm(Helmert2D())
        self.addAlgorithm(LocalTangentPlane())
        self.addAlgorithm(TraverseAdjustment())
        self.addAlgorithm(ConfidenceEllipse())
        self.addAlgorithm(RandomDist())
        self.addAlgorithm(CoordinatesToLayer())
        self.addAlgorithm(MeasureLayers())
        self.addAlgorithm(Bands2RGB())
        self.addAlgorithm(CompressJPEG())
        self.addAlgorithm(CreateHolesInRaster())
        self.addAlgorithm(DefineNullCell())
        self.addAlgorithm(ExtractRasterBand())
        self.addAlgorithm(FillRasterwithPatches())
        self.addAlgorithm(InventoryRaster())
        self.addAlgorithm(LoadRasterByLocation())
        self.addAlgorithm(MosaicRaster())
        self.addAlgorithm(RemoveAlphaBand())
        self.addAlgorithm(RescaleTo8bits())
        self.addAlgorithm(SupervisedClassification())
        self.addAlgorithm(ImportPhotos())
        self.addAlgorithm(DirectionalMerge())
        self.addAlgorithm(ExtendLines())
        self.addAlgorithm(CalculatePolygonAngles())
        self.addAlgorithm(ReverseVertexOrder())
        self.addAlgorithm(SequencePoints())
        self.addAlgorithm(AreaPerimterReport())
        self.addAlgorithm(DescriptiveMemorial())
        self.addAlgorithm(SurveyMarkDoc())
        self.addAlgorithm(DescriptiveTable())
        self.addAlgorithm(AzimuthDistance())
        self.addAlgorithm(Restore())
        self.addAlgorithm(Backup())
        self.addAlgorithm(CloneDB())
        self.addAlgorithm(DeleteDB())
        self.addAlgorithm(RenameDB())
        self.addAlgorithm(ImportRaster())
        self.addAlgorithm(ChangeEnconding())

    def id(self):
        return 'lftools'

    def name(self):
        return self.tr('LF Tools')

    def icon(self):
        return QIcon(os.path.dirname(__file__) + '/images/lftoos.png')

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()