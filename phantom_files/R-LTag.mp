{
   "3DElementsSet": [
      {
         "EleName": "Body", 
         "GeneralParams": {
		    "Density": 1.0, 
            "Priority": 1.0, 
            "RelEDensity": 1.0, 
            "TissueType": "Water"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            0.0, 
            90.0, 
            0.0, 
            0.0, 
            8.0, 
            8.0, 
            8.0
         ], 
         "GeometryParams": {
            "GeoType": "Cylinder", 
            "InitialParams": [
               0.0, 
               0.0, 
               0.0, 
               30.0, 
               15.0, 
               80
            ]
         }, 
         "VisParams": {
            "Color": [
               0.0, 
               0.0, 
               1.0
            ], 
            "Opacity": 0.8, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "Head", 
         "GeneralParams": {
		    "Density": 1.0, 
            "Priority": 1.3, 
            "RelEDensity": 1.0, 
            "TissueType": "Water"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            25.0, 
            0.0, 
            0.0, 
            0.0, 
            4.0, 
            4.0, 
            4.0
         ], 
         "GeometryParams": {
            "GeoType": "Sphere", 
            "InitialParams": [
               15.0, 
               0.0, 
               0.0, 
               10.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.0, 
               0.0, 
               1.0
            ], 
            "Opacity": 0.7, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "Nodes", 
         "GeneralParams": {
		    "Density": 1.62, 
            "Priority": 1.12, 
            "RelEDensity": 1.506, 
            "TissueType": "Bone"
         }, 
         "GeoTunerParams": [
            7.0, 
            0.0, 
            20.0, 
            0.0, 
            0.0, 
            90.0, 
            8.0, 
            8.0, 
            8.0
         ], 
         "GeometryParams": {
            "GeoType": "Cone", 
            "InitialParams": [
               30.0, 
               0.0, 
               0.0, 
               0.0, 
               1.0, 
               0.0, 
               0.0, 
               8.0, 
               4.0, 
               80
            ]
         }, 
         "VisParams": {
            "Color": [
               0.9412, 
               1.0, 
               0.9412
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "Foot", 
         "GeneralParams": {
		    "Density": 1.16, 
            "Priority": 0.7, 
            "RelEDensity": 1.117, 
            "TissueType": "SolidTrabecularBone"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            -27.0, 
            0.0, 
            0.0, 
            0.0, 
            5.6, 
            5.6, 
            4.8
         ], 
         "GeometryParams": {
            "GeoType": "Cube", 
            "InitialParams": [
               0.0, 
               0.0, 
               0.0, 
               20.0, 
               20.0, 
               35.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.9608, 
               1.0, 
               0.9804
            ], 
            "Opacity": 1.0, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "Rflag", 
         "GeneralParams": {
		    "Density": 1.08, 
            "Priority": 0.3, 
            "RelEDensity": 1.031, 
            "TissueType": "StraitedMuscle"
         }, 
         "GeoTunerParams": [
            35.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            3.2, 
            3.2, 
            2.4
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
      4
   ], 
   "MaterialList": "\\default_material_list.txt", 
   "Name": "R-LTag", 
   "Type": "3DPhantom"
}