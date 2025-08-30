# Wellness Tracking Backend Service

This project is a backend service for managing a personal wellness tracking system. It handles tracking of wellness-related activities such as meditation, workouts, hydration, and sleep sessions.

## 📚 Features
- Implement at least one core API endpoint — for example, to **log a wellness activity**, **retrieve historical activity logs**, or **generate aggregated progress summaries** (e.g., daily/weekly totals). You may choose which functionality to prioritize.

- Integrate with the mock API `GET /device-activity` to simulate syncing wearable device data into your system. You may treat this as a background job or manual sync step.

- You are encouraged to add additional endpoints if they improve the overall design or user experience.

- Include test cases or test scripts to demonstrate that your backend service functions as expected.

## 🔌 Mock API Integration

#### **Endpoint**
`GET /device-activity`

#### **Purpose**
Retrieve wellness data collected by a wearable device.

#### **Response Format**
Here is a sample response. Feel free to modify or extend.
```json
[
  {
    "user_id": "789",
    "date": "2025-01-10",
    "hydration_liters": 1.5,
    "sleep_hours": 6.5,
    "exercise_minutes": 30,
    "meditation_minutes": 10
  }
]
```

## 🛠 Tech Requirements
You may use any tech stack of your choice. However, your project must use a database.

## 🧪 Documentation & Testing
TODO

## Assumptions
In cases where the problem description is ambiguous or incomplete, feel free to make reasonable assumptions based on your judgment. Document any such assumptions in this section to clarify your design decisions and implementation approach.

## 📦 Deliverables

At a high level, your submission should include:

- A working backend service

- Integration with the mock API

- Clear documentation outlining setup, API usage, and assumptions made

- A concise explanation of how your tracking logic works

- You are expected to make reasonable decisions about scope, edge cases, and any missing details

- Once you're done, please push your work to a private GitHub repository and add qxie3 as a collaborator so we can review your submission
