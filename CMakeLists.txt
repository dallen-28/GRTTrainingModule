cmake_minimum_required(VERSION 3.5)

project(GestureRecognition)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/GestureRecognition")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Daniel Allen (Robarts Research Institute)")
set(EXTENSION_DESCRIPTION "Gesture Recognition For Leap Motion and other devices")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/GestureRecognition.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/GestureRecognition/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(GestureRecognition)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
