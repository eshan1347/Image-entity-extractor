# Product Image Entity Value Extraction

This project focuses on extracting structured text from product images to identify specific entity values and corresponding units (e.g., dimensions, weight, volume) using Optical Character Recognition (OCR) and object detection techniques.

## Table of Contents
- [Introduction](#introduction)
- [Dataset](#dataset)
- [Requirements](#requirements)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Results](#results)

## Introduction

The goal of this project is to automate the extraction of product-related values such as dimensions, weight, or voltage from product images using OCR models and preprocessing techniques. The images typically contain the product specifications, which are extracted and converted into structured text by leveraging text detection models like CRAFT (Character Region Awareness for Text) and OCR model : EasyOCR. This project was initially developed as a submission for Amazon ML challenge 2024.

Key challenges solved in this project include:
- Detecting and extracting text from complex, noisy and rotated product images.
- Extracting the correct entity value with units as most images from the given dataset had a variety of units present in them 
- Preprocessing the images for improved OCR performance.
- Handling diverse units and values and converting them to standardized formats.

## Dataset

The dataset consists of product images and a corresponding CSV file containing metadata such as:
- `group_id`: An identifier for the product group.
- `entity_name`: The type of value to extract (e.g., `width`, `weight`, `voltage`).
- `entity_value`: The expected value to extract from the image.
- `image_link`: The URL or file path to the product image.

The dataset is split into training and test datasets:
- `train.csv`: Used for model training and validation.
- `test.csv`: Used for evaluating the model performance.

### Sample CSV structure:
| group_id | entity_name | entity_value | image_link |
|----------|-------------|--------------|------------|
| 1        | weight      | 6.4 kg       | image1.jpg |
| 2        | width       | 15 cm        | image2.jpg |

## Requirements

This project requires the following dependencies:
- Python 3.x
- Torch (PyTorch) for model building
- CRAFT Text Detector for detecting text in images
- EasyOCR for text recognition

Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Methodology

Initially , to solve this problem statement, we tried implementing simply OCR models like EasyOCR , paddleOCR but they did not give good results. Even larger models like Tesserect and LLAVA gave mediocre results. So, the final approach that is implemented uses CRAFT model for text region detection , then we process the image by resizing , denoising and increasing contrast and grayscaling. Then the text boxes recognised by craft are each cropped and rotated , if there is rotation present, before being fed to the EasyOCR model to extract the text. After that , the text is passed to our extract_value_and_unit() function which based on pattern matching and rule based approach and using an entity_unit_map, gives the standardised unit and entity value. 

## Project Structure
```
.
├── dataset/
│   ├── train.csv
│   ├── test.csv
│   └── imagestrain/
│       └── sampleTrain/  # Contains the product images
├── craft_text_detector/  # CRAFT model folder
├── main.py  # Main project script
├── product_image_dataset.py 
├── utils.py
├── requirements.txt
├── code.ipynb
└── README.md  # This file
```
amazonml24(4).ipynb : Contains the entire code written and executed on a kaggle environment.
main.py: Contains the main functionality for loading the dataset, preprocessing images, detecting text, and extracting values.
product_image_dataset.py: Defines the ProductImageDataset class for loading and transforming images.
utils.py: Includes utility functions for text processing, image manipulation, image download etc.
craft_text_detector: Some changes were made to the craft_text_detector to fix compatibility issues: Fixed import issues in vgg16_bn.py.
                                                                                                    Adjusted data types for polygons and predictions in craft_utils.py and predict.py.

## Usage

To run the project:

Ensure all dependencies are installed.
Organize your dataset as specified in the Dataset section.
Update the image paths in the dataset CSV if needed.
Run the main script:
```
python main.py
```

## Results

The model is capable of accurately extracting entity values such as dimensions (width, height, depth) and weight from product images with structured labels. The results are stored in a CSV format or can be visualized as annotations over the original images.

Evaluation metrics include:

Accuracy: The percentage of correctly identified and extracted entity values.
F1-Score: For text detection and recognition.
