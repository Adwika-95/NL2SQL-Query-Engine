import { useState } from "react";
import axios from "axios";
import "./App.css";

const EXAMPLES = [
  "Top 5 customers by total spend",
  "Monthly order count for 2024",
  "Which product category generates the most revenue?",
  "Customers who placed more than 3 orders",
];

const SCHEMA = [
  { name: "customers", cols: "customer_id, name, city, country, signup_date" },
  { name: "products", cols: "product_id, name, category, unit_price" },
  { name: "orders", cols: "order_id, customer_id, order_date, status" },
  { name: "order_items", cols: "order_item_id, order_id, product_id, quantity" },
];

function App() {
  const [question, setQuestion] = useState("");
  const [sql, setSql] = useState("");
  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showSchema, setShowSchema] = useState(false);

  const runQuery = async (q) => {
    const query = q || question;
    if (!query) return;
    setQuestion(query);
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("http://localhost:8000/api/query", {
        question: query,
      });
      setSql(res.data.sql);
      setColumns(res.data.columns);
      setRows(res.data.rows);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
      setSql("");
      setRows([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="bg-illustration" />

      <div className="app">
        <div className="badge">⚡ ask in plain english, get real sql</div>
        <h1>NL2SQL <span className="accent">Query Engine</span></h1>
        <p className="subtitle">
          No memorizing joins. No syntax stress. Just ask your question like
          you'd ask a friend — Gemini writes the SQL, SQLite runs it, you get
          the answer.
        </p>

        <div className="schema-toggle" onClick={() => setShowSchema(!showSchema)}>
          <span>📋 Database schema</span>
          <span className="chevron">{showSchema ? "▲" : "▼"}</span>
        </div>

        {showSchema && (
          <div className="schema-card">
            {SCHEMA.map((t) => (
              <div key={t.name} className="schema-row">
                <span className="schema-table">{t.name}</span>
                <span className="schema-cols">{t.cols}</span>
              </div>
            ))}
          </div>
        )}

        <div className="query-box">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g. Who are my top 5 customers by spend?"
            onKeyDown={(e) => e.key === "Enter" && runQuery()}
          />
          <button onClick={() => runQuery()} disabled={loading}>
            {loading ? "Thinking..." : "Run ✨"}
          </button>
        </div>

        <div className="examples">
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              className="example-chip"
              onClick={() => runQuery(ex)}
            >
              {ex}
            </button>
          ))}
        </div>

        {error && <p className="error">⚠️ {error}</p>}

        {loading && (
          <div className="loading-card">
            <div className="spinner" />
            <span>Translating your question into SQL...</span>
          </div>
        )}

        {!loading && sql && (
          <div className="result-section">
            <h3>Generated SQL</h3>
            <pre className="sql-block">{sql}</pre>
          </div>
        )}

        {!loading && rows.length > 0 && (
          <div className="result-section">
            <h3>Results <span className="row-count">{rows.length} rows</span></h3>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    {columns.map((c) => (
                      <th key={c}>{c}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, i) => (
                    <tr key={i}>
                      {row.map((val, j) => (
                        <td key={j}>{String(val)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        <footer>
           Explore how LLMs translate human questions
          into database queries 🚀
        </footer>
      </div>
    </div>
  );
}

export default App;
