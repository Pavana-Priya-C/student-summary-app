import re
from pdfminer.high_level import extract_text

# Function to extract text from PDF using PDFMiner
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Function to get the title
def get_title(text):
    # First, extract text up to the first occurrence of a number, including possible newlines
    match_number = re.search(r"^\s*\d+\s*\n+([^\d\n]+)", text, re.DOTALL)
    match_title1 = re.search(r"([^\d\n]+)\n\s*\d+\n", text, re.DOTALL)
    match_title_till_num = re.search(r"([^\d\n]+)\s*\n*\s*\d+", text, re.DOTALL)

    if match_number:
        # Extracted text before the number
        text_till_number = match_number.group(1).strip()

        # Extract the first meaningful line from the text before the number
        match_title = re.search(r"(.*?)\n", text_till_number, re.DOTALL)

        if match_title:
            return match_title.group(1).strip()  # Extract the first line as the title
        else:
            return text_till_number  # Return all text till the number if no line match        
      
    elif match_title1:
        # Extract and return the title, cleaning up any extra spaces or newlines
        title = match_title1.group(1).strip()
        return title

    elif match_title_till_num:
      title = match_title.group(1).strip()
      return title

    else:
        # If no number is found, apply fallback logic to look for a title pattern
        title = re.search(r"\d+\s*\n\n(.*?)\n", text, re.DOTALL)
        if title:
            return title.group(1).strip()
        else:
            return None

def get_title6_9(text):
    match_title = re.search(r"([^\d\n]+)\s*\n*\s*\d+", text, re.DOTALL)
    
    if match_title:
        # Extract and return the title, cleaning up any extra spaces or newlines
        title = match_title.group(1).strip()
        return title
    
    # Fallback if no match is found
    return None


def get_title_5(text):
    # Search for a pattern where the title appears before the number
    match_title = re.search(r"([^\d\n]+)\s*\n*\s*\d+", text, re.DOTALL)
    
    if match_title:
        # Extract and return the title, cleaning up any extra spaces or newlines
        title = match_title.group(1).strip()
        return title
    return None

#The below function is used only for Chapter 8
def preprocess_text_chap8(raw_text):
  pattern = r'^.*?(\d+).*?READ AND FIND OUT'

  # Search for the pattern and get the match
  match = re.search(pattern, raw_text, re.DOTALL)

  if match:
      # Extract the first occurrence of the number
      number_before_read = match.group(1)
      # Remove everything before the number and the "READ AND FIND OUT" section
      cleaned_text = re.sub(pattern, number_before_read, raw_text, flags=re.DOTALL)
  else:
      cleaned_text = raw_text

  return cleaned_text


# Function for preprocessing text
def preprocess_text(text):
    processed_text = re.sub(r'Reprint 2024-25|\d|\d+\s+Footprints without Feet|Footprints without Feet|A Triumph of Surgery\s\d|READ AND FIND OUT[\s\S]*?(?:•\s.*\n)+', '', text)
  
    # Replace multiple spaces with a single space
    processed_text = re.sub(r'\s+', ' ', processed_text)

    author_pattern = r'\b[A-Z]+\s+[A-Z]+\b'
    processed_text = re.sub(author_pattern, '', processed_text)

    # Strip leading and trailing whitespace
    processed_text = processed_text.strip()

    return processed_text

# Function to remove multiple occurrences of the title
# def remove_subsequent_occurrences(text, phrase):
#     parts = text.split(phrase)
#     return phrase + parts[1] + "".join(parts[2:])

def remove_subsequent_occurrences(text, phrase):
    parts = text.split(phrase)
    # Check if the phrase exists in the text
    if len(parts) > 1:
        return phrase + parts[1] + "".join(parts[2:])
    else:
        # If the phrase does not exist, return the original text
        return text

# Function to get separate sections from the extracted text
def separate_sections(text):
    # Define the regex patterns to extract the sections
    glossary_pattern = re.compile(r'GLOSSARY(.*?)Think about it', re.DOTALL)
    think_about_it_pattern = re.compile(r'Think about it(.*?)Talk about it', re.DOTALL)
    talk_about_it_pattern = re.compile(r'Talk about it(.*?)Suggested reading', re.DOTALL)
    suggested_reading_pattern = re.compile(r'Suggested reading(.*)', re.DOTALL)

    # Extract the sections using the patterns
    main_content = re.split(r'GLOSSARY|Think about it|Talk about it|Suggested reading', text)[0].strip()
    glossary = glossary_pattern.search(text)
    think_about_it = think_about_it_pattern.search(text)
    talk_about_it = talk_about_it_pattern.search(text)
    suggested_reading = suggested_reading_pattern.search(text)

    glossary = glossary.group(1).strip() if glossary else ''
    think_about_it = think_about_it.group(1).strip() if think_about_it else ''
    talk_about_it = talk_about_it.group(1).strip() if talk_about_it else ''
    suggested_reading = suggested_reading.group(1).strip() if suggested_reading else ''

    # Return the extracted sections
    return main_content, glossary, think_about_it, talk_about_it, suggested_reading