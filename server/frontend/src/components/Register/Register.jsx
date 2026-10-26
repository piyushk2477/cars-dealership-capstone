import React, { useState } from "react";

export default function Register({ apiBase = "/djangoapp" }) {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  function update(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setStatus("");
    try {
      const response = await fetch(`${apiBase}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Registration failed");
      setStatus("Account created. You can now sign in.");
      setForm({ username: "", email: "", password: "" });
    } catch (error) {
      setStatus(error.message || "Unable to register. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="register-form">
      <h2>Create an account</h2>
      <label>Username<input name="username" autoComplete="username" value={form.username} onChange={update} required /></label>
      <label>Email<input name="email" type="email" autoComplete="email" value={form.email} onChange={update} required /></label>
      <label>Password<input name="password" type="password" autoComplete="new-password" minLength={8} value={form.password} onChange={update} required /></label>
      <button type="submit" disabled={busy}>{busy ? "Creating account…" : "Register"}</button>
      <p role="status" aria-live="polite">{status}</p>
    </form>
  );
}
