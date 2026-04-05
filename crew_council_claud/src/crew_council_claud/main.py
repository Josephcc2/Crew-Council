#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from crew_council_claud.crew import CrewCouncilClaud

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

#inputTopic = 'Effects of Caffeine on Sleep'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

topic_path = os.path.join(BASE_DIR, "..", "..", "..", "Topic.txt")
with open(topic_path, "r", encoding="utf-8") as f:
    inputTopic = f.read().strip()

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': inputTopic,
        'current_year': str(datetime.now().year)
    }

    try:
        CrewCouncilClaud().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": inputTopic,
        'current_year': str(datetime.now().year)
    }
    try:
        CrewCouncilClaud().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewCouncilClaud().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": inputTopic,
        "current_year": str(datetime.now().year)
    }

    try:
        CrewCouncilClaud().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = CrewCouncilClaud().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
