# ChronoPlan AI – Task Prioritization Assistant

ChronoPlan is a smart, AI-powered task management assistant that helps users organize and prioritize their daily tasks based on contextual understanding and calendar events. Built using Python and LMQL (Language Model Query Language), ChronoPlan leverages large language models to make real-time decisions that reflect user intent and scheduling constraints.

---

## Features

- **AI-Powered Prioritization**: Uses LMQL to prioritize tasks by interpreting natural language inputs and contextual cues like urgency, dependencies, and scheduling conflicts.
- **Calendar Integration**: Syncs with Google Calendar to avoid conflicts and propose optimal task timings.
- **JSON-Based Task Input**: Supports structured task input via JSON files.
- **Custom Rule Logic**: Task rules (e.g., "Doctor appointments override gym sessions") are encoded as LMQL queries.

---

## How LMQL is Used

LMQL serves as the reasoning engine in this project. It enables querying large language models with structured constraints. Here's how it's integrated:

- **Task Evaluation**: LMQL scripts process task descriptions and metadata to compute task priority scores.
- **Constraint Handling**: Ensures priority logic (deadlines, user preferences, or task type rules) are enforced in a human-readable way.
- **Natural Language Interface**: Converts free-form task input into structured data via LMQL prompts.

## High level diagram
![A helpful diagram of ChronoPlan’s workflow](/chronoplan/docs/chronoplan.png)

## Output Visualization

The following image illustrates how ChronoPlan assigns weights to tasks based on contextual importance and user-defined preferences. The integration with LMQL enables natural language understanding to dynamically prioritize tasks with respect to time sensitivity, category, and urgency:

![Task Prioritization Output](/chronoplan/docs/output.png)

## 🚀 Future Work

While ChronoPlan is already a powerful tool for task prioritization, there are several enhancements and features in the pipeline:

- **AI-Powered Prioritization Improvements**: We plan to integrate more advanced machine learning models to further refine task prioritization based on user preferences and historical data.
- **Real-Time Collaboration**: Enabling multi-user collaboration to manage and prioritize tasks together, allowing team-based task management.
- **Mobile App Development**: Exploring options for mobile app integration to bring task management to your fingertips on the go.
- **Enhanced Data Visualizations**: Expanding task prioritization insights with more in-depth data visualizations and performance metrics.
- **Natural Language Understanding (NLU)**: Improving the task input system using NLU techniques, making task entry even more intuitive and responsive to varied user commands.
  
We are also considering building integrations with other popular productivity tools like **Trello**, and **Asana** to further streamline task management for users.

## 🤝 Collaborate with Us

We are open to collaborations to help build ChronoPlan into a more powerful tool for task management! Whether you are an individual or part of a team, we welcome contributions and ideas.

### How You Can Contribute:
- **Open-source Development**: Feel free to fork the repository and submit a pull request.
- **Feature Requests**: If you have an idea that could enhance ChronoPlan, create an issue to discuss it with us.
- **Bug Fixes and Improvements**: Help us improve the stability and performance by tackling existing issues or suggesting optimizations.
  
If you're interested in contributing or want to discuss potential collaborations, don't hesitate to reach out directly to us!

Together, we can make ChronoPlan an even better tool for task management and productivity.

