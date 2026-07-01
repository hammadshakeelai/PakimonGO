class JobRunner:
    def __init__(self):
        self.jobs = {}

    def register(self, job_name, handler):
        self.jobs[job_name] = handler

    def run(self, job_name, payload):
        if job_name in self.jobs:
            return self.jobs[job_name](payload)
        raise ValueError(f"Job {job_name} not found")

# Example idempotency-aware interface doc
# All handlers must ensure processing the same payload multiple times yields the same state.
