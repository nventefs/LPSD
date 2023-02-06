# LPSD 4.0 Quality Assurance Testing
Lightning Protection System Designer: Active Repository
Revision 0.3.1

# Contributors
- Greg Martinjak <greg.martinjak@nvent.com>
- Christian Barcey <chris.barcey@nvent.com>
- Andrew Ritosa <andrew.ritosa@nvent.com>

# Summary of Project
The quality testing for LPSD 4.0 confirms the CVM (Collection Volume Method) calculations for LPSD.  Seven test cases are selected to cover the various buildings that LPSD is expected to handle and a CVM model was created for each of these test cases.  The test cases are as follows:

- Rectangular Castle
- Cylindrical Cake
- Tall Apartments
- J-School
- The Last Resort
- Substation
- Gable Roof Catchy Name

These seven test cases cover the vast majority of use cases for LPSD 4.0.
Bug reports and features are kept track of within the intranet [Feedback Log](https://nventco.sharepoint.com/sites/Web12/Teams1/EFS/E19_02/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2Fsites%2FWeb12%2FTeams1%2FEFS%2FE19%5F02%2FShared%20Documents%2FUser%20Acceptance%20Testing)

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
| Test Case 7  | ![Test case 7](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%207/TC7_Reductive_Chart.png?raw=true)  |![Test case 7](https://github.com/nventefs/LPSD/blob/main/Test%20Case%20-%207/TC7_Multiplicative_Chart.png?raw=true)

# Project Schedule


<details>
  <summary><b>02.06 Open issues:</b></summary>

### Multiplicative - Test Case 7
- Determined two different formulas for passing height of a point to equation F
- Will need to determine which approach is the correct approach for passing height through to point F
- Determined incorrect application of Height to Equation F in excel spreadsheet where it utilized equation B which uses a different height

### Rolling Sphere Method Improper Calculation
- Verified that the calculations in the use-case that Ruud provided are correct
- Will need to ask for an additional use-case where the calculations are not correct to continue investigating this issue

</details>

<details>
  <summary><b>01.11 Open issues:</b></summary>
  
### Reductive/Multiplicative
- Reductive report completed and reviewed briefly with Graitec/ASTI
- Report to be sent for final approval
- Multiplicative report on-hold until bug fixes with multiplicative TC5, TC7
- TC6 multiplicative analysis needs updated code for multiple building influence calculations
- TC6 multiplicative analysis is currently being done manually in excel and may not be required for code updates
- Updated flowchart for multiplicative for gable roofs, finishing up some analysis before scheduling a meeting with Carlo & Ron to review

### Production SFDC issue
- We implemented suggested change but no change to SFDC//LPSD interaction

### Air terminal verification
- Code pushed to production, issue resolved

</details>

<details>
  <summary><b>12.14 Open issues:</b></summary>
  
### Reductive/Multiplicative
- Reductive report completed and reviewed briefly with Graitec/ASTI
- Report to be sent for final approval
- Multiplicative report on-hold until bug fixes with multiplicative TC5, TC7
- TC6 multiplicative analysis needs updated code for multiple building influence calculations
- TC6 multiplicative analysis is currently being done manually in excel and may not be required for code updates

### Air terminal verification
- Code pushed to production, issue resolved

</details>

<details>
  <summary><b>12.07 Open issues:</b></summary>

### Reductive/Multiplicative
- Reductive report completed and approved by nVent
- Multiplicative report in process
- Awaiting push for correction on extended points with awnings underneath
- Multiplicative report to be finalized after push and sent out for approval

### Air terminal verification
- Last step is to verify angle of protection and other air terminal values to finalize S3000 and provide approval for production

</details>

<details>
  <summary><b>11.30 Open issues:</b></summary>

### Reductive/Multiplicative
- Looks good at first glance
- Reductive report update by end of week
- Multiplicative review within 3 weeks

### Issue 204
- Issue resolved, the issue was a local hardware issue (Laptop non-functional)

## Other
- Bug in pulling in new components into the revit family folder
- Found components, terminals, bases that were unable to be found before

### Debug prompt
- Carlo implemented a debug prompt allowing for json data to be pulled instantly by the user
- CTRL+ALT+Q is the hotkey to get to the debug prompt

</details>
<details>
  <summary><b>11.29 Open issues:</b></summary>

### Minimum Width
- Carlo fixed minimum width calculations and verified every level for each project
- Carlo applied the proper sublevels to the seven test cases 

### Reductive/Multiplicative
- Ran through results from .json files sent by Carlo
- As a cursory glance there appears to be additional issues from the changes made that will need to be evaluated

</details>

<details>
  <summary><b>11.17 Open issues:</b></summary>

### Issue 193 [Feature]
- Meeting with Matt and Ruud to begin scope document
- Ruud to take the lead on determining the design guidelines per IEC 62305

### Issue 194
- Unable to acquire project # at the moment since LPSD login is down

### Issue 196 [Feature]
- Matt leading the design requirements for the metric template
- Scope document in progress

</details>

<details>
  <summary><b>11.16 Open issues:</b></summary>

### Issue 193 [Feature]
- Angle protection is resolved when using terminals, mesh protection is not resolved
- No analysis results on mesh when no terminals are used
- Angle protection is not resolved when not using terminals
- Mesh method was never setup for use with POIs
- Need to create SOW to add Mesh method analysis with the use of POIs
- The same analysis method should be included to the SOW for angle protection

### Issue 194 
- Ruud to send project # to Carlo for review
- Greg to send feedback log file to Carlo and highlight issue 194

### Issue 203 [Feature]
- Flyout sets default
- The initial settings greatly impact the analysis of the model
- SOW to be created to add a button/functionality 
- Hotfix to use new option functionality to change the analysis method

### minWidth
- Analyze form tool spheres need to be assigned to a level
- Vertical points will have levels again
- Boundary conditions will look for POIs at z<level_z

### User roles
- Role comes from BIM360
- Region will assign people to projects by default based on region
- Administrator role controls access in BIM360
- The role for external administrator doesn't exist
- The template does allow for various restrictions in BIM360
- "Customized Administrator Role"
- Logging in with Autodesk ID allows for restrictions

</details>

<details>
  <summary><b>11.13 Open issues:</b></summary>

    ### minWidth
    - Carlo sent a fix for minWidth including Test Case 2 with a fail-safe catch for infinite loops on the forge side
    - New minWidth issue found where levels are not including bounding boxes of levels above
    - Had phone call with Carlo and Ron to determine root cause and look at fixes
    - Possible issue with Equation 3: B or Equation 5: L
</details>

<details>
  <summary><b>11.11 Open issues:</b></summary>

### minWidth
- Carlo sent a fix for minWidth excluding Test Case 2 where there is a risk of an infinite loop

</details>
<details>
  <summary><b>11.09 Open issues:</b></summary>

### minWidth
- Carlo will determine next steps with minWidth

### Test Case 6F
- Reductive calculations accurate
- Multiplicative calculations 'accurate' but minWidth an issue

### Feedback Log
- Carlo to check Issue 197
- Carlo to check Issue 193
- Issues 199, 198 resolved
- Matt & Greg to follow up on Issues 192, 194

### SOW - LT Maintenance
- Sebastion to provide starting location for Long Term Maintenance Support

</details>

<details>
  <summary><b>11.03 Open issues:</b></summary>

### minWidth
- Found major bug with determining minWidth that prevents proper multiplicative calculations
- Reached out to ASTI/Graitec and asked for a phone call

### Test Case 6F
- Multiplicative calculation issue resolved
- minWidth issue opened

</details>

<details>
  <summary><b>11.02 Open issues:</b></summary>

### Test Case 6F
- .JSON file received and analyzed
- Reductive and multiplicative charts to be created
- Issue with Greg's multiplicative calculation needs to be resolved

### Issue 194
- Carlo wants to look into this more
- Graitec was added to the project

### Issue 199
- Graitec/ASTI explained that if you zoom in, you can see that the ridge-line to the left of the terminal is showing red
- Root cause found to be that POIs were not placed in the proper locations
- End result was confirmed

### Multiplicative General
- Greg working on resolving code issues in calculating Multiplicative on our side

### Other
- Graitec/ASTI working on new update

</details>
<details>
  <summary><b>10.27 Open issues:</b></summary>

### Test Case 6F
- Carlo provided new code to allow for TC6F to run
- TC6F has been ran and I need to request JSON file from Carlo

### Layer Visibility
- This issue appears resolved as of last push

### Multiplicative
- Greg has worked through all multiplicative values from JSON files on TC1-TC7 excluding 6
- There appears to be some issues on TC7 with the multiplicative flowchart
- There appears to be some issues on TC2 with the cylindrical calculations

</details>

<details>
  <summary><b>10.25 Open issues:</b></summary>

### Test Case 6F
- Model is uploaded and active
- POIs are placed on model
- Model is analyzed
- Analysis is not correct and needs attention
- Email sent to Carlo explaining the issue
- Carlo hasn't looked at the air terminals not providing a CV

### Layer Visibility
- Carlo figured out a primary issue for layers bypassing the visibility toggle when regenerating
- The issue is expected to be resolved by 11.02

### Multiplicative
- Greg is working through multiplicative analysis of all test cases
- All multiplicative test cases are expected to be analyzed by end of this week

</details>