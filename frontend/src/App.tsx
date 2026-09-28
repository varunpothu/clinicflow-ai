import { useEffect, useMemo, useState } from "react";
import Login from "./Login";
import { handleAuthCallback, isAuthenticated, logout, productionAuthEnabled } from "./auth";
import PatientRequest from "./PatientRequest";

type Approval = {
  id: string;
  patient: string;
  appointment: string;
  clinician: string;
  type: string;
  status: "PENDING" | "CONFLICT";
  age: string;
};

const initialApprovals: Approval[] = [
  { id: "APR-1042", patient: "Amelia Carter", appointment: "Tue 29 Sep · 16:30", clinician: "Dr. Sarah Wilson", type: "Routine consultation", status: "PENDING", age: "8 min" },
  { id: "APR-1041", patient: "Daniel Moore", appointment: "Wed 30 Sep · 10:00", clinician: "Dr. Liam Shah", type: "Follow-up", status: "PENDING", age: "14 min" },
  { id: "APR-1038", patient: "Priya Sharma", appointment: "Wed 30 Sep · 14:30", clinician: "Dr. Sarah Wilson", type: "Routine consultation", status: "CONFLICT", age: "21 min" },
];

const navItems = ["Overview", "Patient demo", "Approvals", "Calendar", "Exceptions", "Patients", "Audit"];

function StatCard({ label, value, hint, tone }: { label: string; value: string; hint: string; tone: "blue" | "purple" | "green" | "orange" }) {
  return (
    <article className={`stat-card ${tone}`}>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
      <div className="stat-hint">{hint}</div>
    </article>
  );
}

