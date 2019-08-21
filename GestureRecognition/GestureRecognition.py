import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# GestureRecognition
#

class GestureRecognition(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "GestureRecognition" # TODO make this more human readable by adding spaces
        self.parent.categories = ["Examples"]
        self.parent.dependencies = []
        self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
        self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
        self.parent.helpText += self.getDefaultModuleDocumentationLink()
        self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# GestureRecognitionWidget
#

class GestureRecognitionWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModuleWidget.__init__(self,parent)
        slicer.mymod = self

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        # Instantiate and connect widgets ...

        #
        # Parameters Area
        #
        parametersCollapsibleButton = ctk.ctkCollapsibleButton()
        parametersCollapsibleButton.text = "Parameters"
        self.layout.addWidget(parametersCollapsibleButton)

        # Layout within the dummy collapsible button
        parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

        # input transform
        self.inputSelector = slicer.qMRMLNodeComboBox()
        self.inputSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
        #self.inputSelector.setNodeTypes("vtkMRMLLinearTransformNode")
        self.inputSelector.selectNodeUponCreation = True
        self.inputSelector.addEnabled = False
        self.inputSelector.removeEnabled = False
        self.inputSelector.noneEnabled = False
        self.inputSelector.showHidden = False
        self.inputSelector.showChildNodeTypes = False
        self.inputSelector.setMRMLScene( slicer.mrmlScene )
        self.inputSelector.setToolTip( "Pick a transform to observe." )
        parametersFormLayout.addRow("Input Transform: ", self.inputSelector)

        # Label Slider (1-5)
        self.labelSlider = ctk.ctkSliderWidget()
        self.labelSlider.singleStep = 1
        self.labelSlider.minimum = 1
        self.labelSlider.maximum = 5
        self.labelSlider.setToolTip("Choose label for the training sequence")
        parametersFormLayout.addRow("Gesture Label:", self.labelSlider)

        # Create Training Data File
        self.createTrainingFileButton = qt.QPushButton("Create Training File")
        self.createTrainingFileButton.connect('clicked(bool)', self.onCreateTrainingFileButtonPressed)
        parametersFormLayout.addRow("Create or Reinitialize Training Data File: ", self.createTrainingFileButton)

        # Start GRT Sequence
        self.startGRTSequenceButton = qt.QPushButton("Start Sequence")
        self.startGRTSequenceButton.toolTip = "Start the Sequence"
        self.startGRTSequenceButton.connect('clicked(bool)', self.onStartGRTSequenceButtonPressed)
        parametersFormLayout.addRow(self.startGRTSequenceButton)

        # Stop GRT Sequence
        self.stopGRTSequenceButton = qt.QPushButton("Stop Sequence")
        self.stopGRTSequenceButton.toolTip = "Stop the Sequence"
        self.stopGRTSequenceButton.connect('clicked(bool)', self.onStopGRTSequenceButtonPressed)
        parametersFormLayout.addRow(self.stopGRTSequenceButton)

        # Start Real-time Prediction
        self.predictionButton = qt.QPushButton("Start Prediction")
        self.predictionButton.toolTip = "Start real-time gesture recognition"
        parametersFormLayout.addRow(self.predictionButton)


        # Add vertical spacer
        self.layout.addStretch(0.5)
        self.arr = []
        self.numLines = 0

    def onCreateTrainingFileButtonPressed(self, value):
        file = open("C:/d/grt-bin/Debug/TrainingDataSlicer.grt", "w")
        file.write("GRT_LABELLED_TIME_SERIES_CLASSIFICATION_DATA_FILE_V1.0\n")
        file.write("DatasetName: DummyData\n")
        file.write("InfoText: This data contains some dummy timeseries data\n")
        file.write("NumDimensions: 3\n")
        file.write("TotalNumTrainingExamples: 15\n")
        file.write("NumberOfClasses: 3\n")
        file.write("ClassIDsAndCounters: \n")
        file.write("1   5\n")
        file.write("2   5\n")
        file.write("3   5\n")
        file.write("UseExternalRanges: 0\n")
        file.write("LabelledTimeSeriesTrainingData:")
        file.close()


    # Add the observer to current transform node in dropdown
    def onStartGRTSequenceButtonPressed(self, value):
        self.stopGRTSequenceButton.setDisabled(False)
        self.tranNode = self.inputSelector.currentNode()
        self.gestureLabel = self.labelSlider.value
        self.labelSlider.setDisabled(True)
        self.startGRTSequenceButton.setDisabled(True)
        print self.tranNode
        self.tranNodeObserver = self.tranNode.AddObserver(slicer.vtkMRMLTransformNode.TransformModifiedEvent, self.updateTransforms)


    def updateTransforms(self, caller, event):
        matr = self.tranNode.GetMatrixTransformToParent()
        x = matr.GetElement(0,3)
        y = matr.GetElement(1,3)
        z = matr.GetElement(2,3)
        print x
        self.numLines += 1
        self.arr.append((x,y,z))


    def onStopGRTSequenceButtonPressed(self, value):
        print "TEST"
        self.tranNode.RemoveObserver(self.tranNodeObserver)
        self.appendToTrainingDataFile()
        self.startGRTSequenceButton.setDisabled(False)
        self.stopGRTSequenceButton.setDisabled(True)
        self.labelSlider.setDisabled(False)
        self.arr = []
        self.numLines = 0

    def appendToTrainingDataFile(self):
        file = open("C:/d/grt-bin/Debug/TrainingDataSlicer.grt", "a+")
        #file = open('C:/users/danie/Documents/TrainingDataSlicer.grt', 'w')
        file.write("\n************TIME_SERIES************\n")
        file.write("ClassID: ")
        file.write(str(int(self.gestureLabel)))
        file.write("\nTimeSeriesLength: ")
        file.write(str(self.numLines))
        file.write("\nTimeSeriesData: ")
        for i in range(self.numLines):
            file.write("\n" + str(self.arr[i][0]) + "  " + str(self.arr[i][1]) + "  " + str(self.arr[i][2]))

        file.close()


    def cleanup(self):
        pass


#
# GestureRecognitionLogic
#

class GestureRecognitionLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent = None):
        ScriptedLoadableModuleLogic.__init__(self, parent)
        slicer.mymod = self




class GestureRecognitionTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_GestureRecognition1()

    def test_GestureRecognition1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")
        #
        # first, get some data
        #
        import SampleData
        SampleData.downloadFromURL(
            nodeNames='FA',
            fileNames='FA.nrrd',
            uris='http://slicer.kitware.com/midas3/download?items=5767')
        self.delayDisplay('Finished with download and loading')

        volumeNode = slicer.util.getNode(pattern="FA")
        logic = GestureRecognitionLogic()
        self.assertIsNotNone( logic.hasImageData(volumeNode) )
        self.delayDisplay('Test passed!')
