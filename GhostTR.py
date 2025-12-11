#!/usr/bin/python
# IMPORT MODULE
import json
import requests
import time
import os
import sys
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
import re

Bl = '\033[30m'  # VARIABLE BUAT WARNA CUYY
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'


# Regex patterns for validation
IPV4_PATTERN = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
    r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
)

IPV6_PATTERN = re.compile(
    r'^(?:(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|'
    r'(?:[0-9a-fA-F]{1,4}:){1,7}:|'
    r'(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
    r'(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|'
    r'(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|'
    r'(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|'
    r'(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|'
    r'[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|'
    r':(?:(?::[0-9a-fA-F]{1,4}){1,7}|:))$'
)

USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]+$')


# ============================================================================
# INPUT VALIDATION FUNCTIONS
# ============================================================================

def validate_ipv4(ip):
    """Validate IPv4 address format.
    
    Args:
        ip (str): The IP address string to validate
        
    Returns:
        bool: True if valid IPv4 format, False otherwise
    """
    return bool(IPV4_PATTERN.match(ip))


def validate_ipv6(ip):
    """Validate IPv6 address format.
    
    Args:
        ip (str): The IP address string to validate
        
    Returns:
        bool: True if valid IPv6 format, False otherwise
        
    Example:
        >>> validate_ipv6('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        True
        >>> validate_ipv6('invalid::address')
        False
    """
    return bool(IPV6_PATTERN.match(ip))


def validate_ip(ip):
    """Validate IP address (both IPv4 and IPv6).
    
    Args:
        ip (str): The IP address string to validate
        
    Returns:
        bool: True if valid IPv4 or IPv6 format, False otherwise
        
    Example:
        >>> validate_ip('192.168.1.1')
        True
        >>> validate_ip('2001:0db8::1')
        True
    """
    return validate_ipv4(ip) or validate_ipv6(ip)


def validate_username(username):
    """Validate username contains only allowed characters.
    
    Args:
        username (str): The username to validate
        
    Returns:
        bool: True if username contains only alphanumeric, underscore, dot, or hyphen
        
    Example:
        >>> validate_username('john_doe')
        True
        >>> validate_username('user@domain')
        False
    """
    return bool(USERNAME_PATTERN.match(username))


# utilities

# decorator for attaching run_banner to a function
def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        func(*args, **kwargs)


    return wrapper


