{
   "3DElementsSet": [
      {
         "EleName": "Body", 
         "GeneralParams": {
		    "Density": 1.0, 
            "Priority": 0.0, 
            "RelEDensity": 1.0, 
            "TissueType": "Water"
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
            "GeoType": "Cylinder", 
            "InitialParams": [
               0.0, 
               0.0, 
               0.0, 
               150.0, 
               50.0, 
               80
            ]
         }, 
         "VisParams": {
            "Color": [
               0.0, 
               0.0, 
               1.0
            ], 
            "Opacity": 0.2344, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "vtkin", 
         "GeneralParams": {
		    "Density": 0.99, 
            "Priority": 1.875, 
            "RelEDensity": 0.976, 
            "TissueType": "BreastTissue"
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
            "GeoType": "VTKExternalFile", 
            "InitialParams": [
               "\\VTK\\H&N\\left_eyeball.vtk"
            ]
         }, 
         "VisParams": {
            "Color": [
               0.86, 
               0.16, 
               0.16
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "stlin", 
         "GeneralParams": {
		    "Density": 1.08, 
            "Priority": 3.75, 
            "RelEDensity": 1.031, 
            "TissueType": "StraitedMuscle"
         }, 
         "GeoTunerParams": [
            -70.0, 
            -50.0, 
            -80.0, 
            0.0, 
            0.0, 
            0.0, 
            0.3, 
            0.3, 
            0.3
         ], 
         "GeometryParams": {
            "GeoType": "STLExternalFile", 
            "InitialParams": [
               "\\STL\\Cstick.STL"
            ]
         }, 
         "VisParams": {
            "Color": [
               1.0, 
               0.5, 
               0.0
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }
   ], 
   "CurrentElementIndex": [
      0, 
      2
   ], 
   "MaterialList": "\\default_material_list.txt", 
   "Name": "3DVirtualPhantom", 
   "Type": "3DPhantom"
}