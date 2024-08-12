""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""

import datetime
import os
import image_lib
import sqlite3
import requests
import hashlib
import apod_api

#from datetime import date
# Full paths of the image cache folder and database
# - The image cache directory is a subdirectory of the specified parent directory.
# - The image cache database is a sqlite database located in the image cache directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')
image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    
    
    # Initialize the image cache
    init_apod_cache()
    
    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)
    print(f"En main apod_id={apod_id}")
    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # TODO: Complete function body
    # Hint: The following line of code shows how to convert and ISO-formatted date string to a date object
    print("funcion:get_apod_date")
    # {REQ-1}
    date_in = input("Give a date:(yyyy-mm-dd)")
    #date_in="2024-05-18"
    date_now= datetime.datetime.today() 
    # print(len(date_in))
    if (len(date_in)==0):
        # {REQ-4}
        print ("No date parameter")
        apod_date = datetime.datetime.fromisoformat(str(date_now))
        print(f"No date parameter. Considerer date today. apod_date:{apod_date}")
        return apod_date   
    elif ((date_in[4] !="-") or (date_in[7]!= "-") or len(date_in) < 10): 
        print ("Invalid Date format (yyyy-mm-dd)")
        exit()  # The invalid format

    # Split date given by user
    v_day=int(date_in[8:10])     # User day
    v_month = int(date_in[5:7])  # User month
    v_year = int(date_in[:4])    # User year    
    print(f"fecha proporcionada:{date_in}")
    
    date_now= datetime.datetime.today() 
    date2_now_d = date_now.day
    date2_now_m = date_now.month 
    date2_now_y= date_now.year
     
    # Validate the date

    # {REQ-2}  {REQ-3}
    if (v_year < 1995) or (v_year > 2024):
          print("Invalid Year ")
          exit()     # Invalid year   
    if (v_day <= 0) or (v_day > 31):
            print("Invalid Day")
            exit()   # Invalid day      
    if (v_month <= 0) or (v_month > 12): 
            print("Invalid Month")
            exit()    # Invalid month
            
    # Verify old and future date
    if (str(date_in) < ('1995-06-16')):
        print("Invalid date. The date must be > 1995-06-15")
        exit () # Invalid date
    elif (v_year > date2_now_y): 
          print("The year is future, the date must be <= the day now")
          exit () # Invalid year
    elif (str(v_year) == date2_now_y):
          if (v_month > date2_now_m):
                print("Invalid month, the month is future")
                exit ()    
          elif (v_month == date2_now_m) and (v_day > date2_now_d):
                print("The day is future, the day must be <= the day now")
                exit ()
        
    print(f"Valid Date:{date_in}")    
    apod_date = datetime.datetime.fromisoformat(date_in)
    print(f"apod_date isoformat:{apod_date}")
    return apod_date

def init_apod_cache():
    """Initializes the image cache by:
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    """
    # TODO: Create the image cache directory if it does not already exist
    # TODO: Create the DB if it does not already exist
    print("funcion: init_apod_cache")
    # Image Cache
    # {REQ-14} {REQ-15} Create directory
    if os.path.isdir(image_cache_dir):
        print(f"image_cache_directory:{image_cache_dir} already exists.")       
    else:           
        print(f"Images cache directory:{image_cache_dir} created.")
        os.mkdir(image_cache_dir)

    # Database
    if os.path.isfile(image_cache_db):
        print(f"Images cache DB:{script_dir}")
        print ("Image cache DB already exists.")
    else:
        # {REQ-11}
        print(f"image_cache_db:{image_cache_db}")
        con = sqlite3.connect('image_cache.db')
        cur = con.cursor()
        # {REQ-10} {REQ-12}
        create_ImageCache_tbl_query = """
           CREATE TABLE IF NOT EXISTS ImagesCache
           (
               id           INTEGER PRIMARY KEY,
               title        TEXT NOT NULL,
               explanation  TEXT,
               filepath     TEXT NOT NULL,
               type         TEXT NOT NULL,
               sha256       TEXT NOT NULL
           );
           """
        cur.execute(create_ImageCache_tbl_query)
        con.commit()
        con.close()                
    return

def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("funcion: add_apod_to_cache")
    print("APOD date:", apod_date.isoformat())
    # TODO: Download the APOD information from the NASA API
    # Hint: Use a function from apod_api.py 
    info_dict=apod_api.get_apod_image_url('2024-05-18')
    print(info_dict)
    #get_apod_info(apod_date)

    # TODO: Download the APOD image
    # Hint: Use a function from image_lib.py 

    # TODO: Check whether the APOD already exists in the image cache
    # Hint: Use the get_apod_id_from_db() function below

    # TODO: Save the APOD file to the image cache directory
    # Hint: Use the determine_apod_file_path() function below to determine the image file path
    # Hint: Use a function from image_lib.py to save the image file

    # TODO: Add the APOD information to the DB
    # Hint: Use the add_apod_to_db() function below
    v_titleaux = info_dict['title']
    v_title2=apod_api.cleanTitle(v_titleaux)
    v_expla = info_dict['explanation']
    v_type = info_dict['media_type']
    v_file_p = info_dict['url']
    if v_type == "video":
        v_title = v_title+".wav"
    #v_hash1 = v_file_p + 
    #v_sha256 = hash(info_dict[''])
    print("Valores extraidos del APOD image:")
    print(f"titulo:{v_title2}\n explicacion:{v_expla}\n tipo:{v_type}\n ruta:{v_file_p}")
    #add_apod_to_db(title, explanation, typeIma, file_path, sha256)
    return 0 

def add_apod_to_db(title, explanation, typeIma, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful. Zero, if unsuccessful       
    """
    # TODO: Complete function body
    print("add_apod_to_db")
    
    con = sqlite3.connect('image_cache.db')
    cur = con.cursor()   
    
    # Define an SQL query that inserts a row of data in the table.
    # The ?'s are placeholders to be fill in when the query is executed.
    # Specific values can be passed as a tuple into the execute() method.
    
    add_image_query = """
          INSERT INTO ImagesCache
          (
              tituloIma,
              explanationIma,
              filepathIma,
              typeIma,
              sha256Ima
          )
          VALUES (?, ?, ?, ?, ?);
    """
    title, explanation, typeIma, file_path, sha256

    new_image = (
                title,
                explanation,
                typeIma,
                file_path,
                sha256
            )
    cur.execute(add_image_query,new_image)
    # Execute query to add new image to ImageCache table
     
    cur.execute('SELECT * FROM ImageCache')
    all_image = cur.fetchall()
    print(all_image)
     
    con.commit()
    con.close()   
    return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    print("get_apod_id_from_db")
    resp_msg = requests.get(image_sha256)
    
    return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    # Hint: Use regex and/or str class methods to determine the filename.
    print ("funcion: determine_apod_file_path")
          
    return

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    # TODO: Put information into a dictionary
    apod_info = {
        #'title': , 
        #'explanation': ,
        'file_path': 'TBD',
    }
    
    print("funcion:get_apod_info")
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUIs
    print("get_all_apod_title")
    con = sqlite3.connect('image_cache.db')
    cur = con.cursor()  
    
    cur.execute('SELECT title* FROM ImageCache')
    all_image = cur.fetchall()
    print(all_image)
     
    con.commit()
    con.close()   
    
    return

if __name__ == '__main__':
    main()