# FUNCTIONS FOR MENU
@is_option
def IP_Track():
    while True:
        ip = input(f"{Wh}\n Enter IP target : {Gr}").strip()  # INPUT IP ADDRESS
        
        # Validate IP address format
        if not ip:
            print(f"{Re}\n[!] Error: IP address cannot be empty")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        # Validate IP format using regex
        if not validate_ip(ip):
            print(f"{Re}\n[!] Error: Invalid IP address format")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        # Identify IP type
        ip_type = "IPv4" if validate_ipv4(ip) else "IPv6"
        print(f"{Gr}\n[✓] Valid {ip_type} address detected")
        
        print()
        print(f' {Wh}============= {Gr}SHOW INFORMATION IP ADDRESS {Wh}=============')
        
        try:
            # API request with timeout
            req_api = requests.get(f"http://ipwho.is/{ip}", timeout=10)
            req_api.raise_for_status()
            ip_data = json.loads(req_api.text)
            
            # Check if API returned success
            if not ip_data.get('success', True):
                print(f"{Re}\n[!] Error: {ip_data.get('message', 'Invalid IP address')}")
                retry = input(f"{Wh}\n[{Ye}?{Wh}] Try with different IP? (y/n): {Gr}").strip().lower()
                if retry != 'y':
                    return
                continue
                
        except requests.exceptions.Timeout:
            print(f"{Re}\n[!] Error: Request timed out. Please check your internet connection.")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Retry? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        except requests.exceptions.ConnectionError:
            print(f"{Re}\n[!] Error: Unable to connect to the API. Please check your internet connection.")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Retry? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        except requests.exceptions.HTTPError as e:
            print(f"{Re}\n[!] Error: HTTP error occurred: {e}")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Retry? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        except json.JSONDecodeError:
            print(f"{Re}\n[!] Error: Failed to parse API response")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Retry? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        except Exception as e:
            print(f"{Re}\n[!] Unexpected error: {str(e)}")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Retry? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        # If we got here, the request was successful
        break
    
    # Extract coordinates
    lat = ip_data.get('latitude', 0)
    lon = ip_data.get('longitude', 0)
    
    print(f"\n{Wh}{'='*70}")
    print(f"{Gr}{'IP ADDRESS TRACKING RESULTS':^70}")
    print(f"{Wh}{'='*70}\n")
    
    # BASIC INFORMATION
    print(f"{Cy}[BASIC INFORMATION]{Wh}")
    print(f"{'─'*70}")
    print(f"{Wh}IP Target       : {Gr}{ip}")
    print(f"{Wh}IP Type         : {Gr}{ip_type}")
    print(f"{Wh}Connection Type : {Gr}{ip_data['type']}\n")
    
    # LOCATION DETAILS
    print(f"{Cy}[GEOGRAPHIC LOCATION]{Wh}")
    print(f"{'─'*70}")
    print(f"{Wh}Country         : {Gr}{ip_data['country']} {ip_data['flag']['emoji']} ({ip_data['country_code']})")
    print(f"{Wh}City            : {Gr}{ip_data['city']}")
    print(f"{Wh}Region          : {Gr}{ip_data['region']} ({ip_data['region_code']})")
    print(f"{Wh}Continent       : {Gr}{ip_data['continent']} ({ip_data['continent_code']})")
    print(f"{Wh}Postal Code     : {Gr}{ip_data['postal']}")
    print(f"{Wh}Capital         : {Gr}{ip_data['capital']}")
    print(f"{Wh}EU Member       : {Gr}{ip_data['is_eu']}")
    print(f"{Wh}Calling Code    : {Gr}{ip_data['calling_code']}")
    
    # COORDINATES
    print(f"{Cy}[COORDINATES & MAP]{Wh}")
    print(f"{'─'*70}")
    print(f"{Wh}Latitude        : {Gr}{lat}")
    print(f"{Wh}Longitude       : {Gr}{lon}")
    print(f"{Wh}Google Maps     : {Gr}https://www.google.com/maps/@{lat},{lon},8z\n")
    
    # CONNECTION INFO
    print(f"{Cy}[CONNECTION DETAILS]{Wh}")
    print(f"{'─'*70}")
    print(f"{Wh}ISP             : {Gr}{ip_data['connection']['isp']}")
    print(f"{Wh}Organization    : {Gr}{ip_data['connection']['org']}")
    print(f"{Wh}ASN             : {Gr}{ip_data['connection']['asn']}")
    print(f"{Wh}Domain          : {Gr}{ip_data['connection']['domain']}\n")
    
    # TIMEZONE INFO
    print(f"{Cy}[TIMEZONE INFORMATION]{Wh}")
    print(f"{'─'*70}")
    print(f"{Wh}Timezone ID     : {Gr}{ip_data['timezone']['id']}")
    print(f"{Wh}Abbreviation    : {Gr}{ip_data['timezone']['abbr']}")
    print(f"{Wh}UTC Offset      : {Gr}{ip_data['timezone']['utc']} ({ip_data['timezone']['offset']})")
    print(f"{Wh}DST Active      : {Gr}{ip_data['timezone']['is_dst']}")
    print(f"{Wh}Current Time    : {Gr}{ip_data['timezone']['current_time']}")
    
    print(f"\n{Wh}{'='*70}")


