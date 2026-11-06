
import { useCallback, useEffect, useState } from "react";
import "./App.css";

const API = "/api";

const EMPTY_FORM = {
  title: "",
  description: "",
  status: "pending",
};

function App() {
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);
  const [health, setHealth] = useState("Checking...");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const request = async (path, options = {}) => {
    const response = await fetch(`${API}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.error || `Request failed: ${response.status}`);
    }

    return data;
  };

  const loadTasks = useCallback(async () => {
    try {
      setError("");
      const data = await request("/tasks");
      setTasks(Array.isArray(data) ? data : data.tasks || []);
    } catch (err) {
      setError(`Could not load tasks: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, []);

  const checkHealth = useCallback(async () => {
    try {
      const data = await request("/health");
      setHealth(data.status === "healthy" ? "Healthy" : "Unhealthy");
    } catch {
      setHealth("Unavailable");
    }
  }, []);

  useEffect(() => {
    loadTasks();
    checkHealth();
  }, [loadTasks, checkHealth]);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const resetForm = () => {
    setForm(EMPTY_FORM);
    setEditingId(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!form.title.trim()) {
      setError("Please enter a task title.");
      return;
    }

    try {
      setSaving(true);
      setError("");
      setNotice("");

      const payload = {
        title: form.title.trim(),
        description: form.description.trim(),
        status: form.status,
      };

      if (editingId !== null) {
        await request(`/tasks/${editingId}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
        setNotice("Task updated successfully.");
      } else {
        await request("/tasks", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        setNotice("Task created successfully.");
      }

      resetForm();
      await loadTasks();
    } catch (err) {
      setError(`Unable to save task: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const startEditing = (task) => {
    setEditingId(task.id);
    setForm({
      title: task.title || "",
      description: task.description || "",
      status: task.status || "pending",
    });
    setError("");
    setNotice("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const deleteTask = async (task) => {
    if (!window.confirm(`Delete "${task.title}"?`)) {
      return;
    }

    try {
      setError("");
      setNotice("");

      await request(`/tasks/${task.id}`, {
        method: "DELETE",
      });

      if (editingId === task.id) {
        resetForm();
      }

      setNotice("Task deleted successfully.");
      await loadTasks();
    } catch (err) {
      setError(`Unable to delete task: ${err.message}`);
    }
  };

  const completedCount = tasks.filter(
    (task) => task.status === "completed"
  ).length;

  const pendingCount = tasks.filter(
    (task) => task.status === "pending"
  ).length;

  return (
    <main className="dashboard">
      <header className="topbar">
        <div>
          <p className="eyebrow">CLOUD OPERATIONS</p>
          <h1>CloudOps Hub</h1>
        </div>
        <span className="environment">LOCAL ENVIRONMENT</span>
      </header>

      <section className="welcome">
        <p className="eyebrow">OPERATIONS WORKSPACE</p>
        <h2>Manage your cloud operations</h2>
        <p>
          Track engineering tasks, monitor service health, and prepare
          your infrastructure for deployment.
        </p>
      </section>

      <section className="cards">
        <article className="card">
          <p className="card-label">TOTAL TASKS</p>
          <h3>{tasks.length}</h3>
          <p>Tasks stored in the database</p>
        </article>

        <article className="card">
          <p className="card-label">COMPLETED</p>
          <h3>{completedCount}</h3>
          <p>Tasks finished</p>
        </article>

        <article className="card">
          <p className="card-label">PENDING</p>
          <h3>{pendingCount}</h3>
          <p>Tasks awaiting work</p>
        </article>

        <article className="card">
          <p className="card-label">API STATUS</p>
          <h3 className={health === "Healthy" ? "healthy" : ""}>
            {health}
          </h3>
          <p>Flask and PostgreSQL health check</p>
          <button type="button" onClick={checkHealth}>
            Check again
          </button>
        </article>
      </section>

      {error && <p className="message error">{error}</p>}
      {notice && <p className="message success">{notice}</p>}

      <section className="task-layout">
        <article className="panel">
          <h2>{editingId !== null ? "Edit task" : "Create a task"}</h2>
          <p className="panel-description">
            {editingId !== null
              ? `Editing task #${editingId}`
              : "Add an item to your operations work queue."}
          </p>

          <form onSubmit={handleSubmit}>
            <label htmlFor="title">Task title</label>
            <input
              id="title"
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="e.g. Configure AWS monitoring"
              maxLength={200}
              required
            />

            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={form.description}
              onChange={handleChange}
              placeholder="Describe the work to be completed"
              rows={4}
            />

            <label htmlFor="status">Status</label>
            <select
              id="status"
              name="status"
              value={form.status}
              onChange={handleChange}
            >
              <option value="pending">Pending</option>
              <option value="in_progress">In progress</option>
              <option value="completed">Completed</option>
            </select>

            <button type="submit" disabled={saving}>
              {saving
                ? "Saving..."
                : editingId !== null
                  ? "Save changes"
                  : "Create task"}
            </button>

            {editingId !== null && (
              <button type="button" onClick={resetForm}>
                Cancel editing
              </button>
            )}
          </form>
        </article>

        <article className="panel task-panel">
          <div className="task-heading">
            <div>
              <h2>Operations tasks</h2>
              <p className="panel-description">
                Tasks loaded from the backend API.
              </p>
            </div>
            <button type="button" onClick={loadTasks}>
              Refresh
            </button>
          </div>

          {loading ? (
            <p>Loading tasks...</p>
          ) : tasks.length === 0 ? (
            <p>No tasks found. Create your first task.</p>
          ) : (
            <div className="task-list">
              {tasks.map((task) => (
                <article className="task-item" key={task.id}>
                  <div className="task-title-row">
                    <h3>{task.title}</h3>
                    <span className={`status status-${task.status}`}>
                      {(task.status || "pending").replace("_", " ")}
                    </span>
                  </div>

                  <p>{task.description || "No description provided."}</p>
                  <small>Task ID: {task.id}</small>

                  <div className="task-actions">
                    <button
                      type="button"
                      onClick={() => startEditing(task)}
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      onClick={() => deleteTask(task)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </article>
      </section>

      <footer>
        <span>CloudOps Hub · Local Development</span>
        <span>Flask API · PostgreSQL</span>
      </footer>
    </main>
  );
}

export default App;
