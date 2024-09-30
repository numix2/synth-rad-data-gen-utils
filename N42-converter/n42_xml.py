import xml.etree.ElementTree as ET
from enum import Enum
#import pprint

#########################################
# Enums
#########################################

class _RadInstrumentClassCode(Enum):
    """Enum class, implements the N42 standard's RadInstrumentClassCode field.
    """
    BACKPAK = "Backpack or Personal Radiation Scanner"
    DOSIMETER = "Dosimeter"
    EPERD = "Electronic Personal Emergency Radiation Detector"
    MOBILE = "Moblie System"
    NAM = "Network Area Monitor"
    NEUTRON_HH = "Neutron Handheld"
    PRD = "Personal Radiation Detector"
    RI = "Radionuclide Identifier"
    PM = "Portal Monitor"
    SPM = "Spectroscopic Portal Monitor"
    SPRD = "Spectroscopic Personal Radiation Detector"
    GAMMA_HH = "Gamma Handheld"
    TS = "Transportable System"
    OTHER = "Other"

class _RadDetectorCategoryCode(Enum):
    """Enum class, implement the N42 standard's RadDetectorCategoryCode field.
    """
    GAMMA = "Gamma"
    NEUTRON = "Neutron"
    ALPHA = "Alpha"
    BETA = "Beta"
    X_RAY = "X-ray"
    OTHER = "Other"

class _RadMeasurementClassCode(Enum):
    FOREGROUND = "Foreground"
    BACKGROUND = "Background"
    CALIBRATION = "Calibration"
    INTRIN_ACT = "IntrinsicActivity"
    NOT_SPEC = "NotSpecified"

#########################################
# Private functions
#########################################
def _build_Spectrum(reading, live_time_dur, energy_bin, unit, i, RadInstrumentData) -> ET.Element:
    """ Helper funtion for _build_RadMeasurement(): It assembles the Spectrum XML subtree,
    and the EnergyCalibration subtree.
    @reading: the measured values
    @i: the iterating number, for id creation
    @RadInstrumentData: Pointer to the root object of the XML tree.
    It is reqired, becouse the EnergyCalibration element is a sub-element 
    of the RadInstrumentData element, not the RadMeasurement.
    """
    if energy_bin is not None:
        energy_bin = str(energy_bin)
    count = reading

    ec_x: str = "ec" + str(i)
    EnergyCalibration = ET.Element("EnergyCalibration", {"id":ec_x})
    EnergyValues = ET.Element("EnergyValues")
    if unit is not None:
        EnergyValues.text = unit
    else:
        EnergyValues.text = "1keV"
    EnergyCalibration.append(EnergyValues)
    RadInstrumentData.append(EnergyCalibration)

    s_x: str = "s" + str(i)
    Spectrum = ET.Element("Spectrum", {"id":s_x, "EnergyCalibrationReference": ec_x})

    LiveTimeDuration = ET.Element("LiveTimeDuration")
    if live_time_dur is not None:
        LiveTimeDuration.text = str(live_time_dur)
    else:
        LiveTimeDuration.text = "Not Given"
    Spectrum.append(LiveTimeDuration)

    ChannelData = ET.Element("ChannelData")
    ChannelData.text = " ".join(map(str, count))
    Spectrum.append(ChannelData)

    return Spectrum


def _build_DoseRate(reading, i, unit) -> ET.Element:
    """ Helper function for _build_RadMeasurment(): It assembles the DoseRate XML subtree.
    @reading: The measured value
    @i: The iterating number, for id generation
    @return: returns the XML subtree for DoseRate
    """
    dr_x: str = "dr" + str(i)
    DoseRate = ET.Element("DoseRate", {"id": dr_x, "radDetectorInformationReference": "rdi"})
    
    if unit == None: 
        DoseRateValue = ET.Element("DoseRateValue", {"units": "uSv/h"})
    else:
        DoseRateValue = ET.Element("DoseRateValue", {"units": unit})
    DoseRateValue.text = str(reading)
    DoseRate.append(DoseRateValue)
    
    return DoseRate

def _build_RadInstrumentState(loc_lat, loc_lon) -> ET.Element:
    """ Helper function for _build_RadMeasurement(). This function assembles the RadMeasurmenetState XML subtree
    @loc_lat: locational latitude coordinate
    @loc_lon: locational longitude coordinate
    @return: Returns the XML subtree for RadInstrumentState
    """
    RadInstrumentState = ET.Element("RadInstrumentState", {"radInstrumentInformationReference":"rii"})

    StateVector = ET.Element("StateVector")
    GeographycPoint = ET.Element("GeographycPoint")
    LatitudeValue = ET.Element("LatitudeValue")
    LatitudeValue.text = str(loc_lat)
    LongitudeValue = ET.Element("LongitudeValue")
    LongitudeValue.text = str(loc_lon)
    GeographycPoint.append(LatitudeValue)
    GeographycPoint.append(LongitudeValue)
    StateVector.append(GeographycPoint)
    RadInstrumentState.append(StateVector)

    return RadInstrumentState


