# types.py
REFLEX_TASK = 1
"""
These tasks involve immediate responses to specific stimuli based on predefined rules. 
The agent does not consider past experiences or future consequences, making decisions purely based on the current percept.

Examples:
Automated customer support responses based on keyword detection.
Basic control systems like thermostats or simple robots.

Key Characteristics:
Reactive: Responds directly to current inputs.
Rule-Based: Follows condition-action rules.
Limited Scope: Suitable for stable environments with clear rules.
"""

MODEL_REFLEX_TASK = 2
"""
These tasks involve using an internal model of the environment to make decisions. 
The agent maintains a representation of the world and uses it to predict future states and outcomes.

Examples:
Navigation systems that use maps and sensor data to plan routes.
Predictive maintenance systems in industrial settings.

Key Characteristics:
Predictive: Uses models to anticipate future states.
Stateful: Maintains an internal representation of the environment.
Adaptive: Can adjust actions based on changes in the environment.
"""

GOAL_ORIENTED_TASK = 3
"""
These tasks are driven by specific objectives. The agent evaluates different actions to determine the best way to achieve
its goals, often using search algorithms and planning techniques.

Examples:
Autonomous vehicles planning routes to reach a destination.
Robotic systems performing complex assembly tasks.

Key Characteristics:
Objective-Oriented: Focuses on achieving specific goals.
Planning: Uses logic and search algorithms to determine actions.
Flexible: Can adapt plans based on new information.
"""
UTILITY_DRIVEN_TASK = 4
"""
These tasks involve making decisions based on the expected utility or value of different outcomes. 
The agent evaluates various options and selects the one that maximizes overall benefit.

Examples:
Recommendation systems suggesting products based on user preferences.
Financial trading systems optimizing investment portfolios.

Key Characteristics:
Value-Driven: Considers the utility of different actions.
Comparative: Weighs options to maximize benefits.
Dynamic: Adjusts decisions based on changing utility values.
"""

LEARNING_TASK = 5
"""
These tasks involve the agent improving its performance over time through learning from experiences. 
The agent uses feedback from its actions to refine its decision-making processes.

Examples:
Machine learning models improving predictions based on new data.
Adaptive user interfaces personalizing experiences based on user behavior.

Key Characteristics:
Adaptive: Learns from past experiences.
Feedback-Driven: Uses feedback to improve performance.
Evolving: Continuously updates its knowledge and strategies.
"""