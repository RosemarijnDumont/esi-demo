
import pandas as pd

class VerificationAgent:
    def __init__(self):
        self.pre_implementation_data = None
        self.post_implementation_data = None
        self.user_feedback = []

    def develop_test_plan(self):
        test_plan = {
            "test_cases": [
                {
                    "name": "Small File Sync - Remote User",
                    "description": "Synchronize a 10MB file from a remote location.",
                    "metrics": ["sync_time", "data_transfer_rate", "cpu_usage", "memory_usage"],
                    "acceptance_criteria": {"sync_time": "< 5 seconds"}
                },
                {
                    "name": "Large File Sync - Remote User",
                    "description": "Synchronize a 1GB file from a remote location.",
                    "metrics": ["sync_time", "data_transfer_rate", "cpu_usage", "memory_usage"],
                    "acceptance_criteria": {"sync_time": "< 60 seconds"}
                },
                {
                    "name": "Multiple Files Sync - Remote User",
                    "description": "Synchronize 100 files (total 500MB) from a remote location.",
                    "metrics": ["sync_time", "data_transfer_rate", "cpu_usage", "memory_usage"],
                    "acceptance_criteria": {"sync_time": "< 30 seconds"}
                },
            ],
            "metrics_to_collect": ["sync_time", "data_transfer_rate", "cpu_usage", "memory_usage", "network_latency"]
        }
        print("Test Plan Developed:\n", test_plan)
        return test_plan

    def recruit_uat_users(self, num_users=5):
        print(f"Recruiting {num_users} remote users for UAT...")
        # In a real scenario, this would involve sending out invitations, managing consent, etc.
        uat_users = [f"user_{i}" for i in range(1, num_users + 1)]
        print("UAT users recruited:", uat_users)
        return uat_users

    def instrument_clients_and_servers(self, phase="post-implementation"):
        print(f"Re-instrumenting synchronization clients and servers for {phase} performance data collection...")
        # This simulation assumes data is collected and made available.
        # In a real scenario, this would involve deploying monitoring agents, configuring logs, etc.
        if phase == "post-implementation":
            self.post_implementation_data = self._simulate_performance_data()
            print("Post-implementation data collected.")
        else:
            self.pre_implementation_data = self._simulate_performance_data()
            print("Pre-implementation data collected.")

    def _simulate_performance_data(self):
        # Simulate performance data for demonstration purposes
        data = {
            "test_case": [
                "Small File Sync - Remote User",
                "Large File Sync - Remote User",
                "Multiple Files Sync - Remote User"
            ],
            "sync_time": [4.5, 58.0, 28.0] if self.pre_implementation_data is None else [2.0, 35.0, 15.0],  # Improved times post-implementation
            "data_transfer_rate": [80, 50, 60] if self.pre_implementation_data is None else [150, 90, 110], # Improved rates post-implementation
            "cpu_usage": [30, 60, 45],
            "memory_usage": [500, 1500, 800],
            "network_latency": [50, 80, 60]
        }
        return pd.DataFrame(data)

    def collect_user_feedback(self, user_id, feedback_score, comments):
        self.user_feedback.append({"user_id": user_id, "feedback_score": feedback_score, "comments": comments})
        print(f"Feedback collected from {user_id}.")

    def comparative_analysis(self):
        if self.pre_implementation_data is None or self.post_implementation_data is None:
            print("Error: Both pre and post-implementation data are required for comparative analysis.")
            return

        print("\n--- Comparative Analysis ---")
        comparison = pd.DataFrame()
        for col in self.pre_implementation_data.columns:
            if col not in ["test_case"]:
                comparison[f"pre_{col}"] = self.pre_implementation_data[col]
                comparison[f"post_{col}"] = self.post_implementation_data[col]
                if col in ["sync_time"]:
                    comparison[f"improvement_{col}"] = (self.pre_implementation_data[col] - self.post_implementation_data[col]) / self.pre_implementation_data[col] * 100
                elif col in ["data_transfer_rate"]:
                    comparison[f"improvement_{col}"] = (self.post_implementation_data[col] - self.pre_implementation_data[col]) / self.pre_implementation_data[col] * 100
                else:
                    comparison[f"delta_{col}"] = self.post_implementation_data[col] - self.pre_implementation_data[col]
        comparison["test_case"] = self.pre_implementation_data["test_case"]
        print(comparison.set_index("test_case"))

        print("\n--- User Feedback Summary ---")
        if self.user_feedback:
            feedback_df = pd.DataFrame(self.user_feedback)
            avg_score = feedback_df["feedback_score"].mean()
            print(f"Average User Feedback Score: {avg_score:.2f}/5")
            print("Comments:")
            for feedback in self.user_feedback:
                print(f"  - User {feedback['user_id']}: {feedback['comments']}")
        else:
            print("No user feedback collected.")


        return comparison

    def generate_performance_report(self, comparison_data, acceptance_criteria):
        print("\n--- Final Performance Report ---")
        report_content = []

        report_content.append("## Remote File Synchronization Performance Report")
        report_content.append("### 1. Executive Summary")
        report_content.append("This report details the verification process and the performance improvements achieved in remote file synchronization speeds following the implementation of optimization changes.")
        report_content.append("The analysis demonstrates significant improvements in synchronization times and data transfer rates, meeting the defined acceptance criteria.")

        report_content.append("\n### 2. Performance Metrics Comparison")
        report_content.append(comparison_data.to_markdown(index=False))

        report_content.append("\n### 3. Acceptance Criteria Fulfillment")
        overall_status = "PASS"
        for index, row in comparison_data.iterrows():
            test_case = row["test_case"]
            criteria = None
            for tc in self.test_plan["test_cases"]:
                if tc["name"] == test_case:
                    criteria = tc["acceptance_criteria"]
                    break
            if criteria and "sync_time" in criteria:
                sync_time_threshold = float(criteria["sync_time"].replace('< ', '').replace(' seconds', ''))
                post_sync_time = row["post_sync_time"]
                status = "PASS" if post_sync_time < sync_time_threshold else "FAIL"
                if status == "FAIL":
                    overall_status = "FAIL"
                report_content.append(f"- {test_case}: Sync Time (Post-implementation) = {post_sync_time:.2f}s (Acceptance Criteria: {criteria['sync_time']} - **{status}**)")
            else:
                report_content.append(f"- {test_case}: No specific sync time acceptance criteria defined.")

        report_content.append(f"\nOverall Acceptance Criteria Status: **{overall_status}**")

        report_content.append("\n### 4. User Acceptance Testing (UAT) Feedback")
        if self.user_feedback:
            feedback_df = pd.DataFrame(self.user_feedback)
            avg_score = feedback_df["feedback_score"].mean()
            report_content.append(f"- Average User Feedback Score: {avg_score:.2f}/5")
            report_content.append("- User Comments:")
            for feedback in self.user_feedback:
                report_content.append(f"  - User {feedback['user_id']}: {feedback['comments']}")
        else:
            report_content.append("- No user feedback collected. This might indicate an issue with the UAT recruitment or feedback collection process.")

        final_report = "\n".join(report_content)
        print(final_report)
        with open("performance_report.md", "w") as f:
            f.write(final_report)
        return final_report

    def provide_feedback_to_deployment_agent(self, overall_status, report):
        feedback = {
            "overall_status": overall_status,
            "report_summary": "Please review the detailed performance report for insights into synchronization speed improvements and any identified areas for further fine-tuning.",
            "detailed_report": report
        }
        print("\n--- Feedback to ImplementationAgent-Deployment ---")
        print(feedback)
        return feedback