def _build_RadMeasurement(when_captured,
                          mes_type,
                          reading,
                          i,
                          RadInstrumentData,
                          loc_lat,
                          loc_lon,
                          real_time_dur,
                          live_time_dur,
                          energy_bin,
                          unit
                          ) -> ET.Element:
    """ Takes information from the input data, and build the RadMeasurement subtree from it.
    @when_captured: The captured date
    @loc_lat: locational latitude coordinate
    @loc_lon: locational longitude coordinate
    @mes_type: the type of the measurement (for example: spectrum)
    @reading: the maesured value
    @i: The iterating number, for id creation
    @RadInstrumentData: Pointer to the root of the XML tree, 
    for if @mes_type = Spectrum: so that the EnergyCalibration subtree can be appended to it.
    @return: Returns the assembled RadInstrumentInformation XML subtree
    """
    rm_x: str = "rm" + str(i)
    RadMeasurement = ET.Element("RadMeasurement", {"id":rm_x})
    MeasurementClassCode = ET.Element("MeasurementClassCode")
    MeasurementClassCode.text = _RadMeasurementClassCode.BACKGROUND.value
    RadMeasurement.append(MeasurementClassCode)
    StartDateTime = ET.Element("StartDateTime")
    StartDateTime.text = when_captured
    RadMeasurement.append(StartDateTime)
    RealTimeDuration = ET.Element("RealTimeDuration")
    if real_time_dur is not None:
        RealTimeDuration.text = str(real_time_dur)
    else:
        RealTimeDuration.text = "Not given"
    RadMeasurement.append(RealTimeDuration)
    if loc_lat != None and loc_lon != None:
        RadInstrumentState = _build_RadInstrumentState(loc_lat, loc_lon)
        RadMeasurement.append(RadInstrumentState)
    if mes_type != "spectrum":
        DoseRate = _build_DoseRate(reading, i, unit)
        RadMeasurement.append(DoseRate)
    else:
        RadMeasurement.append(_build_Spectrum(reading, live_time_dur, energy_bin, unit, i, RadInstrumentData))

    return RadMeasurement


#-----------------------------------------------------------------------
def _build_RadDetectorInformation(type: str) -> ET.Element:
    """ Takes the device information from the input data,
    and build the RadDetectorInformation subtree from it.
    @device: The device name
    @return: Returns the assembled RadDetectorInformation XML subtree
    """
    RadDetectorInformation = ET.Element("RadDetectorInformation", {"id": "rdi"})

    RadDetectorCategoryCode = ET.Element("RadDetectorCategoryCode")
    if type == "bg_rad":
        RadDetectorCategoryCode.text = _RadDetectorCategoryCode.GAMMA.value
    if type == "bg_cnt":
        RadDetectorCategoryCode.text = _RadDetectorCategoryCode.OTHER.value
    if type == "neutron":
        RadDetectorCategoryCode.text = _RadDetectorCategoryCode.NEUTRON.value
    if type == "spectrum":
        RadDetectorCategoryCode.text = _RadDetectorCategoryCode.OTHER.valueue
    RadDetectorInformation.append(RadDetectorCategoryCode)

    return RadDetectorInformation

#-------------------------------------------------------------------------
def _build_RadInstrumentInformation(device: str) -> ET.Element:
    """ Takes the device information from the input data, 
    and build the RadInstrumentInformation subtree from it.
    @device: The name of the device
    @return: Returns the assembled RadInstrumentInformation XML subtree
    """
    RadInstrumentInformation = ET.Element("RadInstrumentInformation", {"id": "rii"})
    
    RadInstrumentManufaturerName = ET.Element("RadInstrumentManufacturerName")
    RadInstrumentManufaturerName.text = device
    RadInstrumentInformation.append(RadInstrumentManufaturerName)
    
    RadInstrumentModelName = ET.Element("RadInstrumentModelName")
    RadInstrumentModelName.text = device
    RadInstrumentInformation.append(RadInstrumentModelName)

    RadInstrumentClassCode = ET.Element("RadInstrumentClassCode")
    RadInstrumentClassCode.text = _RadInstrumentClassCode.OTHER.value
    RadInstrumentInformation.append(RadInstrumentClassCode)

    RadInstrumentVersion = ET.Element("RadInstrumentVersion")
    RadInstrumentComponentName = ET.Element("RadInstrumentComponentName")
    RadInstrumentComponentName.text = device
    RadInstrumentComponentVersion = ET.Element("RadInstrumentComponentVersion")
    RadInstrumentComponentVersion.text = device
    RadInstrumentVersion.append(RadInstrumentComponentName)
    RadInstrumentVersion.append(RadInstrumentComponentVersion)
    RadInstrumentInformation.append(RadInstrumentVersion)

    return RadInstrumentInformation

