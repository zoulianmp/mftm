{
   "3DElementsSet": [
      {
         "EleName": "Out", 
         "GeneralParams": {
            "Density": 1.0, 
            "Priority": 0.0, 
            "RelEDensity": 1.0, 
            "TissueType": "G4_WATER"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            10.0, 
            10.0, 
            10.0
         ], 
         "GeometryParams": {
            "GeoType": "Cube", 
            "InitialParams": [
               0.0, 
               0.0, 
               0.0, 
               30.0, 
               30.0, 
               30.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.0, 
               0.0, 
               1.0
            ], 
            "Opacity": 0.2656, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "in1", 
         "GeneralParams": {
            "Density": 0.1, 
            "Priority": 1.0, 
            "RelEDensity": 0.001, 
            "TissueType": "G4_AIR"
         }, 
         "GeoTunerParams": [
            0.0, 
            -12.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            10.0, 
            10.0, 
            10.0
         ], 
         "GeometryParams": {
            "GeoType": "Cube", 
            "InitialParams": [
               -12.0, 
               0.0, 
               0.0, 
               4.0, 
               4.0, 
               4.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.1, 
               0.5, 
               0.3
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "in2", 
         "GeneralParams": {
            "Density": 1.31, 
            "Priority": 2.0, 
            "RelEDensity": 0.19, 
            "TissueType": "G4_BORON_CARBIDE"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            10.0, 
            10.0, 
            10.0
         ], 
         "GeometryParams": {
            "GeoType": "Cube", 
            "InitialParams": [
               -4.0, 
               -12.0, 
               0.0, 
               4.0, 
               4.0, 
               4.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.3, 
               0.5, 
               0.3
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "in3", 
         "GeneralParams": {
            "Density": 0.5, 
            "Priority": 2.4, 
            "RelEDensity": 0.489, 
            "TissueType": "G4_LUNG_ICRP"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            10.0, 
            10.0, 
            10.0
         ], 
         "GeometryParams": {
            "GeoType": "Cube", 
            "InitialParams": [
               4.0, 
               -12.0, 
               0.0, 
               4.0, 
               4.0, 
               4.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.1, 
               0.5, 
               0.3
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "in4", 
         "GeneralParams": {
            "Density": 0.96, 
            "Priority": 3.0, 
            "RelEDensity": 0.926, 
            "TissueType": "G4_ADIPOSE_TISSUE_ICRP"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            10.0, 
            10.0, 
            10.0
         ], 
         "GeometryParams": {
            "GeoType": "Cube", 
            "InitialParams": [
               4.0, 
               -4.0, 
               0.0, 
               4.0, 
               4.0, 
               4.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.2, 
               0.5, 
               0.3
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "in5", 
         "GeneralParams": {
            "Density": 0.99, 
            "Priority": 4.7, 
            "RelEDensity": 0.976, 
            "TissueType": "G4_BRAIN_ICRP"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            10.0, 
            10.0, 
            10.0
         ], 
         "GeometryParams": {
            "GeoType": "Cube", 
            "InitialParams": [
               4.0, 
               4.0, 
               0.0, 
               4.0, 
               4.0, 
               4.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.4, 
               0.5, 
               0.3
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }
   ], 
   "CurrentElementIndex": [
      0, 
      1
   ], 
   "MaterialList": "\\g4_validat_material_list.txt", 
   "Name": "3DVirtualPhantom", 
   "Type": "3DPhantom"
}