export default function App() {
  const [authenticated, setAuthenticated] = useState(
    !productionAuthEnabled || isAuthenticated(),
  );
  const [authError, setAuthError] = useState("");

  useEffect(() => {
    if (!productionAuthEnabled || window.location.pathname !== "/auth/callback") return;
    handleAuthCallback(window.location.search)
      .then(() => {
        window.history.replaceState({}, document.title, "/");
        setAuthenticated(true);
      })
      .catch((error: unknown) => {
        setAuthError(error instanceof Error ? error.message : "Sign-in failed.");
      });
  }, []);

  if (productionAuthEnabled && window.location.pathname === "/auth/callback" && !authenticated) {
    return <main className="shell"><section className="login-card"><h1>Signing you in…</h1><p>{authError || "Completing secure authentication."}</p></section></main>;
  }

  if (productionAuthEnabled && !authenticated) {
    return <Login />;
  }

  const [active, setActive] = useState("Overview");
  const [approvals, setApprovals] = useState(initialApprovals);
  const [toast, setToast] = useState("");
  const pending = useMemo(() => approvals.filter((item) => item.status === "PENDING").length, [approvals]);

  const actOnApproval = (id: string, action: "approve" | "reject") => {
    setApprovals((current) => current.filter((item) => item.id !== id));
    setToast(action === "approve" ? "Appointment approved and queued for booking." : "Proposal rejected and audited.");
    window.setTimeout(() => setToast(""), 2800);
  };

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark">✚</div><div><strong>ClinicFlow</strong><span>AI Operations</span></div></div>
        <nav>
          {navItems.map((item) => (
            <button className={active === item ? "nav-item active" : "nav-item"} key={item} onClick={() => setActive(item)}>
              <span className="nav-icon">{item === "Overview" ? "◈" : item === "Patient demo" ? "✦" : item === "Approvals" ? "✓" : item === "Calendar" ? "▦" : item === "Exceptions" ? "!" : item === "Patients" ? "◉" : "≡"}</span>
              {item}
            </button>
          ))}
        </nav>
        <div className="sidebar-footer"><div className="health-dot" /><div><strong>All systems healthy</strong><span>Demo environment</span></div></div>
      </aside>

      <main className="content">
        <header className="topbar">
          <div><div className="eyebrow">NORTHSTAR HEALTH CLINIC</div><h1>{active === "Overview" ? "Good afternoon, team" : active}</h1><p>Human-in-the-loop appointment operations dashboard.</p></div>
          <div className="header-actions"><span className="environment-chip">{productionAuthEnabled ? "PRODUCTION AUTH" : "LOCAL DEMO"}</span><button className="avatar" onClick={() => productionAuthEnabled && logout()} title={productionAuthEnabled ? "Sign out" : "Demo user"}>VS</button></div>
        </header>

        {active === "Patient demo" ? (
          <PatientRequest />
        ) : (
          <>
            <section className="hero-card">
              <div><div className="hero-kicker">TODAY'S CONTROL ROOM</div><h2>AI proposes. Your team decides.</h2><p>Review the highest-risk scheduling actions, resolve conflicts, and keep every booking decision traceable.</p></div>
              <div className="hero-flow"><span>AI</span><b>→</b><span>Rules</span><b>→</b><span className="human-pill">Human</span><b>→</b><span>Booking</span></div>
            </section>

            <section className="stats">
              <StatCard label="Pending approvals" value={String(pending)} hint="2 within SLA" tone="orange" />
              <StatCard label="Bookings today" value="38" hint="+12% vs last week" tone="green" />
              <StatCard label="Open exceptions" value="3" hint="1 needs attention" tone="purple" />
              <StatCard label="AI extraction" value="98.4%" hint="Schema-valid requests" tone="blue" />
            </section>

            <section className="workspace">
              <article className="panel approvals-panel"><div className="panel-header"><div><h3>Approval queue</h3><p>Decisions awaiting authorised staff.</p></div><span className="count-badge">{approvals.length}</span></div><div className="approval-list">{approvals.map((item) => <div className={`approval-card ${item.status === "CONFLICT" ? "conflict" : ""}`} key={item.id}><div className="patient-badge">{item.patient.split(" ").map((n) => n[0]).join("")}</div><div className="approval-main"><div className="approval-title-row"><strong>{item.patient}</strong><span className={item.status === "CONFLICT" ? "status-chip danger" : "status-chip pending"}>{item.status}</span></div><div className="meta-line">{item.type} · {item.clinician}</div><div className="meta-line">{item.appointment} · {item.age} ago</div></div><div className="approval-actions">{item.status === "CONFLICT" ? <button className="button secondary">Resolve</button> : <><button className="button reject" onClick={() => actOnApproval(item.id, "reject")}>Reject</button><button className="button approve" onClick={() => actOnApproval(item.id, "approve")}>Approve</button></>}</div></div>)}</div></article>

              <article className="panel timeline-panel"><div className="panel-header"><div><h3>Live workflow</h3><p>Recent events across the control plane.</p></div><span className="live-dot">LIVE</span></div><div className="timeline">{[["17:04","Appointment proposal created","APR-1042","purple"],["17:02","Availability conflict detected","APR-1038","red"],["16:59","Approval accepted","APR-1039","green"],["16:55","AI intent validated","REQ-2021","blue"],["16:51","Natural-language request received","REQ-2021","orange"]].map(([time,event,code,tone]) => <div className="timeline-row" key={`${time}-${code}`}><span className="time">{time}</span><span className={`timeline-dot ${tone}`} /><div><strong>{event}</strong><span>{code}</span></div></div>)}</div></article>
            </section>

            <section className="bottom-grid"><article className="panel exception-panel"><div className="panel-header"><div><h3>Exception health</h3><p>Issues requiring operational attention.</p></div><button className="text-button">View all →</button></div><div className="exception-row"><span className="severity high">HIGH</span><div><strong>Slot conflict</strong><span>1 proposal needs regeneration</span></div><span className="age-text">21m</span></div><div className="exception-row"><span className="severity medium">MEDIUM</span><div><strong>Notification retry</strong><span>Email provider retry 2/3</span></div><span className="age-text">7m</span></div><div className="exception-row"><span className="severity low">LOW</span><div><strong>AI fallback used</strong><span>Mock provider handled request</span></div><span className="age-text">3m</span></div></article><article className="panel architecture-panel"><div className="panel-header"><div><h3>System pulse</h3><p>Core service health.</p></div><span className="system-ok">● Healthy</span></div><div className="pulse-grid"><span><b>API</b><em>42ms</em></span><span><b>AI Gateway</b><em>680ms</em></span><span><b>Booking DB</b><em>18ms</em></span><span><b>Outbox</b><em>0 backlog</em></span></div></article></section>
          </>
        )}
      </main>
      {toast && <div className="toast">{toast}</div>}
    </div>
  );
}
