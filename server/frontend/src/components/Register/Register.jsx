import React, { useState } from "react";

export default function Register({ apiBase = "/djangoapp" }) {
  const [form, setForm] = useState({ username: "", first_name: "", last_name: "", email: "", password: "" });
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
        credentials: "include",
        body: JSON.stringify(form),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Registration failed");
      setStatus("Account created. You can now sign in.");
      setForm({ username: "", first_name: "", last_name: "", email: "", password: "" });
    } catch (error) {
      setStatus(error.message || "Unable to register. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="register-form">
      <h2>Create an account</h2>
      <label>Username<input name="username" placeholder="Username" autoComplete="username" value={form.username} onChange={update} required /></label>
      <label>First Name<input name="first_name" placeholder="First Name" autoComplete="given-name" value={form.first_name} onChange={update} required /></label>
      <label>Last Name<input name="last_name" placeholder="Last Name" autoComplete="family-name" value={form.last_name} onChange={update} required /></label>
      <label>Email<input name="email" type="email" placeholder="email" autoComplete="email" value={form.email} onChange={update} required /></label>
      <label>Password<input name="password" type="password" placeholder="Password" autoComplete="new-password" minLength={8} value={form.password} onChange={update} required /></label>
      <button type="submit" disabled={busy}>{busy ? "Creating account…" : "Register"}</button>
      <p role="status" aria-live="polite">{status}</p>
    </form>
  );
}
