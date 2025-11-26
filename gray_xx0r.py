#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import re
from typing import Optional, Set, List

# Color codes
BOLD_WHITE = "\033[1;97m"
BOLD_BLUE = "\033[1;34m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
BOLD_CYAN = "\033[1;36m"
CYAN = "\033[0;36m"
NC = "\033[0m"  # No Color
BLOOD_RED = "\033[38;5;196m"  # Blood red color

# Global variables
domain_name: Optional[str] = None
last_completed_option = 1
skip_order_check_for_option_4 = False
total_merged_urls = 0

def display_banner() -> None:
    print(f"{BLOOD_RED}")
    print(" ██████╗ ██████╗  █████╗ ██╗   ██╗    ██╗  ██╗███████╗███████╗")
    print("██╔════╝ ██╔══██╗██╔══██╗╚██╗ ██╔╝    ╚██╗██╔╝╚══███╔╝╚══███╔╝")
    print("██║  ███╗██████╔╝███████║ ╚████╔╝      ╚███╔╝   ███╔╝   ███╔╝ ")
    print("██║   ██║██╔══██╗██╔══██║  ╚██╔╝       ██╔██╗  ███╔╝   ███╔╝  ")
    print("╚██████╔╝██║  ██║██║  ██║   ██║       ██╔╝ ██╗███████╗███████╗")
    print(" ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚══════╝╚══════╝")
    print(f"{Version 2.0")
    print(f"{NC}")
    print(f"{BOLD_WHITE}                      Website: computerkorner.org")


def handle_error_with_solution(step: str, solution: str) -> None:
    print(f"{RED}Error occurred during the execution of {step}. Exiting step but continuing with the next installation.{NC}")
    with open("error.log", "a") as f:
        f.write(f"Error during: {step}\n")
    print(f"{YELLOW}Possible Solution for manual installation:{NC}")
    print(f"{BOLD_WHITE}{solution}{NC}")

def show_progress(message: str) -> None:
    print(f"{BOLD_BLUE}Current process: {message}...⌛️{NC}")

def check_command(command: str) -> None:
    try:
        subprocess.run([command, "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{BOLD_BLUE}{command} installed correctly.{NC}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{RED}{command} could not be found or is not installed correctly.{NC}")
        handle_error_with_solution(f"{command} installation check", f"Manual installation required for {command}")

def display_options() -> None:
    print(f"{BOLD_BLUE}Please select an option:{NC}")
    print(f"{RED}1: Install all tools{NC}")
    print(f"{RED}2: Enter a domain name of the target{NC}")
    print(f"{YELLOW}3: Enumerate and filter domains{NC}")
    print(f"{YELLOW}4: Crawl and filter URLs{NC}")
    print(f"{YELLOW}5: Filtering all{NC}")
    print(f"{YELLOW}6: Create new separated file for Arjun & SQLi testing{NC}")
    print(f"{YELLOW}7: Getting ready for XSS & URLs with query strings{NC}")
    print(f"{YELLOW}8: xss0r RUN{NC}")
    print(f"{YELLOW}9: Exit{NC}")
    print(f"{YELLOW}10: VPS server xss0r help{NC}")

def install_tools() -> None:
    global last_completed_option
    
    current_dir = os.getcwd()
    print(f"{BOLD_WHITE}You selected: Install all tools{NC}")
    
    # Update Parrot OS repositories
    show_progress("Updating Parrot OS repositories")
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)
    
    # Install dependencies
    show_progress("Installing dependencies")
    subprocess.run(["sudo", "apt", "install", "-y", 
                   "rsync", "zip", "unzip", "p7zip-full", "wget", "golang-go",
                   "python3-pip", "python3-venv", "terminator",
                   "subfinder", "amass", "assetfinder", "httprobe"], check=True)
    
    # Set up Python virtual environment
    show_progress("Setting up Python virtual environment")
    subprocess.run(["python3", "-m", "venv", "myenv"], check=True)
    
    # Install Go tools
    show_progress("Installing Go tools")
    subprocess.run(["go", "install", "github.com/projectdiscovery/katana/cmd/katana@latest"], check=True)
    subprocess.run(["go", "install", "github.com/tomnomnom/waybackurls@latest"], check=True)
    subprocess.run(["go", "install", "github.com/lc/gau/v2/cmd/gau@latest"], check=True)
    subprocess.run(["go", "install", "github.com/jaeles-project/gospider@latest"], check=True)
    subprocess.run(["go", "install", "github.com/hakluke/hakrawler@latest"], check=True)
    
    # Copy binaries to /usr/local/bin
    go_bin = os.path.expanduser("~/go/bin")
    for tool in ["katana", "waybackurls", "gau", "gospider", "hakrawler"]:
        subprocess.run(["sudo", "cp", os.path.join(go_bin, tool), "/usr/local/bin/"], check=True)
    
    # Install Python tools
    show_progress("Installing Python tools")
    subprocess.run([os.path.join(current_dir, "myenv", "bin", "pip"), "install", "uro", "arjun"], check=True)
    
    # Install other tools from Parrot repos
    show_progress("Installing tools from Parrot repositories")
    subprocess.run(["sudo", "apt", "install", "-y", "arjun", "tmux"], check=True)
    
    # Verify installations
    print(f"{BOLD_BLUE}Verifying installations...{NC}")
    for cmd in ["katana", "waybackurls", "gau", "gospider", "hakrawler", "arjun", "tmux", "subfinder", "amass", "assetfinder", "httprobe"]:
        check_command(cmd)
    
    print(f"{BOLD_BLUE}All tools have been successfully installed.{NC}")
    last_completed_option = 1

