---
title: Home
hero: true
hero_code: |
    class Researcher:

        def __init__(self):
            self.name = "Dr. Antoine Chevrot"
            self.position = "Assistant Professor"
            self.university = "Marie and Louis Pasteur"
            self.interests = [
                "Machine Learning",
                "Autonomous Testing",
                "Python (duh)",
            ]
        
        def contact(self):
            return "antoine.chevrot@umlp.fr"
    
    # Usage
    me = Researcher()
    print(f"Welcome to {me.name}'s website!")

email: antoine.chevrot@umlp.fr
github: achevrot
scholar: 0C7Wc-4AAAAJ

---

## About_Me

I am an Assistant Professor in the Department of Computer Science at **University of Marie and Louis Pasteur**. My research focuses on developing novel machine learning algorithms with applications in Autonomous Testing and Anomaly Detection.

### Research Interests

- **Deep Learning**: Neural network architectures and optimiSation
- **Autonomous Testing**: Large language models and text understanding
- **Anomaly Detection**: Anomaly detection in Time-Series and Identified Flying Objects (for now)

### News

- **[Sep 2025]** Started new position at University of Marie and Louis Pasteur
- **[Jun 2025]** Presenting paper on Autonomous agent at ISSTA in Trondheim 

## Education

```python
education = [
    {"degree": "Ph.D. Computer Science", "University": "Université de Bourgogne Franche-Comté", "year": 2022},
    {"degree": "Engineer Degree in Computer Science", "school": "INSA de Lyon", "year": 2016}
] 
```