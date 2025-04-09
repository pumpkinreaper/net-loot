#!/usr/bin/env python3
import sys
import time
import random
from colorama import Fore, Style, init
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PromptStyle
from googlesearch import search

# Initialize colorama with auto-conversion for Windows terminals
init(convert=True)

class GoogleDorker:
    def __init__(self):
        self.params = {
            "title": "",
            "site": "",
            "filetype": "",
            "inurl": "",
            "intext": "",
            "intitle": "",
            "link": "",
            "before": "",
            "after": "",
            "exclude": ""
        }
        self.results = []
        self.prompt_style = PromptStyle.from_dict({
            'prompt': '#ff0066 bold',
            'completion': 'bg:#008800 #ffffff',
        })
        self.commands = ["set", "clear", "show", "run", "help", "exit"]
        self.command_completer = WordCompleter([
            "set title:", "set site:", "set filetype:", "set inurl:", "set intext:",
            "set intitle:", "set link:", "set before:", "set after:", "set exclude:",
            "set results:", "clear", "show", "run", "help", "exit"
        ])
        self.session = PromptSession(completer=self.command_completer, style=self.prompt_style)
        self.num_results = 10  # Default number of results to return
        self.pause_time = 3  # Default pause between searches to avoid blocking

    def set_param(self, param, value):
        """Set a search parameter"""
        if param in self.params:
            self.params[param] = value
            print(f"{Fore.GREEN}Set {param}: {value}{Style.RESET_ALL}")
        elif param == "results":
            try:
                self.num_results = int(value)
                print(f"{Fore.GREEN}Set number of results to: {value}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid value for results. Must be a number.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Unknown parameter: {param}{Style.RESET_ALL}")

    def clear_params(self):
        """Clear all search parameters"""
        for param in self.params:
            self.params[param] = ""
        print(f"{Fore.YELLOW}All parameters cleared!{Style.RESET_ALL}")

    def show_params(self):
        """Show current search parameters"""
        print(f"\n{Fore.CYAN}Current search parameters:{Style.RESET_ALL}")
        for param, value in self.params.items():
            if value:
                print(f"{Fore.GREEN}{param}: {value}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Number of results: {self.num_results}{Style.RESET_ALL}")
        print()

    def build_query(self):
        """Build Google search query from parameters"""
        query_parts = []
        
        if self.params["title"]:
            query_parts.append(f"intitle:\"{self.params['title']}\"")
        
        if self.params["intitle"]:
            query_parts.append(f"intitle:\"{self.params['intitle']}\"")
            
        if self.params["site"]:
            query_parts.append(f"site:{self.params['site']}")
            
        if self.params["filetype"]:
            query_parts.append(f"filetype:{self.params['filetype']}")
            
        if self.params["inurl"]:
            query_parts.append(f"inurl:{self.params['inurl']}")
            
        if self.params["intext"]:
            query_parts.append(f"intext:\"{self.params['intext']}\"")
            
        if self.params["link"]:
            query_parts.append(f"link:{self.params['link']}")
            
        if self.params["before"]:
            query_parts.append(f"before:{self.params['before']}")
            
        if self.params["after"]:
            query_parts.append(f"after:{self.params['after']}")
            
        if self.params["exclude"]:
            for term in self.params["exclude"].split():
                query_parts.append(f"-{term}")
                
        return " ".join(query_parts)

    def execute_search(self, query):
        """Execute search using googlesearch-python"""
        if not query:
            print(f"{Fore.YELLOW}Empty query. Please set search parameters.{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}Searching for: {query}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Fetching {self.num_results} results. This may take a moment...{Style.RESET_ALL}")
        
        try:
            # Use the googlesearch library to get results
            results = list(search(
                query, 
                num_results=self.num_results,
                lang="en",
                advanced=True
            ))
            
            if not results:
                print(f"{Fore.YELLOW}No results found.{Style.RESET_ALL}")
                return
                
            print(f"\n{Fore.CYAN}Found {len(results)} results:{Style.RESET_ALL}\n")
            
            for i, result in enumerate(results, 1):
                print(f"{Fore.GREEN}[{i}] {result.title}{Style.RESET_ALL}")
                print(f"{Fore.BLUE}{result.url}{Style.RESET_ALL}")
                if hasattr(result, 'description') and result.description:
                    print(f"{result.description}\n")
                else:
                    print()
                    
                # Add small random delay between displaying results
                time.sleep(random.uniform(0.1, 0.3))
                
        except Exception as e:
            print(f"{Fore.RED}Error executing search: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Google may be blocking automated queries. Try changing your IP or waiting.{Style.RESET_ALL}")

    def print_help(self):
        """Print help information"""
        help_text = f"""
{Fore.CYAN}NET-LOOT GOOGLE DORKING CLI{Style.RESET_ALL}

{Fore.YELLOW}Commands:{Style.RESET_ALL}
  {Fore.GREEN}set [param]:[value]{Style.RESET_ALL} - Set search parameter
    Available parameters:
      - title: Search for pages with specific title
      - site: Limit search to specific domain
      - filetype: Limit search to specific file types (pdf, doc, xls, etc.)
      - inurl: Search for URLs containing specific text
      - intext: Search for pages containing specific text
      - intitle: Search for pages with specific text in title
      - link: Search for pages that link to specific URL
      - before: Search for pages indexed before date (YYYY-MM-DD)
      - after: Search for pages indexed after date (YYYY-MM-DD)
      - exclude: Terms to exclude from search (space separated)
      - results: Number of results to return (default: 10)
  
  {Fore.GREEN}clear{Style.RESET_ALL} - Clear all search parameters
  {Fore.GREEN}show{Style.RESET_ALL} - Show current search parameters
  {Fore.GREEN}run{Style.RESET_ALL} - Execute search with current parameters
  {Fore.GREEN}help{Style.RESET_ALL} - Show this help information
  {Fore.GREEN}exit{Style.RESET_ALL} - Exit the program
        """
        print(help_text)

    def run(self):
        """Main CLI loop"""
        print(f"{Fore.RED}╔═══════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.RED}║         💀 NET-LOOT DORKING CLI 💀            ║{Style.RESET_ALL}")
        print(f"{Fore.RED}║     Type 'help' for available commands        ║{Style.RESET_ALL}")
        print(f"{Fore.RED}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}Dork responsibly...{Style.RESET_ALL}")
        
        while True:
            try:
                user_input = self.session.prompt("💀 net-loot> ")
                
                if user_input.strip() == "":
                    continue
                    
                cmd_parts = user_input.strip().split(" ", 1)
                cmd = cmd_parts[0].lower()
                
                if cmd == "exit":
                    print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
                    break
                    
                elif cmd == "help":
                    self.print_help()
                    
                elif cmd == "clear":
                    self.clear_params()
                    
                elif cmd == "show":
                    self.show_params()
                    
                elif cmd == "run":
                    query = self.build_query()
                    if query:
                        print(f"\n{Fore.CYAN}Search query:{Style.RESET_ALL} {query}")
                        confirm = input(f"\n{Fore.YELLOW}Does this query look good? (y/n): {Style.RESET_ALL}").lower()
                        if confirm in ["y", "yes"]:
                            self.execute_search(query)
                    else:
                        print(f"{Fore.YELLOW}No search parameters set. Use 'set' command to define search criteria.{Style.RESET_ALL}")
                        
                elif cmd == "set" and len(cmd_parts) > 1:
                    param_parts = cmd_parts[1].split(":", 1)
                    if len(param_parts) == 2:
                        param, value = param_parts[0].strip(), param_parts[1].strip()
                        self.set_param(param, value)
                    else:
                        print(f"{Fore.RED}Invalid format. Use 'set param:value'{Style.RESET_ALL}")
                        
                else:
                    print(f"{Fore.RED}Unknown command: {cmd}{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' to quit{Style.RESET_ALL}")
            except EOFError:
                print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
                break

def main():
    dorker = GoogleDorker()
    dorker.run()

if __name__ == "__main__":
    main()