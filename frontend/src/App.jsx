import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/health")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Health check failed");
        }
        return response.json();
      })
      .then(setHealth)
      .catch(() => setError(true));
  }, []);

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
        <p className="eyebrow">OVERVIEW</p>
        <h2>Your cloud operations workspace</h2>
        <p>
          Monitor services, inspect application health, and prepare
          your infrastructure for deployment.
        </p>
      </section>

      <section className="cards">
        <article className="card">
          <p className="card-label">APPLICATION</p>
          <h3>CloudOps Hub API</h3>
          <p>Flask backend service</p>
        </article>

        <article className="card">
          <p className="card-label">SERVICE STATUS</p>
          <h3 className={health ? "healthy" : error ? "failed" : ""}>
            {health ? "Healthy" : error ? "Unavailable" : "Checking..."}
          </h3>
          <p>
            {health
              ? "Health endpoint responding"
              : error
                ? "Check whether the backend is running"
                : "Connecting to the backend"}
          </p>
        </article>

        <article className="card">
          <p className="card-label">DEPLOYMENT</p>
          <h3>Local Development</h3>
          <p>Cloud deployment comes later</p>
        </article>
      </section>

      <footer>
        <span>CloudOps Hub · Project Day 1</span>
        <span>
          Last health check:{" "}
          {health
            ? new Date(health.timestamp).toLocaleTimeString()
            : "Not available"}
        </span>
      </footer>
    </main>
  );
}

export default App;
