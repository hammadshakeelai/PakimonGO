import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.runner import JobRunner

def test_job_runner_registers_and_runs():
    runner = JobRunner()
    
    def dummy_handler(payload):
        return payload.get("value", 0) * 2

    runner.register("dummy_job", dummy_handler)
    result = runner.run("dummy_job", {"value": 5})
    
    assert result == 10
