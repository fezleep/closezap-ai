import { useLeads } from '../hooks/useLeads';
import { LeadsTable } from './LeadsTable';
import { useState } from 'react';

export function Dashboard() {
  const { leads, loading, error, fetchLeads, createLead, closeLead } = useLeads();

  const [isOpen, setIsOpen] = useState(false);

  const [form, setForm] = useState({
  name: '',
  phone: '',
  interest: '',
});

  const [loadingCreate, setLoadingCreate] = useState(false);
  const [formError, setFormError] = useState('');

  const handleCreateLead = async () => {
  if (!form.name.trim() || !form.phone.trim()) {
    setFormError('name and phone are required');
    return;
  }

  try {
    setLoadingCreate(true);
    setFormError('');

    await createLead({
      name: form.name,
      phone: form.phone,
      interest: form.interest,
      status: 'new',
      intent: 'hot',
    });

    setForm({ name: '', phone: '', interest: '' });
    setIsOpen(false);
  } catch (err) {
    setFormError('could not create lead');
  } finally {
    setLoadingCreate(false);
  }
};

  const stats = {
    total: leads.length,
    new: leads.filter((lead) => lead.status === 'new').length,
    engaged: leads.filter((lead) => lead.status === 'engaged').length,
    closed: leads.filter((lead) => lead.status === 'closed').length,
    hot: leads.filter((lead) => lead.intent === 'hot').length,
  };

  return (
    <div className="min-h-screen bg-[#080808] text-zinc-100">
      <header className="border-b border-white/10 bg-[#080808]">
        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold tracking-tight">
              CloseZap <span className="text-[#d4af37]">AI</span>
            </h1>
            <p className="text-sm text-zinc-500">
              lead management and automation dashboard
            </p>
          </div>

          <span className="text-sm text-zinc-500">
            {new Date().toLocaleDateString('en-US', {
              weekday: 'long',
              month: 'long',
              day: 'numeric',
            })}
          </span>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-10">
        <section className="mb-8 rounded-3xl border border-white/10 bg-[#111111] p-8">
          <p className="text-sm font-medium text-[#d4af37] mb-3">
            portfolio project
          </p>

          <h2 className="max-w-3xl text-4xl font-semibold tracking-tight text-white">
            a clean system to manage leads, track intent and support sales automation
          </h2>

          <p className="mt-5 max-w-2xl leading-7 text-zinc-400">
            CloseZap AI simulates a real sales workflow. The goal is simple:
            organize leads, understand their stage and prepare the base for automated follow-ups.
          </p>

          <div className="mt-8 flex flex-wrap gap-3">
            <Tag>FastAPI</Tag>
            <Tag>React</Tag>
            <Tag>SQLite</Tag>
            <Tag>automation-ready</Tag>
          </div>

          <div className="mt-8 flex gap-3">
            <button
              onClick={() => setIsOpen(true)}
              className="rounded-xl bg-[#d4af37] px-5 py-2 text-sm font-medium text-black hover:opacity-90 transition"
            >
              create lead
            </button>

            <a
              href={`${import.meta.env.VITE_API_BASE_URL.replace('/api', '')}/docs`}
              target="_blank"
              className="rounded-xl border border-white/10 px-5 py-2 text-sm text-zinc-300 hover:bg-white/5 transition"
            >
              view API docs
            </a>
          </div>

        </section>

        

        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          <StatCard label="total leads" value={stats.total} />
          <StatCard label="new" value={stats.new} />
          <StatCard label="engaged" value={stats.engaged} />
          <StatCard label="closed" value={stats.closed} />
          <StatCard label="hot intent" value={stats.hot} highlight />
        </section>

        <section className="mb-8 rounded-3xl border border-white/10 bg-[#111111] p-6">
          <div className="max-w-3xl">
            <p className="text-sm font-medium text-[#d4af37]">
              how it works
            </p>

            <h2 className="mt-3 text-2xl font-semibold text-white">
              from a new lead to a clear sales opportunity
            </h2>

            <p className="mt-4 leading-7 text-zinc-400">
              CloseZap AI was built to make the sales process easier to understand.
              Every lead has a status, an intent and a context, so the person using the dashboard
              can quickly decide what needs attention.
            </p>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <FlowCard
              number="01"
              title="capture"
              text="a lead is created through the API and stored with basic contact information"
            />

            <FlowCard
              number="02"
              title="understand"
              text="the system shows status, interest and intent to make the opportunity easier to read"
            />

            <FlowCard
              number="03"
              title="act"
              text="the user can follow the pipeline and close leads when they become customers"
            />
          </div>
        </section>

        <section className="overflow-hidden rounded-3xl border border-white/10 bg-[#111111]">
          <div className="flex items-center justify-between border-b border-white/10 px-6 py-5">
            <div>
              <h2 className="text-lg font-semibold text-white">Leads dashboard</h2>
              <p className="text-sm text-zinc-500">
                data provided by the FastAPI backend
              </p>
            </div>

            <button
              onClick={fetchLeads}
              className="rounded-xl border border-[#d4af37]/40 px-4 py-2 text-sm font-medium text-[#d4af37] hover:bg-[#d4af37] hover:text-black transition"
            >
              Refresh
            </button>
          </div>

          <div className="p-6">
            {loading ? (
              <div className="py-16 text-center text-zinc-500">
                loading leads...
              </div>
            ) : error ? (
              <div className="py-16 text-center">
                <p className="font-medium text-[#d4af37]">error loading leads</p>
                <p className="mt-2 text-zinc-500">{error}</p>
              </div>
            ) : (
              <LeadsTable leads={leads} onCloseLead={closeLead} />
            )}
          </div>
        </section>
            </main>

      {isOpen && (
        <div
          className="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
          onClick={() => setIsOpen(false)}
        >
          <div
            className="w-full max-w-md rounded-2xl bg-[#111111] border border-white/10 p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-lg font-semibold text-white">
              create new lead
            </h2>

            <div className="mt-4 space-y-3">
              <input
                placeholder="name"
                className="w-full bg-black/30 border border-white/10 rounded-lg px-3 py-2 text-sm text-white"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />

              <input
                placeholder="phone"
                className="w-full bg-black/30 border border-white/10 rounded-lg px-3 py-2 text-sm text-white"
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
              />

              <input
                placeholder="interest"
                className="w-full bg-black/30 border border-white/10 rounded-lg px-3 py-2 text-sm text-white"
                value={form.interest}
                onChange={(e) => setForm({ ...form, interest: e.target.value })}
              />
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => {
                  setIsOpen(false);
                  setForm({ name: '', phone: '', interest: '' });
                }}
              >
                cancel
              </button>

              <button
                onClick={handleCreateLead}
                disabled={loadingCreate}
                className="px-4 py-2 rounded-lg bg-[#d4af37] text-black text-sm font-medium disabled:opacity-60"
              >
                {loadingCreate ? 'creating...' : 'create'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Tag({ children }) {
  return (
    <span className="rounded-full border border-white/10 bg-black/20 px-4 py-2 text-sm text-zinc-300">
      {children}
    </span>
  );
}

function StatCard({ label, value, highlight = false }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#111111] p-5">
      <p className={highlight ? 'text-sm text-[#d4af37]' : 'text-sm text-zinc-500'}>
        {label}
      </p>
      <p className={highlight ? 'mt-3 text-3xl font-semibold text-[#d4af37]' : 'mt-3 text-3xl font-semibold text-white'}>
        {value}
      </p>
    </div>
  );
}

function FlowCard({ number, title, text }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
      <div className="mb-4 flex h-9 w-9 items-center justify-center rounded-full border border-[#d4af37]/40 text-sm font-medium text-[#d4af37]">
        {number}
      </div>

      <h3 className="font-semibold text-white">{title}</h3>

      <p className="mt-2 text-sm leading-6 text-zinc-500">
        {text}
      </p>




    </div>
  );
}