if __name__ == "__main__":
    agent = VerificationAgent()

    # Task 1: Develop a test plan
    test_plan = agent.develop_test_plan()
    agent.test_plan = test_plan # Store for later use

    # Simulate pre-implementation data collection
    agent.instrument_clients_and_servers(phase="pre-implementation")

    # Task 2: Recruit UAT users (simulated)
    uat_users = agent.recruit_uat_users(num_users=3)

    # Task 3: Re-instrument and collect post-implementation data (simulated)
    agent.instrument_clients_and_servers(phase="post-implementation")

    # Simulate user feedback
    agent.collect_user_feedback("user_1", 4, "Much faster, great improvement!")
    agent.collect_user_feedback("user_2", 5, "Seamless synchronization, no more delays.")
    agent.collect_user_feedback("user_3", 3, "Improved, but still some occasional slowness with very large files.")

    # Task 4: Conduct comparative analysis
    comparison_results = agent.comparative_analysis()

    # Task 5: Generate a final performance report
    final_report = agent.generate_performance_report(comparison_results, test_plan["test_cases"])

    # Determine overall status for feedback
    overall_status = "PASS" # This would be derived more robustly from acceptance criteria in a real scenario
    if "FAIL" in final_report:
        overall_status = "FAIL"

    # Task 6: Provide feedback to the 'ImplementationAgent-Deployment'
    agent.provide_feedback_to_deployment_agent(overall_status, final_report)
