import requests
import json

class ResearchAgenticAI:
    def __init__(self, api_key, model="llama-3.1-8b-instant"):
        self.api_key = api_key
        self.model = model
        self.history = []  # Track previous interactions to make decisions
        self.API_URL = "https://api.groq.com/openai/v1/chat/completions"

    def query_model(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "n": 1  # Requesting multiple responses (n=3) for a more comprehensive data collection
        }
        
        response = requests.post(self.API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return [choice['message']['content'] for choice in result['choices']]  # Return all responses
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def adapt_query(self, topic):
        """Generate a query based on the input topic dynamically."""
        return f"Can you tell me everything about {topic} all you know about it ?"  # General query for in-depth research

    def run_agent(self, topic):
        print(f"Initial topic: {topic}")
        
        # Generate an adaptive query based on the user's topic
        query = self.adapt_query(topic)
        print(f"Generated query: {query}")
        
        # Collecting multiple pieces of data related to the topic
        responses = self.query_model(query)
        
        if responses:
            collected_data = "\n".join(responses)  # Combine all the responses into a single string
            print(f"Collected Data: {collected_data}")
            self.history.append({"query": query, "responses": responses})
            
            return collected_data
        else:
            print("Failed to retrieve data.")
            return None


class SummarizerAgent:
    def __init__(self, api_key, model="llama-3.1-8b-instant"):
        self.api_key = api_key
        self.model = model
        self.API_URL = "https://api.groq.com/openai/v1/chat/completions"

    def summarize_content(self, content):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Asking the model to summarize in simple, short language
        prompt = f"Summarize the following content in a very short and simple way, using easy words:\n{content}"

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "n": 1  # Only requesting one summary
        }

        response = requests.post(self.API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def evaluate_summary(self, original_content, summary):
        """A simple evaluation to check if the summary is concise and relevant."""
        if summary:
            print(f"Evaluating the summary...")

            # Ensure the summary is shorter and reflects the content well
            if len(summary.split()) < len(original_content.split()):
                print("Summary is concise and acceptable.")
                return True
            else:
                print("Summary might be too long or not clear enough.")
                return False
        else:
            return False


class EvaluationAgent:
    def __init__(self):
        pass
    
    def cross_check_summary(self, original_data, summary):
        """Check if the summary aligns with the key points of the original content."""
        if summary and original_data:
            print("Cross-checking the summary against the original data...")
            
            # For simplicity, we can check if the summary mentions key phrases from the original content
            if any(keyword in summary for keyword in original_data.split()[:20]):  # Check for early keywords in content
                print("Summary is aligned with the original content.")
                return True
            else:
                print("Summary does not align well with the original content.")
                return False
        else:
            print("Invalid summary or data.")
            return False


# Initialize both agents
api_key = "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"

# Research Agent
research_agent = ResearchAgenticAI(api_key)

# Summarizer Agent
summarizer_agent = SummarizerAgent(api_key)

# Evaluation Agent
evaluation_agent = EvaluationAgent()

# Get topic input from the usern
user_query = input("Enter a topic you want to know about: ")

# Run the Research Agent
collected_data = research_agent.run_agent(user_query)

if collected_data:
    # Pass the content to the Summarizer Agent for summarization
    print(f"Summarizing the collected content...")
    summary = summarizer_agent.summarize_content(collected_data)
    
    if summary:
        print(f"Summary: {summary}")
        
        # Evaluate if the summary is acceptable
        is_accepted = evaluation_agent.cross_check_summary(collected_data, summary)
        
        if is_accepted:
            print(f"Final accepted summary: {summary}")
        else:
            print("Summary is not accepted, further adjustments needed.")
else:
    print("No response from Research Agent. No summarization can be performed.")
