{
   "3DElementsSet": [
      {
         "EleName": "in", 
         "GeneralParams": {
            "Density": 0.1, 
            "Priority": 1.0, 
            "RelEDensity": 0.001, 
            "TissueType": "G4_AIR"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            1.0, 
            1.0, 
            1.0
         ], 
         "GeometryParams": {
            "GeoType": "Sphere", 
            "InitialParams": [
               30.0, 
               0.0, 
               0.0, 
               0.0
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
         "EleName": "out", 
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
            1.0, 
            1.0, 
            1.0
         ], 
         "GeometryParams": {
            "GeoType": "Cube", 
            "InitialParams": [
               0.0, 
               0.0, 
               0.0, 
               65.0, 
               65.0, 
               65.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.0, 
               0.0, 
               1.0
            ], 
            "Opacity": 0.5, 
            "Representation": "surface", 
            "Visibility": true
         }
      }
   ], 
   "CurrentElementIndex": [
      0, 
      0
   ], 
   "MaterialList": "\\g4_material_list.txt", 
   "Name": "3DVirtualPhantom", 
   "Type": "3DPhantom"
}