import unittest
import os
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents.routers import TaskComplexityRouter

class TestTaskComplexityRouter(unittest.TestCase):
    def setUp(self):
        BASE_URL = "http://localhost:1234/v1"
        YI_LARGE_API_KEY = os.getenv("YI_LARGE_API_KEY")

        # Create instances of RexiaAIOpenAI for each LLM
        self.base_llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="yi-1.5",
            temperature=0,
        )

        self.router_llm = RexiaAIOpenAI(
            base_url=BASE_URL,
            model="yi-1.5",
            temperature=0,
        )

        self.complex_llm = RexiaAIOpenAI(
            base_url="https://api.01.ai/v1",
            model="yi-large",
            temperature=0,
            api_key=YI_LARGE_API_KEY,
        )

        self.router = TaskComplexityRouter(
            base_llm=self.base_llm,
            complex_llm=self.complex_llm,
            router_llm=self.router_llm,
            task_complexity_threshold=50
        )

    def test_route_simple_task(self):
        task = "Classify this movie review as positive or negative: 'I loved this film! The acting was superb and the plot kept me engaged throughout.'"
        complexity_score = self.router.route(task)
        
        self.assertGreaterEqual(complexity_score, 1)
        self.assertLessEqual(complexity_score, 50)

    def test_route_complex_task(self):
        task = """Write a 500-word explanation of how photosynthesis works in plants, 
                  including the light-dependent and light-independent reactions. Describe the role of chlorophyll, 
                  the importance of water and carbon dioxide, and how the process produces glucose and oxygen. 
                  Then, discuss how this process impacts the global carbon cycle and its significance for life on Earth."""
        complexity_score = self.router.route(task)
        
        self.assertGreaterEqual(complexity_score, 51)
        self.assertLessEqual(complexity_score, 100)

if __name__ == "__main__":
    unittest.main()