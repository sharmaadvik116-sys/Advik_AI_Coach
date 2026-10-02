# Land Cover Classification in Remote Sensing

## What Is Land Cover?

Land cover describes what physically covers the surface of Earth.

Examples include:

- Forest
- Water
- Cropland
- Grassland
- Wetlands
- Urban areas
- Barren land
- Snow and ice

Remote sensing can help identify and map different types of land cover across large areas.

---

# Why Is Land Cover Classification Useful?

Land cover maps can help scientists study:

- Forests
- Agriculture
- Urban growth
- Habitat
- Water resources
- Environmental change
- Deforestation
- Land-cover change

Because satellites can repeatedly observe large areas, remote sensing is useful for monitoring land-cover changes over time.

---

# How Remote Sensing Identifies Land Cover

Different land-cover types interact with electromagnetic radiation differently.

For example:

- Vegetation can have a strong response in near-infrared wavelengths.
- Water often has relatively low reflectance in many near-infrared wavelengths.
- Soil has its own reflectance characteristics.
- Urban materials can have different visible, infrared, thermal, and radar responses.

These differences can be used to classify pixels into land-cover categories.

---

# Classification

Classification is the process of assigning pixels or areas to categories.

For example:

A remote sensing image might be classified into:

- Water
- Forest
- Urban
- Cropland
- Grassland
- Barren land

The classification result can then be displayed as a map.

---

# Supervised Classification

In supervised classification, the analyst provides examples of known land-cover classes.

These examples are sometimes called training data.

For example, the analyst may identify areas known to be:

- Forest
- Water
- Urban
- Cropland

The classification method uses the characteristics of these training examples to classify other pixels.

---

## Basic Supervised Classification Process

### Step 1

Identify known examples of each land-cover class.

### Step 2

Use those examples as training information.

### Step 3

Analyze the spectral or other measured characteristics of the training areas.

### Step 4

Classify other pixels based on their similarity to the training information.

### Step 5

Evaluate the classification result.

---

# Unsupervised Classification

In unsupervised classification, the system groups pixels based on similarities in their measured characteristics.

The analyst does not initially provide every land-cover class.

The system creates groups or clusters.

The analyst then examines the clusters and determines what they may represent.

---

## Basic Unsupervised Classification Process

### Step 1

Provide the remote sensing data.

### Step 2

The classification method identifies groups of pixels with similar characteristics.

### Step 3

The resulting clusters are examined.

### Step 4

The analyst assigns meaningful land-cover labels to the groups.

---

# Supervised vs. Unsupervised Classification

| Feature | Supervised | Unsupervised |
|---|---|---|
| Training examples provided? | Yes | No initial labeled training examples |
| Initial classes specified by analyst? | Yes | Not necessarily |
| System groups pixels automatically? | Uses training information | Yes |
| Analyst interprets results? | Yes | Yes |
| Main idea | Learn from known examples | Find groups of similar pixels |

---

# Spectral Information and Classification

Classification often uses information about how pixels respond at different wavelengths.

A pixel may have measurements in several spectral bands.

For example:

| Band | Possible Information |
|---|---|
| Blue | Visible reflectance |
| Green | Visible reflectance |
| Red | Visible reflectance |
| NIR | Vegetation response |
| SWIR | Surface material and moisture information |

The combination of measurements can help distinguish land-cover types.

---

# Multispectral Imagery

Multispectral sensors collect information in multiple wavelength bands.

Different bands provide different information about Earth's surface.

Combining several bands can make land-cover classes easier to distinguish.

---

# Classification and Image Interpretation

Classification and image interpretation are related but are not exactly the same.

### Image interpretation

A person examines an image and uses visual and scientific evidence to understand what features are present.

### Classification

Pixels or areas are assigned to categories using measured characteristics and a classification method.

Both approaches can use spectral information.

---

# Land-Cover Change

Land cover can change over time.

Examples include:

- Forest converted to agriculture
- Forest cleared for development
- Agricultural land converted to urban areas
- New roads and buildings
- Wetlands changing
- Burned areas recovering
- Water bodies changing in extent

Remote sensing can compare images from different dates to identify these changes.

---

# Change Detection

Change detection involves comparing observations from different times.

A simple workflow is:

1. Obtain imagery from an earlier date.
2. Obtain imagery from a later date.
3. Make sure the observations are comparable.
4. Identify differences.
5. Determine whether the differences represent actual land-cover change.
6. Map or measure the change.

