# LPSD 4.0 Quality Assurance Testing
Lightning Protection System Designer: Active Repository
Revision 0.3.1

# Contributors
- Greg Martinjak <greg.martinjak@nvent.com>
- Christian Barcey <chris.barcey@nvent.com>
- Andrew Ritosa <andrew.ritosa@nvent.com>

# Summary of Project
The quality testing for LPSD 4.0 confirms the CVM (Collection Volume Method) calculations for LPSD.  Seven test cases are selected to cover the various buildings that LPSD is epected to handle and a CVM model was created for each of these test cases.  The test cases are as follows:
- Rectangular Castle
- Cylindrical Cake
- Tall Apartments
- J-School
- The Last Resort
- Substation
- Gable Roof Catchy Name

These seven test cases cover the vast majority of use cases for LPSD 4.0.
Bug repots and features are kept track in the intranet [Feedback Log](https://nventco.sharepoint.com/sites/Web12/Teams1/EFS/E19_02/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2Fsites%2FWeb12%2FTeams1%2FEFS%2FE19%5F02%2FShared%20Documents%2FUser%20Acceptance%20Testing)

# CVM Summary
Collection Volume Method consists of two primary parts:
- Multiplicativity
- Reductive

These two calculations go into determining a POI's (point of interest) total contribution to the electric field intensification factor (Ki).
- The electric field distribution around a structure is due to the presence of the structure in an ambient electric field, EA. The ambient field is due to the thundercloud charge and, more importantly, to the dynamic field of the approaching downward leader. The normalized value for the field, or the field intensification factor Ki = EP/EA, can be computed at any point P on the structure, including at or near any lightning rods installed on the structure. 
- Models were created so that the problem region was at least five times the size of the structure to be modelled. Dirichlet boundary conditions were applied to the grounded structure, lightning rod and the lower plane boundary (the ground) in the model. These boundaries were all assigned a zero potential, whilst the upper plane boundary of the problem region was assigned a potential such that , in the absence of the structure, a uniform ambient field of magnitude 10 kV/m was created throughout the model region. 
- With the structure present, Laplace’s equation, 𝛻^2 𝑉=0, was solved using the finite element method. This solution provided contours of potential over the problem region. The magnitude of the voltage gradient, 𝐸_𝑃=−𝛻𝑉, was computed from the contour values. Finally, the value of Ki at the required locations (x,y,z) was determined by using 𝐾_𝑖=𝐸_𝑃/𝐸_𝐴. In lightning protection studies, the vertical distribution of the field is of most interest and so, in general, only 𝐾_𝑖 (𝑧) was needed in each particular case.

# Multiplicativity
For features stacked on top of one another, ie. Lift motor rooms on rectangular buildings or air terminals on roof surfaces, the field intensification factors of each element are multiplied together along with a calculated Field Intensification Ratio (FIR) to produce the total multiplicative effects at a given point of interest.

Extended features placed on top of a rectangular, cylindrical or gable-roofed structure
- Used for roof equipment, stairwells, other floors, etc. 
- Intended to be smaller objects on the top of the structure that at most only have slender objects on top of it

Slender objects located on rectangular, cylindrical or gable-roofed structures
- Used for air terminals, masts, flagpoles, etc.
- Objects can be placed on the ground, directly on roofs, or on extended features on roofs
- Slender objects are described as have a “slenderness ratio”,  𝐻/𝑊>50

# Reduction
For complete independence of the fields due to two “isolated” structures, the minimum distance between them is a positive power function of the height and width of the taller structure. For adjoined structures, the taller structures reduces the field around the lower structure as a positive power of the height difference and a negative power of the width of the lower structure. 

The latter result is easily understood in terms of the field at the most distant edges and corners of the lower structure-the further these are away from the taller structure, the less is the degree of shielding. For non-adjoined structures, but those in close proximity (inside the minimum distance), the width relation described above can be replaced by an equivalent distance.

A reduction factor, 𝑹_𝒇, is calculated based on the position of shorter structures being in proximity of taller structures or composite structures with multiple roof levels. This reduction factor is applied to the 𝑲_𝒊 of the lower structure.

For example, the total reductive effects of a rectangular structure on a lower POI is:

𝐾_𝑖=(𝐾_𝑖 (𝑃𝑂𝐼 @ 𝑧))/(𝑅_𝑓 (𝐻_1,𝐻_2,𝑊_2))

# Project Progress

| Test Case #  | Reductive | Multiplicative |
| ------------- | ------------- | ------------- |
| Test Case 1  | ![Test case 1](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%201/TC1_Reductive_Chart.png?raw=true)  |![Test case 1](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%201/TC1_Multiplicative_Chart.png?raw=true)
| Test Case 2  | ![Test case 2](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%202/TC2_Reductive_Chart.png?raw=true)  |![Test case 2](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%202/TC2_Multiplicative_Chart.png?raw=true)
| Test Case 3  | ![Test case 3](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%203/TC3_Reductive_Chart.png?raw=true)  |![Test case 3](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%203/TC3_Multiplicative_Chart.png?raw=true)
| Test Case 4  | ![Test case 4](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%204/TC4_Reductive_Chart.png?raw=true)  |![Test case 4](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%204/TC4_Multiplicative_Chart.png?raw=true)
| Test Case 5  | ![Test case 5](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%205/TC5_Reductive_Chart.png?raw=true)  |![Test case 5](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%205/TC5_Multiplicative_Chart.png?raw=true)
| Test Case 6  | ![Test case 6](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%206/TC6_Reductive_Chart.png?raw=true)  |![Test case 6](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%206/TC6_Multiplicative_Chart.png?raw=true)
| Test Case 7  | ![Test case 7](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%207/TC7_Completion_Chart.png?raw=true)  |![Test case 7](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%207/TC7_Multiplicative_Chart.png?raw=true)

# Project Schedule
```
11.03 Open issues:
```
<b>minWidth</b>
- Found major bug with determining minWidth that prevents proper multiplicative calculations
- Reached out to ASTI/Graitec and asked for a phone call

<b>Test Case 6F</b>
- Multiplicative calculation issue resolved
- minWidth issue opened

```
11.02 Open issues:
```
<b>Test Case 6F</b>
- .JSON file received and analyzed
- Reductive and multiplicative charts to be created
- Issue with Greg's multiplicative calculation needs to be resolved

<b>Issues 194</b>

- Carlo wants to look into this more
- Graitec was added to the project

<b>Issue 199</b>

- Graitec/ASTI explained that if you zoom in, you can see that the ridge-line to the left of the terminal is showing red
- Root cause found to be that POIs were not placed in the proper locations
- End result was confirmed

<b>Multiplicative General</b>
- Greg working on resolving code issues in calculating Multiplicative on our side

<b>Other</b>
- Graitec/ASTI working on new update

```
10.27 Open issues:
```
<b>Test Case 6F</b>
- Carlo provided new code to allow for TC6F to run
- TC6F has been ran and I need to request JSON file from Carlo

<b>Layer Visibility</b>
- This issue appears resolved as of last push

<b>Multiplicative</b>
- Greg has worked through all multiplicative values from JSON files on TC1-TC7 excluding 6
- There appears to be some issues on TC7 with the multiplicative flowchart
- There appears to be some issues on TC2 with the cylindrical calculations
```
10.26 Open issues:
```
<b>Test Case 6F</b>
- Model is uploaded and active
- POIs are placed on model
- Model is analyzed
- Analysis is not correct and needs attention
- Email sent to Carlo explaining the issue
- Carlo hasn't looked at the air terminals not providing a CV

<b>Layer Visibility</b>
- Carlo figured out a primary issue for layers bypassing the visibility toggle when regenerating
- The issue is expected to be resolved by 11.02

<b>Multiplicative</b>
- Greg is working through multiplicative analysis of all test cases
- All multiplicative test cases are expected to be analyzed by end of this week