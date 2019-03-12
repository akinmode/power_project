#GUI classes for the application
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

#Default packages
import json, os
import datetime as date
#FUNCTION classes for the application
from app_functions import AmpFunctions, RoomDesign
from app_constants import AppConstants

class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        ''' Catch and handle the view changes '''
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        action = Distribution()
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            machine_data = """
        Machine Name: %s
        Machine Load: %s
        Machine Section: %s
        Machine Current: %sA
        Machine Current(fx): %sA
        Machine Breaker Size: %sA
        Machine Cable Size: %smm
            """ % (str(rv.data[index]['machine_name']),
            str(rv.data[index]['machine_load']),
            str(rv.data[index]['machine_section']),
            str(rv.data[index]['machine_amp']),
            str(rv.data[index]['machine_amp_gd']),
            str(rv.data[index]['breaker_size']),
            str(rv.data[index]['cable_size']))
            action.popDisplays('Machine Details', machine_data)

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''

#Screens
class LaunchPage(Screen):
    pass
class PowerInputPage(Screen):
    #Instantiate the application class to access global methods
    #Objects referenced from the .KV file
    compTitle = ObjectProperty()
    numSections = ObjectProperty()
    normalVoltage: ObjectProperty()
    growthFactor: ObjectProperty()
    deratingFactor: ObjectProperty()
    dropMachineSection = ObjectProperty()
    dispMachineNumError = ObjectProperty()
    machineName = ObjectProperty()
    machineLoad = ObjectProperty
    machineFactor = ObjectProperty()
    buttAddMachine = ObjectProperty()
    dispMachineListHeader = ObjectProperty()
    dispMachinesList = ObjectProperty()
    dispMachineName = ObjectProperty()
    powerViewboard = ObjectProperty()

    def calculatePowerInputs(self, machines, sections):
        app = Distribution()
        self.machineFactor.text = '0.8'
        if machines:
            if self.dispMachineNumError.text == 'MACHINE PARAMETERS' or self.dispMachineNumError.text == 'Indicate Number of Machines':
                if sections:
                    app.displayInLabelMessage(self.dispMachineNumError, t='MACHINE NUMBER 1', c=[0, 0, 0, 1])
                    self.machineName.text = 'Machine 1'
                    self.buttAddMachine.text = 'Add Machine'
                else:
                    app.displayInLabelMessage(self.dispMachineNumError, t='Indicate Number of Sections', i=True)
            else:
                if sections:
                    app.displayInLabelMessage(self.dispMachineNumError, t='MACHINE NUMBER 1', c=[0, 0, 0, 1])
                    self.machineName.text = 'Machine 1'
                    self.buttAddMachine.text = 'Add Machine'
                else:
                    app.displayInLabelMessage(self.dispMachineNumError, t='Indicate Number of Sections', i=True)
        else:
            app.displayInLabelMessage(self.dispMachineNumError, t='Indicate Number of Machines', i=True)
            #errorMessage = 'Please, Indicate Number of Machines'
            #app.popDisplays('Computing Error', errorMessage)

    def addMachineParameters(self, machines, sections, load, section_selected):
        app = Distribution()
        self.machineFactor.text = '0.8'
        if machines:
            if self.dispMachineNumError.text == 'MACHINE PARAMETERS' or self.dispMachineNumError.text == 'Indicate Number of Machines':
                if sections:
                    app.displayInLabelMessage(self.dispMachineNumError, t='MACHINE NUMBER 1', c=[0, 0, 0, 1])
                    self.machineName.text = 'Machine 1'
                    self.buttAddMachine.text = 'Add Machine'
                else:
                    app.displayInLabelMessage(self.dispMachineNumError, t='Indicate Number of Sections', i=True)
            else:
                if sections:
                    if self.dispMachineNumError.text == 'COMPUTATION ENDED':
                        app.displayInLabelMessage(self.dispMachineNumError, t='COMPUTATION ENDED', i=True)
                        self.machineName.text = ''
                        self.machineFactor.text = ''
                        self.buttAddMachine.text = 'Machines Complete!!!'
                        #completeMessage = 'Machine Computation Completed!!!'
                        #app.popDisplays('Machine Computation', completeMessage)
                    else:
                        if load:
                            if section_selected != 'Select Machine Section':
                                if int(self.dispMachineNumError.text.split()[2]) >= int(machines):
                                    self.machineListLabels()
                                    self.displayPowerViewboard()
                                    app.displayInLabelMessage(self.dispMachineNumError, t='COMPUTATION ENDED', i=True)
                                    self.machineName.text = ''
                                    self.machineLoad.text = ''
                                    self.machineFactor.text = ''
                                    self.dropMachineSection.text = 'Complete!!!'
                                    self.buttAddMachine.text = 'Machines Complete!!!'
                                    #completeMessage = 'Machine Computation Completed!!!'
                                    #app.popDisplays('Machine Computation', completeMessage)
                                else:
                                    self.machineListLabels()
                                    self.displayPowerViewboard()
                                    next_number = self.getMachineNumber(int(self.dispMachineNumError.text.split()[2]), machines)
                                    app.displayInLabelMessage(self.dispMachineNumError, t='MACHINE NUMBER '+str(next_number), c=[0, 0, 0, 1])
                                    self.machineName.text = 'Machine '+str(next_number)
                                    self.buttAddMachine.text = 'Add This Machine '
                                    self.machineLoad.text = ''
                                    self.dropMachineSection.text = 'Select Machine Section'
                                    self.dispMachineListHeader.text = 'List of Machines Added'
                            else:
                                errorMessage = 'Please, Select a Machine Section'
                                app.popDisplays('Inputing Error', errorMessage)
                        else:
                            errorMessage = 'Please, Enter the load of the machine'
                            app.popDisplays('Inputing Error', errorMessage)
                else:
                    app.displayInLabelMessage(self.dispMachineNumError, t='Indicate Number of Sections', i=True)
        else:
            app.displayInLabelMessage(self.dispMachineNumError, t='Indicate Number of Machines', i=True)
            #errorMessage = 'Please, Indicate Number of Machines'
            #app.popDisplays('Computing Error', errorMessage)

    def getMachineNumber(self, a, b):
        if a < int(b)+1:
            return a+1

    def selectMachineSection(self, sections):
        if sections:
            val = []
            for i in range(1, int(sections)+1):
                val.append('Section  '+str(i))
            self.dropMachineSection.values = val
        else:
            self.dropMachineSection.values = []

    def machineListLabels(self):
        ampCal = AmpFunctions(float(self.machineLoad.text),
                            float(self.normalVoltage.text),
                            float(self.growthFactor.text),
                            float(self.deratingFactor.text))
        appCons = AppConstants()
        self.dispMachinesList.data.insert(0, {'machine_name': str(self.machineName.text),
                                                'machine_load': str(self.machineLoad.text),
                                                'machine_section': str(self.dropMachineSection.text),
                                                'machine_amp': str(ampCal.ampWithoutFutureExpansion()),
                                                'machine_amp_gd': str(ampCal.ampWithFutureExpansion()),
                                                'breaker_size': str(appCons.breakerSize(ampCal.ampWithoutFutureExpansion())),
                                                'cable_size': str(appCons.cableSize(ampCal.ampWithoutFutureExpansion()))})

    def displayPowerViewboard(self):
        ampCal = AmpFunctions(float(self.machineLoad.text),
                            float(self.normalVoltage.text),
                            float(self.growthFactor.text),
                            float(self.deratingFactor.text))
        #Determine the total current
        all_currents = []
        for i in self.dispMachinesList.data:
            all_currents.append(float(i['machine_amp']))
        t_current = round(sum(all_currents), 2)

        #Determine the transformer capacity
        p_current = (float(self.normalVoltage.text) * t_current)/float(self.utilityVoltage.text)
        t_capacity =  round((ampCal.phaseRoot() * float(self.utilityVoltage.text) * p_current * 1)/1000, 2)
        power_viewboard_message = """
POWER VIEWBOARD
Total Current from Machines: %sA
Change Over Switch Capacity: 2500A
Transformer Capacity: %skVA
Generator Capacity: %skVA
        """ % (t_current, t_capacity, t_capacity)
        self.powerViewboard.text = power_viewboard_message

