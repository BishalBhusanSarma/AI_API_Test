# TEST STRATEGY
**Project:** FastAPI Leave Management API & AI Leave Assistant

### 1. Testing Objectives
- Verify API functionality, business rules, data integrity and access controls.
- Evaluate the AI Assistant's ability to understand employee requests, prepare leave drafts, answer policy questions and request clarification.
- Identify functional, security, privacy and AI-related defects.
- Assess the reliability and consistency of AI-generated responses.

### 2. Scope of Testing
**Leave Management API**
- `POST /leave` – Create leave requests.
- `GET /leave/{id}` – Retrieve leave requests.
- `PUT /leave/{id}/approve` – Approve leave requests.
- Validate the 20-day annual leave limit, overlapping requests, inclusive date calculation, cross-year leave, supported leave types (casual, sick and earned), manager-only approval and employee-specific data access.

**AI Leave Assistant**
- `POST /ai/chat` – Process employee messages and provide assistance.
- Test normal requests, ambiguous dates, missing information, spelling mistakes, mixed languages, policy questions, out-of-scope queries, prompt injection and privacy-related scenarios.
- Verify that the assistant does not submit, approve or reject leave requests or disclose another employee's private information.

### 3. Testing Approach
**API Testing:** Prepare 31 manual test cases and automate 16 selected high-priority scenarios using Python, Pytest and Requests. Coverage includes functional, negative, boundary, edge-case, authentication and authorization testing. Validate HTTP status codes, response data and business rules.

**AI Testing:** Prepare a dataset of 30 prompts with expected behaviour and pass criteria. Execute each prompt against the AI endpoint and store actual responses in `actual_responses.json`. Use a separate Groq-based LLM evaluator to compare actual responses against expected behaviour and generate PASS/FAIL results in `result.json`.

**Defect Management:** Document identified defects with severity, reproduction steps, expected and actual results, supporting evidence and suggested fixes. Review LLM evaluation failures before classifying them as product defects.

### 4. Test Environment and Tools
- **Backend:** Python, FastAPI
- **API Automation:** Pytest, Requests
- **AI Model:** Groq API – Llama 3.3
- **Test Data:** CSV and JSON
- **Reporting:** JSON evaluation report and defect reports
- **Execution:** Local development environment

### 5. Entry and Exit Criteria
**Entry Criteria**
- API and AI endpoints are accessible.
- Test cases, test prompts and expected results are prepared.
- Authentication tokens, dependencies and required API credentials are available.

**Exit Criteria**
- Planned API test cases have been executed and results recorded.
- All AI evaluation prompts have recorded outcomes or documented execution errors.
- Defects and test execution issues are documented.
- Critical security and authorization behaviours are verified against backend enforcement.
- Outstanding failures and limitations are reported.

### 6. Risks and Limitations
- LLM responses may vary between executions due to non-deterministic behaviour.
- LLM-based evaluation may produce incorrect judgments and requires review.
- API failures, timeouts or invalid responses may affect evaluation results.
- Prompt instructions alone cannot guarantee security; authorization and privacy must be enforced by the backend.
- Testing is limited to the prepared test cases and AI evaluation dataset and does not represent complete production validation.

### 7. Metrics and CI Considerations
**Metrics:** API test pass rate, number of passed/failed tests, AI evaluation pass rate, defect count by severity and execution errors.

**CI Proposal:** Integrate automated API tests into a CI pipeline to execute on code changes. Generate test reports and flag failed tests. Run AI evaluations separately and monitor their results, considering LLM variability.

### 8. Deliverables
- Test strategy document.
- 31 manual API test cases and 16 automated test scenarios.
- Pytest automation scripts and execution results.
- 30-prompt AI evaluation dataset.
- Actual response JSON and AI evaluation report.
- Defect reports and test summary.
- AI usage disclosure.