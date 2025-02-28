import axios from "axios";
import React, { useEffect, useState } from "react";

const ViewTasks = () => {
    const [viewTask, setViewTask] = useState<string[]>([]);
    const [prioritizedTasks, setPrioritizedTasks] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchAllTasks = async () => {
            try {
                const { data } = await axios.get("http://localhost:8000/todos");
                console.log("Fetched tasks:", data.todos);
                setViewTask(data.todos);
                prioritizeTasks(data.todos); // Send to Ollama for prioritization
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        };

        fetchAllTasks();
    }, []);

    const prioritizeTasks = async (tasks: string[]) => {
        if (tasks.length === 0) return;
        setLoading(true);

        try {
            const response = await axios.post("http://localhost:8000/prioritize_tasks/", { tasks });
            console.log("Prioritized tasks:", response.data.prioritized_tasks);
            setPrioritizedTasks(response.data.prioritized_tasks);
        } catch (error) {
            console.error("Error prioritizing tasks:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="flex flex-col items-center mt-5">
            <h1 className="text-center text-xl font-bold">View your tasks for today</h1>

            {loading ? (
                <p className="text-gray-500">Prioritizing tasks...</p>
            ) : (
                <ul className="mt-3">
                    {prioritizedTasks.length > 0 ? (
                        prioritizedTasks.map((task, index) => <li key={index}>{task}</li>)
                    ) : (
                        <li>No tasks available</li>
                    )}
                </ul>
            )}
        </section>
    );
};

export default ViewTasks;