class IlluminationPage(Screen):
    lengthOfRoom = ObjectProperty()
    breadthOfRoom = ObjectProperty()
    workingHeight = ObjectProperty()
    wattMSq = ObjectProperty()
    lampL = ObjectProperty()
    numL = ObjectProperty()
    mainFac = ObjectProperty()
    dispIllumination = ObjectProperty()
    dispLampDistributions = ObjectProperty()
    def calculateLampsNeeded(self, length, breadth, w_height, watt_m_sq, lamp_l, no_lumin, main_fac):
        app = Distribution()
        if length and breadth and watt_m_sq and lamp_l:
            if lamp_l != 'Lamp lumen':
                if main_fac != 'Maintenance factor':
                    Ll = AppConstants().lampLumen(str(self.lampL.text))
                    room = RoomDesign(float(self.lengthOfRoom.text),
                                    float(self.breadthOfRoom.text),
                                    float(self.workingHeight.text),
                                    float(self.wattMSq.text),
                                    float(Ll),
                                    float(self.numL.text),
                                    float(self.mainFac.text))
                    if room.utilizationFactor() != 'Not Applicable':
                        message_illumination = """
Room Index Calculated at: %s \r
Total Number of lamps needed: %s
                        """ % (str(room.roomIndex()), str(room.roomLamps()))
                        lamp_dis = """
POSSIBLE COMBINATIONS OF LAMPS\r
%s
                        """ % str(room.possibleLampConfigurations())
                        app.displayInLabelMessage(self.dispIllumination, t=message_illumination, c=[0,0,0,1])
                        app.displayInLabelMessage(self.dispLampDistributions, t=lamp_dis, c=[0,0,0,1])
                    else:
                        er_roomIndex = 'Room Index of '+ str(room.roomIndex())+' is Not Applicable\n\r Adjust your inputs'
                        app.displayInLabelMessage(self.dispIllumination, t=er_roomIndex, i=True)
                else:
                    app.displayInLabelMessage(self.dispIllumination, t='Please select the maintenance factor', i=True)
            else:
                app.displayInLabelMessage(self.dispIllumination, t='Please choose the lamp lumen', i=True)
        else:
            app.displayInLabelMessage(self.dispIllumination, t='Missing Parameter/Input', i=True)


#Main Screen Manager
class DistributionApp(ScreenManager):
    pass
DistributionApplication = Builder.load_file("Distribution.kv")
class Distribution(App):
    def build(self):
        return DistributionApplication

    def displayInLabelMessage(self, obj, **kwargs):
        obj.color = 1, 0, 0, 1
        obj.italic = False
        if kwargs == {}:
            #Default error message
            obj.text = 'Attention: Application Message'
        else:
            for i in kwargs.keys():
                if i == 'text' or i == 't':
                    obj.text = kwargs[i]
                elif i == 'color' or i == 'c':
                    obj.color = kwargs[i]
                elif i == 'italic' or i == 'i':
                    obj.italic = kwargs[i]

    def popDisplays(self, title, message):
        Popup(title=title, title_color=[1,0,0,1],
                content=Label(text=message),
                size_hint=(.5, .4),
                separator_color=[1,1,0,.6]).open()

if __name__ == '__main__':
    Distribution().run()