def _build_RadInstrumentData(processed_data: dict, device_name: str) -> ET.Element:
    """ Takes the data from @parsed_json file and distributes
    it amongst the different subtree builder functions.
    @processed_json: A dictionary of lists with the data from a JSON file for one device
    @device_name: the key for the processed_data
    @return: An ET.Element. This will be the root of the output XML
    """
    RadInstrumentData = ET.Element("RadInstrumentData")
    RadInstrumentInformation = _build_RadInstrumentInformation(device_name)
    RadInstrumentData.append(RadInstrumentInformation)
    RadDetectorInformation = _build_RadDetectorInformation(processed_data["type"])
    RadInstrumentData.append(RadDetectorInformation)
    for i, _ in enumerate(processed_data["when_captured"]):
        RadMeasurement = _build_RadMeasurement(processed_data["when_captured"][i], 
                                               processed_data["type"][i],
                                               processed_data["reading"][i],
                                               i,
                                               RadInstrumentData, # for spectrum info to be added
                                               processed_data["loc_lat"][i], 
                                               processed_data["loc_lon"][i],
                                               processed_data["real_time_dur"][i],
                                               processed_data["live_time_dur"][i],
                                               processed_data["energy_bin"][i],
                                               processed_data["unit"][i])
        RadInstrumentData.append(RadMeasurement)
    return RadInstrumentData

#---------------------------------------------------------------------------------

def pre_processing(parsed_json: dict[list]) -> dict[dict[list]]:
    """Takes the dictionary of lists from the parsed JSON file, 
    and creats from it anohter sturcture like this:
    The new structure is a dictionary, which's keys are all the unique 
    values of the original structure's "device" list. 
    
    These keys than get for their values all the other data from the
    JSON file that has been gathered by the device designated by the key.

    This makes it possible to create separate N42 XML files for every device 
    found in the single JSON.
    @parsed_json: a dictionary of lists where the keys are the different 
    fields of the JSON file, and the lists are all the datapoints associated with that field
    @return: The function returns the same data, but structured in a way that the datapoints
    are sorted by the different devices.
    """
    devices: list = parsed_json["device"]
    unique_devices = set(devices)

    data_by_device = {}

    for u_dev in unique_devices:
        data_by_device[u_dev] = {}
        data_by_device[u_dev]["when_captured"] = []
        data_by_device[u_dev]["device"] = []
        data_by_device[u_dev]["loc_lat"] = []
        data_by_device[u_dev]["loc_lon"] = []
        data_by_device[u_dev]["type"] = []
        data_by_device[u_dev]["reading"] = []
        data_by_device[u_dev]["real_time_dur"] = []
        data_by_device[u_dev]["live_time_dur"] = []
        data_by_device[u_dev]["energy_bin"] = []
        data_by_device[u_dev]["unit"] = []
        for i, curr_dev in enumerate(devices):
            if u_dev == curr_dev:
                data_by_device[u_dev]["when_captured"].append(parsed_json["when_captured"][i])
                data_by_device[u_dev]["device"].append(parsed_json["device"][i])
                data_by_device[u_dev]["loc_lat"].append(parsed_json["loc_lat"][i])
                data_by_device[u_dev]["loc_lon"].append(parsed_json["loc_lon"][i])
                data_by_device[u_dev]["type"].append(parsed_json["type"][i])
                data_by_device[u_dev]["reading"].append(parsed_json["reading"][i])
                data_by_device[u_dev]["real_time_dur"].append(parsed_json["real_time"][i])
                data_by_device[u_dev]["live_time_dur"].append(parsed_json["live_time"][i])
                data_by_device[u_dev]["energy_bin"].append(parsed_json["energy_bin"][i])
                data_by_device[u_dev]["unit"].append(parsed_json["unit"][i])
    #pprint.pprint(data_by_device)
    return data_by_device



#####################################
# Public functions
#####################################

def create_N42(parsed_json: dict) -> dict[ET.ElementTree]:
    """Takes the input JSON file and creates from it one or more N42 format XML files
    @param input: A dictionary with all the data from a json file
    """
    
    roots: dict[ET.Element] = {}
    processed_data = pre_processing(parsed_json)
    
    for device_name in processed_data:
        roots[device_name] = _build_RadInstrumentData(processed_data[device_name], device_name)

    trees: dict[ET.ElementTree] = {}
    for root in roots:
        tree = ET.ElementTree(roots[root])
        ET.indent(tree, '\t', level=0)
        trees[root] = tree
    
    return trees

def write(xml_out: dict[ET.ElementTree], path: str) -> None:
    """Take the input xml structure and writes it to the file specified in output
    Takes a dict of XML ElementTrees and for each key it creates 
    a file with name <key>.xml at the location specified by path
    @param xml_out: Dictionary of ElementTree objects
    @param path: the filepath where the files are to be written
    """

    for key in xml_out:
        xml_out[key].write(path + '/' + str(key) + ".xml")
