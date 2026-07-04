import os
import time
# Import the modern Google GenAI SDK
from google import genai

class CodebaseCrawler:
    """Recursively crawls a target directory to extract valid source code files."""
    
    def __init__(self, target_directory: str):
        self.target_directory = target_directory
        # Folders we must skip to prevent flooding the LLM context with build junk
        self.ignored_dirs = {'bin', 'obj', '.git', '.vs', 'packages', 'node_modules'}

    def extract_source_pool(self, extension: str = ".cs") -> str:
        """Finds all files matching the target extension and bundles them into one string."""
        combined_payload = ""
        
        for root, dirs, files in os.walk(self.target_directory):
            # In-place slice modification to skip ignored folders entirely
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
            
            for file in files:
                if file.endswith(extension):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            combined_payload += f"\n\n// ==========================================\n"
                            combined_payload += f"// FILE SOURCE: {file_path}\n"
                            combined_payload += f"// ==========================================\n\n"
                            combined_payload += f.read()
                    except Exception as e:
                        print(f"⚠️ Skipping unreadable file {file_path}: {e}")
                        
        return combined_payload


class AutomationOrchestrator:
    """Ties the codebase payload together with agent prompt configurations using google.genai."""
    
    def __init__(self, api_key: str, source_payload: str):
        # Explicit initialization for modern SDK standards
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'
        self.source_payload = source_payload

    def execute_agent(self, manifest_path: str, output_destination: str, max_retries: int = 3, initial_delay: int = 5):
        """Executes a pipeline run with an automatic exponential backoff retry mechanism for 503 limits."""
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Missing required agent manifest: {manifest_path}")

        with open(manifest_path, "r", encoding="utf-8") as f:
            agent_instructions = f.read()

        execution_context = (
            f"{agent_instructions}\n\n"
            f"--- START TARGET SOURCE CODEBASE ---\n"
            f"{self.source_payload}\n"
            f"--- END TARGET SOURCE CODEBASE ---"
        )

        print(f"🚀 Dispatching task using manifest [{manifest_path}]...")
        
        delay = initial_delay
        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=execution_context,
                )
                
                with open(output_destination, "w", encoding="utf-8") as out:
                    out.write(response.text)
                    
                print(f"✅ Success! Deliverable exported cleanly to: {output_destination}\n")
                
                # Mandatory cooling pause to prevent hitting rate controls on subsequent calls
                time.sleep(2) 
                return 

            except Exception as e:
                if "503" in str(e) or "demand" in str(e).lower():
                    if attempt < max_retries:
                        print(f"⚠️ Server busy (503). Retrying attempt {attempt}/{max_retries} in {delay} seconds...")
                        time.sleep(delay)
                        delay *= 2  
                    else:
                        print(f"❌ Critical Pipeline Failure after {max_retries} attempts: {e}")
                else:
                    print(f"❌ Non-retryable Pipeline Failure: {e}")
                    break


if __name__ == "__main__":
    # ==================================================
    # RUNTIME PIPELINE EXECUTION CONFIGURATION
    # ==================================================
    
    # Load environment variables (create a .env file or set system variables)
    USER_API_KEY = os.getenv("USER_API_KEY")
    PROJECT_TARGET = os.getenv("PROJECT_TARGET")
    
    # Validate required environment variables
    if not USER_API_KEY:
        raise ValueError(
            "❌ Missing USER_API_KEY environment variable. "
            "Set it in your .env file or system environment. "
            "Get a free key from: https://aistudio.google.com/app/apikey"
        )
    
    if not PROJECT_TARGET:
        raise ValueError(
            "❌ Missing PROJECT_TARGET environment variable. "
            "Set it in your .env file or system environment."
        )
    
    print("==================================================")
    print(f"🔍 Analyzing source repository target: [{PROJECT_TARGET}]")
    print("==================================================")
    
    # Instantiate the crawler (defined at the top)
    crawler = CodebaseCrawler(target_directory=PROJECT_TARGET)
    code_text = crawler.extract_source_pool(extension=".cs")
    
    if not code_text.strip():
        print(f"❌ Automation Halted: No target files found in '{PROJECT_TARGET}'. Verify directory path.")
    else:
        print(f"📦 Codebase parsed. Total Payload: {len(code_text)} characters.")
        print("==================================================\n")
        
        # Initialize the Orchestrator with your payload
        orchestrator = AutomationOrchestrator(api_key=USER_API_KEY, source_payload=code_text)
        
        # Deploy Agent 1: The LaTeX Document Publisher
        orchestrator.execute_agent(
            manifest_path="prompt_manifests/agent_latex.md", 
            output_destination="ACADEMIC_REPORT.tex"
        )
        
        # Deploy Agent 2: Premium Portfolio Readme Page
        orchestrator.execute_agent(
            manifest_path="prompt_manifests/agent_readme.md", 
            output_destination="README_PREMIUM.md"
        )
        
        # Deploy Agent 3: Static Structural Code Review & Quality Audit
        orchestrator.execute_agent(
            manifest_path="prompt_manifests/agent_code_review.md", 
            output_destination="CODE_QUALITY_AUDIT.md"
        )
        
        # Deploy Agent 4: XML Header Comments Manifest (Updated to Markdown format)
        orchestrator.execute_agent(
            manifest_path="prompt_manifests/agent_xml_doc.md", 
            output_destination="AUTO_XML_DOCUMENTATION.md"
        )
        
        print("🎉 [DocuAgentSuite] Multi-Agent generation loop fully complete.")