def run_step_3() -> None:
    global domain_name, last_completed_option
    
    if not domain_name:
        print("Domain name is not set. Please select option 2 first.")
        return
    
    print(f"{BOLD_WHITE}You selected: Enumerate and filter domains for {domain_name}{NC}")
    
    try:
        # Passive subdomain enumeration using tools available in Parrot OS
        show_progress("Running passive subdomain enumeration")
        
        # Using subfinder (available in Parrot OS)
        with open("subfinder.txt", "w") as f:
            subprocess.run(["subfinder", "-d", domain_name, "-silent"], stdout=f, check=True)
        
        # Using amass (available in Parrot OS)
        with open("amass.txt", "w") as f:
            subprocess.run(["amass", "enum", "-passive", "-d", domain_name], stdout=f, check=True)
        
        # Using assetfinder (available in Parrot OS)
        with open("assetfinder.txt", "w") as f:
            subprocess.run(["assetfinder", "--subs-only", domain_name], stdout=f, check=True)
        
        # Merge results
        show_progress("Merging results")
        with open(f"{domain_name}-domains.txt", "w") as outfile:
            for fname in ["subfinder.txt", "amass.txt", "assetfinder.txt"]:
                with open(fname) as infile:
                    outfile.write(infile.read())
        
        # Clean up temporary files
        for fname in ["subfinder.txt", "amass.txt", "assetfinder.txt"]:
            os.remove(fname)
        
        # Filter unique domains
        show_progress("Filtering unique domains")
        with open(f"{domain_name}-domains.txt") as infile, \
             open(f"unique-{domain_name}-domains.txt", "w") as outfile:
            domains = set()
            for line in infile:
                clean_line = re.sub(r'^https?://(www\.)?', '', line.strip())
                if clean_line and clean_line not in domains:
                    domains.add(clean_line)
                    outfile.write(clean_line + "\n")
        
        # Verify alive domains using httprobe (available in Parrot OS)
        show_progress("Verifying alive domains")
        with open(f"unique-{domain_name}-domains.txt") as infile, \
             open(f"{domain_name}-domains.txt", "w") as outfile:
            httprobe = subprocess.Popen(["httprobe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            output, _ = httprobe.communicate(input="\n".join(domains))
            outfile.write(output)
        
        # Clean up
        os.remove(f"unique-{domain_name}-domains.txt")
        
        print(f"{BOLD_BLUE}Enumeration completed. Results saved to {domain_name}-domains.txt{NC}")
        last_completed_option = 3
        
        # Ask to continue to step 4
        response = input(f"{BOLD_WHITE}Continue to crawl URLs (step 4)? [Y/n]: {NC}").strip().lower()
        if response in ('', 'y', 'yes'):
            run_step_4()
            
    except subprocess.CalledProcessError as e:
        handle_error_with_solution("Subdomain enumeration", "Check network connection and tool installations")

def run_step_4() -> None:
    global domain_name, last_completed_option, total_merged_urls
    
    if not domain_name:
        print("Domain name is not set. Please select option 2 first.")
        return
    
    print(f"{BOLD_WHITE}You selected: Crawl and filter URLs for {domain_name}{NC}")
    
    try:
        # Run crawling tools
        show_progress("Running GoSpider")
        with open(f"{domain_name}-gospider.txt", "w") as f:
            subprocess.run(["gospider", "-S", f"{domain_name}-domains.txt", "-c", "10", "-d", "5"], 
                         stdout=f, stderr=subprocess.PIPE, text=True)
        
        show_progress("Running Hakrawler")
        with open(f"{domain_name}-hakrawler.txt", "w") as f:
            subprocess.run(["hakrawler", "-d", "3"], 
                         stdin=open(f"{domain_name}-domains.txt"), 
                         stdout=f, stderr=subprocess.PIPE, text=True)
        
        show_progress("Running Katana")
        with open(f"{domain_name}-katana.txt", "w") as f:
            subprocess.run(["katana"], 
                         stdin=open(f"{domain_name}-domains.txt"), 
                         stdout=f, stderr=subprocess.PIPE, text=True)
        
        show_progress("Running Waybackurls")
        with open(f"{domain_name}-waybackurls.txt", "w") as f:
            subprocess.run(["waybackurls"], 
                         stdin=open(f"{domain_name}-domains.txt"), 
                         stdout=f, stderr=subprocess.PIPE, text=True)
        
        show_progress("Running Gau")
        with open(f"{domain_name}-gau.txt", "w") as f:
            subprocess.run(["gau"], 
                         stdin=open(f"{domain_name}-domains.txt"), 
                         stdout=f, stderr=subprocess.PIPE, text=True)
        
        # Process results
        show_progress("Processing results")
        all_urls = []
        for tool in ["gospider", "hakrawler", "katana", "waybackurls", "gau"]:
            with open(f"{domain_name}-{tool}.txt") as f:
                urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f.read())
                all_urls.extend(urls)
        
        total_merged_urls = len(all_urls)
        print(f"{BOLD_WHITE}Total URLs collected: {total_merged_urls}{NC}")
        
        # Save merged URLs
        with open(f"{domain_name}-links-final.txt", "w") as f:
            f.write("\n".join(all_urls))
        
        # Clean up
        for tool in ["gospider", "hakrawler", "katana", "waybackurls", "gau"]:
            os.remove(f"{domain_name}-{tool}.txt")
        
        print(f"{BOLD_BLUE}URL collection completed. Results saved to {domain_name}-links-final.txt{NC}")
        last_completed_option = 4
        
        # Continue to step 5
        run_step_5()
        
    except subprocess.CalledProcessError as e:
        handle_error_with_solution("URL crawling", "Check tool installations and network connection")

def run_step_5() -> None:
    global domain_name, last_completed_option
    
    if not domain_name:
        print("Domain name is not set. Please select option 2 first.")
        return
    
    print(f"{BOLD_WHITE}You selected: Filtering extensions from the URLs for {domain_name}{NC}")
    
    try:
        # Filter out unwanted extensions
        show_progress("Filtering extensions")
        extensions_to_exclude = [
            '.css', '.js', '.jpg', '.png', '.gif', '.jpeg', '.svg', 
            '.woff', '.woff2', '.ico', '.pdf', '.doc', '.docx', '.xls',
            '.xlsx', '.ppt', '.pptx', '.mp3', '.mp4', '.avi', '.mov',
            '.zip', '.tar', '.gz', '.rar', '.7z', '.exe', '.dll', '.deb'
        ]
        
        with open(f"{domain_name}-links-final.txt") as infile, \
             open(f"{domain_name}-links-clean.txt", "w") as outfile:
            for line in infile:
                line = line.strip()
                if not any(ext in line.lower() for ext in extensions_to_exclude):
                    outfile.write(line + "\n")
        
        # Filter domain-specific URLs
        show_progress("Filtering domain-specific URLs")
        with open(f"{domain_name}-links-clean.txt") as infile, \
             open(f"{domain_name}-links-clean1.txt", "w") as outfile:
            for line in infile:
                if domain_name in line:
                    outfile.write(line)
        
        # Clean up
        os.remove(f"{domain_name}-links-clean.txt")
        os.rename(f"{domain_name}-links-clean1.txt", f"{domain_name}-links-clean.txt")
        
        # Run URO to remove similar URLs
        show_progress("Running URO to remove similar URLs")
        subprocess.run(["uro", "-i", f"{domain_name}-links-clean.txt", "-o", f"{domain_name}-uro.txt"], check=True)
        
        # Final filtering
        show_progress("Final filtering")
        with open(f"{domain_name}-uro.txt") as infile, \
             open(f"{domain_name}-links.txt", "w") as outfile:
            seen = set()
            for line in infile:
                line = line.strip()
                if line and line not in seen:
                    seen.add(line)
                    outfile.write(line + "\n")
        
        # Clean up
        os.remove(f"{domain_name}-uro.txt")
        os.remove(f"{domain_name}-links-final.txt")
        
        print(f"{BOLD_BLUE}Filtering completed. Results saved to {domain_name}-links.txt{NC}")
        last_completed_option = 5
        
        # Continue to step 6
        run_step_6()
        
    except subprocess.CalledProcessError as e:
        handle_error_with_solution("URL filtering", "Check URO installation and input files")

def run_step_6() -> None:
    global domain_name, last_completed_option
    
    if not domain_name:
        print("Domain name is not set. Please select option 2 first.")
        return
    
    print(f"{BOLD_WHITE}You selected: Create new separated file for Arjun & SQLi testing for {domain_name}{NC}")
    
    try:
        # Separate URLs with parameters
        show_progress("Separating URLs with parameters")
        with open(f"{domain_name}-links.txt") as infile, \
             open("arjun-urls.txt", "w") as arjun_file, \
             open("output-php-links.txt", "w") as php_file:
            for line in infile:
                line = line.strip()
                if '?' in line:
                    php_file.write(line + "\n")
                elif any(ext in line.lower() for ext in ['.php', '.asp', '.aspx', '.jsp']):
                    arjun_file.write(line + "\n")
        
        # Run Arjun on parameter-less URLs
        if os.path.exists("arjun-urls.txt") and os.path.getsize("arjun-urls.txt") > 0:
            show_progress("Running Arjun on parameter-less URLs")
            subprocess.run(["arjun", "-i", "arjun-urls.txt", "-oT", "arjun_output.txt", "-t", "10"], check=True)
        
        # Merge results
        show_progress("Merging results")
        with open(f"urls-ready.txt", "w") as outfile:
            # Add original URLs with parameters
            if os.path.exists("output-php-links.txt"):
                with open("output-php-links.txt") as f:
                    outfile.write(f.read())
            
            # Add Arjun results
            if os.path.exists("arjun_output.txt"):
                with open("arjun_output.txt") as f:
                    outfile.write(f.read())
            
            # Add remaining URLs
            with open(f"{domain_name}-links.txt") as f:
                for line in f:
                    if '?' not in line and not any(ext in line.lower() for ext in ['.php', '.asp', '.aspx', '.jsp']):
                        outfile.write(line)
        
        # Clean up
        for fname in ["arjun-urls.txt", "output-php-links.txt", "arjun_output.txt", f"{domain_name}-links.txt"]:
            if os.path.exists(fname):
                os.remove(fname)
        
        print(f"{BOLD_BLUE}URL separation completed. Results saved to urls-ready.txt{NC}")
        last_completed_option = 6
        
        # Continue to step 7
        run_step_7()
        
    except subprocess.CalledProcessError as e:
        handle_error_with_solution("URL separation", "Check Arjun installation and input files")

def run_step_7() -> None:
    global domain_name, last_completed_option
    
    if not domain_name:
        print("Domain name is not set. Please select option 2 first.")
        return
    
    print(f"{BOLD_WHITE}You selected: Getting ready for XSS & URLs with query strings for {domain_name}{NC}")
    
    try:
        # Separate URLs with query parameters
        show_progress("Separating URLs with query parameters")
        with open("urls-ready.txt") as infile, \
             open(f"{domain_name}-query.txt", "w") as query_file, \
             open(f"{domain_name}-ALL-links.txt", "w") as all_file:
            for line in infile:
                line = line.strip()
                if '=' in line:
                    query_file.write(line + "\n")
                all_file.write(line + "\n")
        
        # Analyze query parameters for XSS potential
        show_progress("Analyzing query parameters for XSS potential")
        param_patterns = ['id', 'q', 'search', 'query', 'name', 'user', 'email']
        
        with open(f"{domain_name}-query.txt") as infile, \
             open("ibro-xss.txt", "w") as xss_file:
            seen_params = set()
            for line in infile:
                line = line.strip()
                if any(param in line.lower() for param in param_patterns):
                    xss_file.write(line + "\n")
                    # Extract and remember parameters to avoid duplicates
                    params = re.findall(r'\?([^#]+)', line)
                    if params:
                        seen_params.update(params[0].split('&'))
        
        # Finalize XSS targets
        show_progress("Finalizing XSS targets")
        os.rename("ibro-xss.txt", f"{domain_name}-query.txt")
        
        print(f"{BOLD_BLUE}XSS target preparation completed.{NC}")
        print(f"{BOLD_WHITE}Query URLs saved to {domain_name}-query.txt{NC}")
        print(f"{BOLD_WHITE}All URLs saved to {domain_name}-ALL-links.txt{NC}")
        last_completed_option = 7
        
        # Continue to step 8
        run_step_8()
        
    except Exception as e:
        handle_error_with_solution("XSS preparation", f"Error: {str(e)}")

def run_step_8() -> None:
    global domain_name
    
    if not domain_name:
        print("Domain name is not set. Please select option 2 first.")
        return
    
    print(f"{BOLD_WHITE}You selected: xss0r RUN for {domain_name}{NC}")
    
    try:
        # Check if xss-checker exists
        if not os.path.exists("xss-checker"):
            print(f"{RED}xss-checker not found in current directory.{NC}")
            print(f"{YELLOW}Please download it from: https://github.com/s0md3v/XSStrike{NC}")
            return
        
        # Check if payloads.txt exists
        if not os.path.exists("payloads.txt"):
            print(f"{RED}payloads.txt not found in current directory.{NC}")
            print(f"{YELLOW}Please create a payloads file or download one.{NC}")
            return
        
        # Check if we have query URLs to test
        if not os.path.exists(f"{domain_name}-query.txt"):
            print(f"{RED}No query URLs found to test.{NC}")
            return
        
        # Run xss-checker
        show_progress("Running xss-checker")
        subprocess.run([
            "./xss-checker",
            "--urls", f"{domain_name}-query.txt",
            "--payloads", "payloads.txt",
            "--shuffle",
            "--threads", "9"
        ], check=True)
        
        print(f"{BOLD_BLUE}XSS testing completed. Check the results.{NC}")
        last_completed_option = 8
        
    except subprocess.CalledProcessError as e:
        handle_error_with_solution("xss-checker", "Check XSStrike installation and configuration")

def main() -> None:
    global domain_name, last_completed_option
    
    # Clear screen
    os.system('clear')
    display_banner()
    
    while True:
        display_options()
        try:
            choice = int(input("Enter your choice [1-10]: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        
        if choice == 1:
            install_tools()
        elif choice == 2:
            domain_name = input("Please enter a domain name (example.com): ").strip()
            print(f"{BOLD_WHITE}Domain name set to {domain_name}{NC}")
            last_completed_option = 2
        elif choice == 3:
            if not domain_name:
                print("Please set domain name first (option 2)")
            else:
                run_step_3()
        elif choice == 4:
            if not domain_name:
                print("Please set domain name first (option 2)")
            elif last_completed_option < 3:
                print("Please complete domain enumeration first (option 3)")
            else:
                run_step_4()
        elif choice == 5:
            if not domain_name:
                print("Please set domain name first (option 2)")
            elif last_completed_option < 4:
                print("Please complete URL crawling first (option 4)")
            else:
                run_step_5()
        elif choice == 6:
            if not domain_name:
                print("Please set domain name first (option 2)")
            elif last_completed_option < 5:
                print("Please complete URL filtering first (option 5)")
            else:
                run_step_6()
        elif choice == 7:
            if not domain_name:
                print("Please set domain name first (option 2)")
            elif last_completed_option < 6:
                print("Please complete URL separation first (option 6)")
            else:
                run_step_7()
        elif choice == 8:
            if not domain_name:
                print("Please set domain name first (option 2)")
            elif last_completed_option < 7:
                print("Please complete XSS preparation first (option 7)")
            else:
                run_step_8()
        elif choice == 9:
            print("Exiting...")
            sys.exit(0)
        elif choice == 10:
            print("VPS help information would be displayed here")
        else:
            print("Option not yet implemented")

if __name__ == "__main__":
    main()