---

# Example: Urban Growth

Suppose a satellite image from an earlier year shows:

- Forest
- Agricultural fields
- A small urban area

A later image shows:

- More buildings
- More roads
- Less agricultural land

The comparison may indicate urban expansion.

Remote sensing can be used to map and measure this change.

---

# Example: Deforestation

Suppose an earlier image shows a large forested area.

A later image shows that part of the area has been converted to another land-cover type.

Remote sensing can help:

- Locate the changed area
- Estimate its size
- Compare changes over time
- Create a land-cover change map

---

# Land Cover vs. Land Use

These terms are related but different.

### Land cover

Describes what physically covers the surface.

Examples:

- Trees
- Water
- Buildings
- Grass
- Bare soil

### Land use

Describes how people use the land.

Examples:

- Agriculture
- Residential development
- Industrial development
- Recreation

A remote sensing classification may focus specifically on land cover.

---

# Classification Accuracy

A classification is not automatically correct just because every pixel has been assigned a category.

Classification results should be evaluated.

Possible sources of error include:

- Similar spectral responses between different materials
- Mixed pixels
- Atmospheric effects
- Shadows
- Seasonal differences
- Sensor limitations
- Incorrect training data

---

# Mixed Pixels

A pixel may contain more than one type of land cover.

For example, one pixel could contain:

- Part of a road
- Part of vegetation
- Part of a building

This is called a mixed pixel.

Mixed pixels can make classification more difficult because the measured signal represents multiple materials.

---

# Training Data

Good training data are important for supervised classification.

Training areas should represent the land-cover classes accurately.

If the training data are poor, the classification may also be poor.

---

# Land Cover Change Index

Land-cover datasets can be used to examine how land cover changes over time.

A change index can summarize or represent changes between different land-cover conditions.

When interpreting a particular land-cover change dataset, always check:

- The dataset definition
- The time period
- The classification categories
- The geographic area
- The units or index meaning

---

# Classification Strategy

When solving a land-cover classification problem, ask:

1. What land-cover classes are being considered?
2. What sensor or imagery is being used?
3. Which spectral bands are available?
4. What characteristics distinguish the classes?
5. Is the method supervised or unsupervised?
6. What training information is available?
7. Could mixed pixels affect the result?
8. How was classification accuracy evaluated?

---

# Quick Review

### Land cover

What physically covers Earth's surface.

### Classification

Assigning pixels or areas to categories.

### Supervised classification

Uses known training examples.

### Unsupervised classification

Groups pixels based on similarities before the analyst assigns meaning to the groups.

### Multispectral imagery

Uses multiple wavelength bands.

### Mixed pixel

A pixel containing more than one surface type.

### Change detection

Comparing observations from different times to identify changes.

---

# Practice Questions

## Question 1

What does land cover describe?

A. How fast a satellite moves  
B. What physically covers Earth's surface  
C. The satellite's orbit  
D. The Earth's rotation

---

## Question 2

Which classification method uses known examples as training data?

A. Unsupervised classification  
B. Supervised classification  
C. Random classification  
D. Thermal classification

---

## Question 3

What happens during unsupervised classification?

A. Every pixel is manually labeled first  
B. Pixels are grouped based on similarities in their measured characteristics  
C. The satellite changes its orbit  
D. Only visible light is measured

---

## Question 4

Why can mixed pixels make classification difficult?

A. They contain measurements from more than one surface type  
B. They always have no data  
C. They are always clouds  
D. They have no spatial location

---

## Question 5

Which example represents land-cover change?

A. A satellite moving into a different orbit  
B. Forest being converted to another surface type  
C. A map being printed  
D. A sensor changing its name

---

## Question 6

Why can multispectral imagery help with land-cover classification?

A. It provides information from multiple wavelength bands  
B. It removes all measurement errors  
C. It makes every pixel the same  
D. It eliminates the need for image interpretation

---

## Question 7

A student is given known examples of forest, water, and urban areas and uses them to classify the rest of an image. What method is being described?

A. Supervised classification  
B. Unsupervised classification  
C. Radar altimetry  
D. InSAR

---

# Key Memory Tricks

**Land cover → What is physically there?**

**Supervised → Examples are supplied**

**Unsupervised → Groups are discovered first**

**Multispectral → Multiple wavelength bands**

**Mixed pixel → More than one surface type in a pixel**

**Change detection → Compare different times**