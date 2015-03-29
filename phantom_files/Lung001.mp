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
            90.0, 
            0.0, 
            0.0, 
            1.0, 
            0.7, 
            1.0
         ], 
         "GeometryParams": {
            "GeoType": "Cylinder", 
            "InitialParams": [
               0.0, 
               0.0, 
               0.0, 
               250.0, 
               150.0, 
               80
            ]
         }, 
         "VisParams": {
            "Color": [
               0.0, 
               0.0, 
               1.0
            ], 
            "Opacity": 0.1473, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "LeftLung", 
         "GeneralParams": {
		    "Density": 0.46, 
            "Priority": 3.69, 
            "RelEDensity": 0.294, 
            "TissueType": "Lung"
         }, 
         "GeoTunerParams": [
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.75, 
            0.75, 
            1.2
         ], 
         "GeometryParams": {
            "GeoType": "Sphere", 
            "InitialParams": [
               70.0, 
               -80.0, 
               0.0, 
               0.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.7529, 
               0.7529, 
               0.7529
            ], 
            "Opacity": 0.2326, 
            "Representation": "surface", 
            "Visibility": true
         }
      }, 
      {
         "EleName": "SpinalCord", 
         "GeneralParams": {
		    "Density": 1.62, 
            "Priority": 2.6550000000000002, 
            "RelEDensity": 1.506, 
            "TissueType": "Bone"
         }, 
         "GeoTunerParams": [
            10.0, 
            0.0, 
            70.0, 
            90.0, 
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
               250.0, 
               10.0, 
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
         "EleName": "RightLung", 
         "GeneralParams": {
		    "Density": 0.46, 
            "Priority": 4.6899999999999995, 
            "RelEDensity": 0.294, 
            "TissueType": "Lung"
         }, 
         "GeoTunerParams": [
            85.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            1.0, 
            1.0, 
            1.5
         ], 
         "GeometryParams": {
            "GeoType": "Sphere", 
            "InitialParams": [
               50.0, 
               0.0, 
               0.0, 
               0.0
            ]
         }, 
         "VisParams": {
            "Color": [
               0.7529, 
               0.7529, 
               0.7529
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
   "MaterialList": "\\default_material_list.txt", 
   "Name": "Lung001", 
   "Type": "3DPhantom"
}