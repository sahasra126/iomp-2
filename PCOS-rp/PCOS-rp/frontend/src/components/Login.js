// src/components/Login.jsx
import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate(); // <-- correct usage
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!email || !password) {
      setError("Email and password are required");
      return;
    }

    setBusy(true);
    try {
      const res = await login(email, password);
      console.log("[Login] login result:", res);

      if (res && res.success) {
        // prefer a protected page — change path if you want a different landing
        const target = "/"; // or "/lifestyle-assessment"
        try {
          navigate(target);
        } catch (err) {
          // fallback if navigate fails for any reason
          console.warn("[Login] navigate failed, falling back to full reload:", err);
          window.location.href = target;
        }
      } else {
        // show backend error message (if present)
        setError(res?.error || "Login failed");
      }
    } catch (err) {
      console.error("[Login] unexpected error", err);
      setError("An unexpected error occurred. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "40px auto", padding: 20, border: "1px solid #eee", borderRadius: 8 }}>
      <h2 style={{ marginBottom: 8 }}>Login</h2>
      <form onSubmit={handleSubmit}>
        <label style={{ display: "block", marginBottom: 6 }}>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ display: "block", width: "100%", padding: 8, marginTop: 6 }}
            required
          />
        </label>

        <label style={{ display: "block", marginBottom: 12 }}>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ display: "block", width: "100%", padding: 8, marginTop: 6 }}
            required
          />
        </label>

        {error && <div style={{ color: "crimson", marginBottom: 12 }}>{error}</div>}

        <button type="submit" disabled={busy} style={{ padding: "10px 16px" }}>
          {busy ? "Signing in..." : "Sign in"}
        </button>
      </form>
    </div>
  );
}