@is_option
def phoneGW():
    while True:
        User_phone = input(
            f"\n {Wh}Enter phone number target {Gr}Ex [+6281xxxxxxxxx] {Wh}: {Gr}").strip()  # INPUT NUMBER PHONE
        
        if not User_phone:
            print(f"{Re}\n[!] Error: Phone number cannot be empty")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        # Check if country code is provided
        if not User_phone.startswith('+'):
            print(f"{Re}\n[!] Error: Phone number must include country code")
            print(f"{Ye}    Please start with + followed by country code")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        # Validate that after + there are only digits
        if not User_phone[1:].replace(' ', '').replace('-', '').isdigit():
            print(f"{Re}\n[!] Error: Invalid characters in phone number")
            print(f"{Ye}    Phone number should only contain: + digits spaces -")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        default_region = "ID"  

        try:
            parsed_number = phonenumbers.parse(User_phone, default_region)  # VARIABLE PHONENUMBERS
            break  # Success, exit the loop
        except phonenumbers.NumberParseException as e:
            print(f"{Re}\n[!] Error: Invalid phone number format - {str(e)}")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        except Exception as e:
            print(f"{Re}\n[!] Unexpected error while processing phone number: {str(e)}")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
    try:
        region_code = phonenumbers.region_code_for_number(parsed_number)
        jenis_provider = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "id")
        is_valid_number = phonenumbers.is_valid_number(parsed_number)
        is_possible_number = phonenumbers.is_possible_number(parsed_number)
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        formatted_number_for_mobile = phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region,
                                                                                    with_formatting=True)
        number_type = phonenumbers.number_type(parsed_number)
        timezone1 = timezone.time_zones_for_number(parsed_number)
        timezoneF = ', '.join(timezone1)
    except Exception as e:
        print(f"{Re}\n[!] Error retrieving phone number information: {str(e)}")
        return

    print(f"\n{Wh}{'='*70}")
    print(f"{Gr}{'PHONE NUMBER TRACKING RESULTS':^70}")
    print(f"{Wh}{'='*70}\n")
    
    # VALIDATION STATUS
    validation_status = f"{Gr}✓ Valid" if is_valid_number else f"{Re}✗ Invalid"
    print(f"{Cy}[VALIDATION STATUS]{Wh}")
    print(f"{'─'*70}")
    print(f"{Wh}Status          : {validation_status}")
    print(f"{Wh}Valid Number    : {Gr if is_valid_number else Re}{is_valid_number}")
    print(f"{Wh}Possible Number : {Gr if is_possible_number else Re}{is_possible_number}\n")
    
    # PHONE NUMBER FORMATS
    print(f"{Cy}[NUMBER FORMATS]{Wh}")
    print(f"{'─'*70}")
    print(f"{Wh}International    : {Gr}{formatted_number}")
    print(f"{Wh}E.164 Format     : {Gr}{phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
    print(f"{Wh}Mobile Format    : {Gr}{formatted_number_for_mobile}")
    print(f"{Wh}National Number  : {Gr}{parsed_number.national_number}")
    print(f"{Wh}Country Code     : {Gr}+{parsed_number.country_code}\n")
    
    # LOCATION & CARRIER
    print(f"{Cy}[LOCATION & CARRIER]{Wh}")
    print(f"{'─'*70}")
    print(f"{Wh}Location         : {Gr}{location}")
    print(f"{Wh}Region Code      : {Gr}{region_code}")
    print(f"{Wh}Timezone(s)      : {Gr}{timezoneF}")
    print(f"{Wh}Operator/Carrier : {Gr}{jenis_provider if jenis_provider else 'Unknown'}\n")
    
    # Detailed phone type information
    print(f"{Cy}[NUMBER TYPE & DESCRIPTION]{Wh}")
    print(f"{'─'*70}")
    if number_type == phonenumbers.PhoneNumberType.MOBILE:
        print(f"{Wh}Type            : {Gr}Mobile/Cellular ")
        print(f"{Wh}Description     : {Gr}This is a mobile phone number")
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
        print(f"{Wh}Type            : {Gr}Fixed Line ")
        print(f"{Wh}Description     : {Gr}This is a landline/home phone number")
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE:
        print(f"{Wh}Type            : {Gr}Fixed Line or Mobile ")
        print(f"{Wh}Description     : {Gr}Could be either landline or mobile")
    elif number_type == phonenumbers.PhoneNumberType.TOLL_FREE:
        print(f"{Wh}Type            : {Gr}Toll-Free ")
        print(f"{Wh}Description     : {Gr}Free to call number")
    elif number_type == phonenumbers.PhoneNumberType.SHARED_COST:
        print(f"{Wh}Type            : {Gr}Shared Cost ")
        print(f"{Wh}Description     : {Gr}Cost shared between caller and recipient")
    elif number_type == phonenumbers.PhoneNumberType.VOIP:
        print(f"{Wh}Type            : {Gr}VoIP ")
        print(f"{Wh}Description     : {Gr}Internet-based phone number")
    else:
        print(f"{Wh}Type            : {Ye}Unknown ")
        print(f"{Wh}Description     : {Ye}Phone type could not be determined")
    
    print(f"\n{Wh}{'='*70}")

@is_option
def TrackLu():
    while True:
        username = input(f"\n {Wh}Enter Username : {Gr}").strip()
        
        if not username:
            print(f"{Re}\n[!] Error: Username cannot be empty")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        if len(username) < 2:
            print(f"{Re}\n[!] Error: Username too short (minimum 2 characters)")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        if len(username) > 50:
            print(f"{Re}\n[!] Error: Username too long (maximum 50 characters)")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        # Validate username format
        if not validate_username(username):
            print(f"{Re}\n[!] Error: Invalid username format")
            print(f"{Ye}    Username can only contain:")
            print(f"{Ye}    - Letters (a-z, A-Z)")
            print(f"{Ye}    - Numbers (0-9)")
            print(f"{Ye}    - Special characters: _ . -")
            retry = input(f"{Wh}\n[{Ye}?{Wh}] Try again? (y/n): {Gr}").strip().lower()
            if retry != 'y':
                return
            continue
        
        print(f"{Gr}\n[✓] Valid username format")
        break  # Success, exit the loop
    
    try:
        results = {}
        social_media = [
            {"url": "https://www.facebook.com/{}", "name": "Facebook"},
            {"url": "https://www.twitter.com/{}", "name": "Twitter"},
            {"url": "https://www.instagram.com/{}", "name": "Instagram"},
            {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
            {"url": "https://www.github.com/{}", "name": "GitHub"},
            {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
            {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
            {"url": "https://www.youtube.com/{}", "name": "Youtube"},
            {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
            {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
            {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
            {"url": "https://www.behance.net/{}", "name": "Behance"},
            {"url": "https://www.medium.com/@{}", "name": "Medium"},
            {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
            {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
            {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
            {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
            {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
            {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
            {"url": "https://www.ello.co/{}", "name": "Ello"},
            {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
            {"url": "https://www.telegram.me/{}", "name": "Telegram"},
            {"url": "https://www.weheartit.com/{}", "name": "We Heart It"}
        ]
        print(f"\n{Wh}[{Gr}*{Wh}] Searching across {len(social_media)} platforms...\n")
        
        for site in social_media:
            url = site['url'].format(username)
            try:
                response = requests.get(url, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    results[site['name']] = url
                else:
                    results[site['name']] = (f"{Ye}Not found")
            except requests.exceptions.Timeout:
                results[site['name']] = (f"{Re}Timeout")
            except requests.exceptions.ConnectionError:
                results[site['name']] = (f"{Re}Connection error")
            except Exception as e:
                results[site['name']] = (f"{Re}Error: {str(e)[:20]}")
    except KeyboardInterrupt:
        print(f"\n{Re}[!] Search cancelled by user")
        return
    except Exception as e:
        print(f"{Re}\n[!] Unexpected error: {str(e)}")
        return
    
    # Categorize results
    found_results = {}
    not_found_results = {}
    error_results = {}
    
    for site, result in results.items():
        if 'Not found' in str(result):
            not_found_results[site] = result
        elif any(err in str(result) for err in ['Timeout', 'Connection error', 'Error']):
            error_results[site] = result
        else:
            found_results[site] = result
    
    # Calculate statistics
    total_platforms = len(social_media)
    found_count = len(found_results)
    not_found_count = len(not_found_results)
    error_count = len(error_results)
    success_rate = (found_count / total_platforms * 100) if total_platforms > 0 else 0
    
    # Display results
    print(f"\n{Wh}{'='*70}")
    print(f"{Gr}{'USERNAME TRACKING RESULTS':^70}")
    print(f"{Wh}{'='*70}\n")
    
    # Username only
    print(f"{Wh}Username: {Gr}{username}\n")
    
    # Found profiles
    if found_results:
        print(f"{Gr}[✓ FOUND PROFILES - {len(found_results)}]{Wh}")
        print(f"{Gr}{'─'*70}")
        for idx, (site, url) in enumerate(found_results.items(), 1):
            print(f"{Gr}{idx:2d}. {Wh}{site:<20} {Gr}→ {url}")
        print()
    
    # Not found profiles  
    if not_found_results:
        print(f"{Ye}[✗ NOT FOUND - {len(not_found_results)}]{Wh}")
        print(f"{Ye}{'─'*70}")
        # Show first 10, then summarize if more
        displayed = 0
        for site in not_found_results:
            if displayed < 10:
                print(f"{Ye}   {site}")
                displayed += 1
        if len(not_found_results) > 10:
            print(f"{Ye}   ... and {len(not_found_results) - 10} more")
        print()
    
    # Errors
    if error_results:
        print(f"{Re}[! ERRORS - {len(error_results)}]{Wh}")
        print(f"{Re}{'─'*70}")
        for site, error in error_results.items():
            print(f"{Re}   {site:<20} → {error}")
        print()
    
    print(f"{Wh}{'='*70}")
    
    # Ask if user wants to search another username
    another = input(f"\n{Wh}[{Gr}?{Wh}] Search another username? (y/n): {Gr}").strip().lower()
    if another == 'y':
        TrackLu()  # Recursive call to search again


@is_option
def showIP():
    try:
        respone = requests.get('https://api.ipify.org/', timeout=10)
        respone.raise_for_status()
        Show_IP = respone.text.strip()
        
        if not Show_IP:
            print(f"{Re}\n[!] Error: Unable to retrieve IP address")
            return

        print(f"\n{Wh}{'='*70}")
        print(f"{Gr}{'YOUR PUBLIC IP ADDRESS':^70}")
        print(f"{Wh}{'='*70}\n")
        print(f"{Wh}IP Address      : {Gr}{Show_IP}")
        print(f"{Wh}Status          : {Gr}✓ Retrieved Successfully")
        print(f"\n{Wh}{'='*70}")
    except requests.exceptions.Timeout:
        print(f"{Re}\n[!] Error: Request timed out. Please check your internet connection.")
    except requests.exceptions.ConnectionError:
        print(f"{Re}\n[!] Error: Unable to connect to the API. Please check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"{Re}\n[!] Error: HTTP error occurred: {e}")
    except Exception as e:
        print(f"{Re}\n[!] Unexpected error: {str(e)}")


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux
    else:
        _ = os.system('clear')


def exit_program():
    """Exit the program and close the terminal window."""
    print(f'{Gr}\n[✓] Thank you for using GhostTrack!')
    print(f'{Wh}[{Gr}+{Wh}] Goodbye!\n')
    
    # For Windows, close the command prompt window
    if os.name == 'nt':
        os.system('taskkill /F /IM cmd.exe /T')
    
    # Fallback to normal exit
    sys.exit(0)


# OPTIONS
options = [
    {
        'num': 1,
        'text': 'IP Tracker',
        'func': IP_Track
    },
    {
        'num': 2,
        'text': 'Show Your IP',
        'func': showIP

    },
    {
        'num': 3,
        'text': 'Phone Number Tracker',
        'func': phoneGW
    },
    {
        'num': 4,
        'text': 'Username Tracker',
        'func': TrackLu
    },
    {
        'num': 0,
        'text': 'Exit',
        'func': exit_program
    }
]


def call_option(opt):
    if not is_in_options(opt):
        raise ValueError(f'{Re}Invalid option. Please select a valid option number.')
    for option in options:
        if option['num'] == opt:
            if 'func' in option:
                option['func']()
            else:
                print(f'{Re}No function detected for this option')


def execute_option(opt):
    try:
        call_option(opt)
        input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue')
        main()
    except ValueError as e:
        print(f'\n{str(e)}')
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        exit()
    except Exception as e:
        print(f'\n{Re}[!] Unexpected error: {str(e)}')
        main()


def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text


def is_in_options(num):
    for opt in options:
        if opt['num'] == num:
            return True
    return False


def option():
    # BANNER TOOLS
    clear()
    stderr.writelines(f"""
       ________               __      ______                __  
      / ____/ /_  ____  _____/ /_    /_  __/________ ______/ /__
     / / __/ __ \/ __ \/ ___/ __/_____/ / / ___/ __ `/ ___/ //_/
    / /_/ / / / / /_/ (__  ) /_/_____/ / / /  / /_/ / /__/ ,<   
    \____/_/ /_/\____/____/\__/     /_/ /_/   \__,_/\___/_/|_| 

              {Wh}[ + ]  C O D E   B Y  H U N X  [ + ]
    """)

    stderr.writelines(f"\n\n\n{option_text()}")


def run_banner():
    clear()
    stderr.writelines(f"""{Wh}
         .-.
       .'   `.          {Wh}--------------------------------
       :g g   :         {Wh}| {Gr}GHOST - TRACKER - IP ADDRESS {Wh}|
       : o    `.        {Wh}|       {Gr}@CODE BY HUNXBYTS      {Wh}|
      :         ``.     {Wh}--------------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:'
           :              `.
            `.              `.     .
              `'`'`'`---..,___`;.-'
        """)


def main():
    clear()
    option()
    try:
        opt = int(input(f"{Wh}\n [ + ] {Gr}Select Option : {Wh}"))
        execute_option(opt)
    except ValueError:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Please input number')
        main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        exit()
