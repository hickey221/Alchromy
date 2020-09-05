import json

"""

*** MOVED TO ALCH_ENGINE ***

Take an alch OBJECT and save it to the disk as an .alch FILE

pickle vs json?

.alch
    - Metadata: {
        version: 1.0,
        date: 9/5/2020 14:04:00,
        name: "Test run",
        comments: None,
        file paths: [
                    C:/Users/...file.ext
                    ]
        }
    - Data
        - [Dataset 1]
        - [Dataset 2]
    - References
        - [Refset 1]
    - Results
        - Run 1
            - Data used: {
                Data: Dataset 1,
                Reference: Refset 1
                }
            - Settings used: {
                mode: 'Simple',
                wavelengths: (450, 700),
                normalize: False
                }
            - Analysis: {
                Components:
                R2: 0.99
                }

"""
