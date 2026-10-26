import React, { useEffect, useState } from "react";
import Register from "./components/Register/Register.jsx";

const API = "/djangoapp";
async function request(path, options = {}) {
  const response = await fetch(API + path, {
    credentials: "include",
    ...options,
    headers: { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(options.headers || {}) }
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

export default function App() {
  const [dealers, setDealers] = useState([]);
  const [state, setState] = useState("");
  const [selected, setSelected] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [review, setReview] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  async function loadDealers(filter = "") {
    try {
      const result = await request(filter ? `/get_dealers?state=${encodeURIComponent(filter)}` : "/get_dealers");
      setDealers(result.dealers || []);
    } catch (error) { setNotice(error.message); }
  }
  async function openDealer(dealer) {
    setSelected(dealer);
    setNotice("");
    try {
      const result = await request(`/get_dealer_reviews/${dealer.id}`);
      setReviews(result.reviews || []);
    } catch (error) { setReviews([]); setNotice(error.message); }
  }
  useEffect(() => { loadDealers(); }, []);

  async function signIn(event) {
    event.preventDefault(); setBusy(true); setNotice("");
    try {
      await request("/login", { method: "POST", body: JSON.stringify({ username, password }) });
      setLoggedIn(true); setNotice("Signed in successfully."); setPassword("");
    } catch (error) { setNotice(error.message); }
    finally { setBusy(false); }
  }
  async function signOut() {
    try { await request("/logout", { method: "POST", body: JSON.stringify({}) }); setLoggedIn(false); setNotice("You are signed out."); }
    catch (error) { setNotice(error.message); }
  }
  async function submitReview(event) {
    event.preventDefault(); setBusy(true); setNotice("");
    try {
      await request("/add_review", { method: "POST", body: JSON.stringify({ dealer_id: selected.id, review }) });
      setReview(""); setNotice("Review added successfully."); await openDealer(selected);
    } catch (error) { setNotice(error.message); }
    finally { setBusy(false); }
  }

  return <div className="app-shell">
    <header className="topbar"><a className="brand" href="#"><span className="brand-mark">C</span> Cars Dealership</a><nav><a href="#dealers">Dealers</a><a href="/About.html">About</a><a href="/Contact.html">Contact</a></nav><span className="session">{loggedIn ? <><span>Signed in</span><button className="button ghost small" onClick={signOut}>Log out</button></> : <span>Guest session</span>}</span></header>
    <main>
      <section className="hero"><div><p className="eyebrow">THE BETTER WAY TO SHOP</p><h1>Find a dealer you<br/>can <em>trust.</em></h1><p className="hero-copy">Explore local dealerships, read real feedback, and share your experience with the community.</p><a className="button" href="#dealers">Explore dealerships <span>↗</span></a></div><div className="hero-art" aria-hidden="true"><div className="sun"></div><div className="road"></div><div className="car"><div className="window"></div><div className="wheel wheel-one"></div><div className="wheel wheel-two"></div></div><div className="art-caption">YOUR NEXT CHAPTER STARTS HERE</div></div></section>
      <section className="content-grid" id="dealers"><div className="dealer-column"><div className="section-head"><div><p className="eyebrow">DISCOVER</p><h2>Dealerships near you</h2></div><span className="count">{dealers.length} listed</span></div>
      <form className="filter" onSubmit={e => {e.preventDefault();loadDealers(state.trim().toUpperCase());}}><label htmlFor="state">Filter by state</label><input id="state" value={state} maxLength={2} placeholder="e.g. TX" onChange={e => setState(e.target.value.toUpperCase())}/><button className="button" type="submit">Search</button><button className="button ghost" type="button" onClick={() => {setState("");loadDealers("");}}>Reset</button></form>
      <div className="dealer-list">{dealers.map((dealer,index)=><button key={dealer.id} className={selected?.id===dealer.id?"dealer-card active":"dealer-card"} onClick={() => openDealer(dealer)}><span className="dealer-number">{String(index+1).padStart(2,"0")}</span><span className="dealer-info"><strong>{dealer.name}</strong><small>{[dealer.city,dealer.state].filter(Boolean).join(", ")}</small><small>{dealer.address}</small></span><span className="arrow">↗</span></button>)}{dealers.length===0&&<div className="empty">No dealerships yet. Run <code>python manage.py seed_dealers</code> after migrations.</div>}</div>
      </div>
      <aside className="side-panel">{selected ? <><p className="eyebrow">DEALER PROFILE</p><h2>{selected.name}</h2><p className="muted">{[selected.address,selected.city,selected.state,selected.zip].filter(Boolean).join(", ")}</p>{selected.phone&&<p>{selected.phone}</p>}{selected.website&&<a href={selected.website} target="_blank" rel="noreferrer">Visit website ↗</a>}<div className="rule"></div><div className="section-head"><h3>Customer reviews</h3><span className="count">{reviews.length}</span></div>{reviews.length?reviews.map(item=><article className="review" key={item.id}><div className="review-meta"><strong>{item.name}</strong><span>{item.sentiment||"review"}</span></div><p>{item.review_text}</p></article>):<p className="muted">No reviews yet. Be the first to share your experience.</p>}{loggedIn&&<form className="review-form" onSubmit={submitReview}><label htmlFor="review">Write a review</label><textarea id="review" value={review} onChange={e=>setReview(e.target.value)} rows="4" minLength="5" required placeholder="What was your experience like?"/><button className="button" disabled={busy}>{busy?"Submitting…":"Submit review"}</button></form>}{!loggedIn&&<p className="muted small-note">Sign in to submit a review.</p>}</>:<div className="select-prompt"><div className="prompt-icon">↖</div><h3>Select a dealership</h3><p>Choose a listing to view its profile and customer feedback.</p></div>}
      <div className="login-panel"><div className="section-head"><h3>{loggedIn?"Your account":"Member sign in"}</h3>{!loggedIn&&<button className="text-button" onClick={()=>setShowRegister(!showRegister)}>{showRegister?"Sign in":"Register"}</button>}</div>{!loggedIn&&!showRegister?<form onSubmit={signIn}><label htmlFor="username">Username</label><input id="username" value={username} onChange={e=>setUsername(e.target.value)} required autoComplete="username"/><label htmlFor="password">Password</label><input id="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} required autoComplete="current-password"/><button className="button full" disabled={busy}>{busy?"Signing in…":"Sign in"}</button></form>:!loggedIn?<Register/>:<p className="muted">You are signed in and can add a review to a selected dealership.</p>}</div></aside></section>
      {notice&&<div className="notice" role="status"><span>{notice}</span><button aria-label="Dismiss message" onClick={()=>setNotice("")}>×</button></div>}
    </main><footer><span>Cars Dealership Capstone</span><span>Built for better-informed car shopping.</span></footer>
  </div>;
}
